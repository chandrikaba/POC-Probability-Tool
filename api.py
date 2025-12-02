"""
FastAPI Application for Deal Win Probability Prediction

This API provides endpoints to:
1. Generate synthetic training data
2. Train the XGBoost model
3. Predict deal outcomes from uploaded Excel files
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any
import pandas as pd
import joblib
import os
import io
from datetime import datetime
from sklearn.preprocessing import LabelEncoder

# Initialize FastAPI app
app = FastAPI(
    title="Deal Win Probability API",
    description="API for predicting deal win probability using XGBoost classifier",
    version="1.0.0",
    docs_url="/swagger",
    redoc_url="/redoc"
)

# Define paths
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "xgb_classifier.pkl")
SYNTHETIC_DATA_PATH = os.path.join(PROJECT_ROOT, "data", "output", "synthetic_deals.xlsx")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data", "output")

# Pydantic models for request/response
class HealthResponse(BaseModel):
    status: str
    message: str
    model_loaded: bool

class PredictionResponse(BaseModel):
    success: bool
    message: str
    predictions_file: str
    total_records: int

class TrainingResponse(BaseModel):
    success: bool
    message: str
    validation_accuracy: float
    model_path: str

class SyntheticDataResponse(BaseModel):
    success: bool
    message: str
    records_generated: int
    output_path: str


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - API information"""
    return {
        "name": "Deal Win Probability API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "swagger": "/swagger",
            "redoc": "/redoc",
            "generate_data": "/generate-synthetic-data",
            "train": "/train-model",
            "predict": "/predict"
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Check API health and model availability"""
    model_exists = os.path.exists(MODEL_PATH)
    
    return HealthResponse(
        status="healthy",
        message="API is running",
        model_loaded=model_exists
    )


@app.post("/generate-synthetic-data", response_model=SyntheticDataResponse, tags=["Data Generation"])
async def generate_synthetic_data():
    """
    Generate synthetic training data
    
    This endpoint runs the synthetic data generation script to create
    training data for the XGBoost model.
    """
    try:
        # Import and run the generation script
        import subprocess
        import sys
        
        script_path = os.path.join(PROJECT_ROOT, "src", "generate_synthetic_data.py")
        result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
        
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Data generation failed: {result.stderr}")
        
        # Check if file was created
        if not os.path.exists(SYNTHETIC_DATA_PATH):
            raise HTTPException(status_code=500, detail="Synthetic data file not created")
        
        # Count records
        df = pd.read_excel(SYNTHETIC_DATA_PATH)
        
        return SyntheticDataResponse(
            success=True,
            message="Synthetic data generated successfully",
            records_generated=len(df),
            output_path=SYNTHETIC_DATA_PATH
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/train-model", response_model=TrainingResponse, tags=["Model Training"])
async def train_model():
    """
    Train the XGBoost classifier model
    
    This endpoint trains a new model using the synthetic data.
    The model is saved to the models directory.
    """
    try:
        import subprocess
        import sys
        
        # Check if synthetic data exists
        if not os.path.exists(SYNTHETIC_DATA_PATH):
            raise HTTPException(
                status_code=400, 
                detail="Synthetic data not found. Please generate data first using /generate-synthetic-data"
            )
        
        script_path = os.path.join(PROJECT_ROOT, "src", "train_xgb_classifier.py")
        result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
        
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Model training failed: {result.stderr}")
        
        # Extract accuracy from output (if printed)
        accuracy = 0.0
        if "Validation Accuracy:" in result.stdout:
            try:
                accuracy_line = [line for line in result.stdout.split('\n') if 'Validation Accuracy:' in line][0]
                accuracy = float(accuracy_line.split(':')[1].strip())
            except:
                pass
        
        return TrainingResponse(
            success=True,
            message="Model trained successfully",
            validation_accuracy=accuracy,
            model_path=MODEL_PATH
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict_deal_outcomes(file: UploadFile = File(..., description="Excel file with deal data")):
    """
    Predict deal outcomes from uploaded Excel file
    
    Upload an Excel file with deal information and get predictions.
    The file should have the same structure as the training data.
    
    Returns a downloadable Excel file with predictions.
    """
    try:
        import numpy as np
        
        # Check if model exists
        if not os.path.exists(MODEL_PATH):
            raise HTTPException(
                status_code=400,
                detail="Model not found. Please train the model first using /train-model"
            )
        
        # Check if label encoder exists
        encoder_path = os.path.join(PROJECT_ROOT, "models", "label_encoder.pkl")
        if not os.path.exists(encoder_path):
            raise HTTPException(
                status_code=400,
                detail="Label encoder not found. Please train the model first using /train-model"
            )
        
        # Validate file type
        if not file.filename.endswith(('.xlsx', '.xls')):
            raise HTTPException(status_code=400, detail="Only Excel files (.xlsx, .xls) are supported")
        
        # Read uploaded file
        contents = await file.read()
        raw_df = pd.read_excel(io.BytesIO(contents), skiprows=1)
        
        # Load model and label encoder
        model = joblib.load(MODEL_PATH)
        le = joblib.load(encoder_path)
        
        # Load synthetic data to get expected column structure
        if not os.path.exists(SYNTHETIC_DATA_PATH):
            raise HTTPException(status_code=400, detail="Synthetic data not found. Please train the model first.")
        
        synthetic_df = pd.read_excel(SYNTHETIC_DATA_PATH)
        drop_cols = ["CRM ID", "Opportunity Name", "Account Name", "Detailed Remarks", "Deal Status"]
        expected_cols = [c for c in synthetic_df.columns if c not in drop_cols]
        
        # Get the expected types for each column from synthetic data
        expected_types = {}
        for col in expected_cols:
            expected_types[col] = synthetic_df[col].dtype
        
        # Add missing columns with appropriate default values based on expected type
        for col in expected_cols:
            if col not in raw_df.columns:
                if expected_types[col] in ['int64', 'float64']:
                    raw_df[col] = 0.0
                else:
                    raw_df[col] = "UNKNOWN"
        
        # Preprocessing - same as training
        X_input = raw_df.drop(columns=[c for c in drop_cols if c in raw_df.columns], errors="ignore").copy()
        
        # Convert columns to match expected types from training
        for col in X_input.columns:
            if col in expected_types:
                if expected_types[col] in ['int64', 'float64']:
                    # This should be numeric
                    X_input[col] = pd.to_numeric(X_input[col], errors='coerce')
                else:
                    # This should be categorical
                    X_input[col] = X_input[col].astype(str)
        
        # Now identify numeric vs categorical based on actual dtypes
        numeric_cols = X_input.select_dtypes(include=['int64', 'float64']).columns.tolist()
        categorical_cols = X_input.select_dtypes(include=['object']).columns.tolist()
        
        # Clean categorical columns
        for col in categorical_cols:
            X_input[col] = X_input[col].str.strip()
            X_input[col] = X_input[col].replace({'nan': np.nan, 'None': np.nan, '': np.nan, 'NaN': np.nan})
            X_input[col] = X_input[col].fillna("UNKNOWN")
        
        # Impute numeric columns
        for col in numeric_cols:
            if X_input[col].isna().any():
                median_val = X_input[col].median()
                if pd.isna(median_val):
                    median_val = 0.0
                X_input[col] = X_input[col].fillna(median_val)

        
        # Predict using pipeline
        pred_numeric = model.predict(X_input)
        pred_labels = le.inverse_transform(pred_numeric)
        
        # Get probabilities
        pred_probs = model.predict_proba(X_input)
        
        # Create result dataframe
        result_df = raw_df.copy()
        result_df["Predicted Deal Status"] = pred_labels
        
        # Add probability columns
        for idx, class_name in enumerate(le.classes_):
            result_df[f"Probability_{class_name}"] = pred_probs[:, idx]
        
        # Remove Deal Status column if exists
        if "Deal Status" in result_df.columns:
            result_df = result_df.drop(columns=["Deal Status"])
        
        # Save to output
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"predictions_{timestamp}.xlsx"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        result_df.to_excel(output_path, index=False)
        
        return PredictionResponse(
            success=True,
            message="Predictions generated successfully",
            predictions_file=output_filename,
            total_records=len(result_df)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.get("/download-predictions/{filename}", tags=["Prediction"])
async def download_predictions(filename: str):
    """
    Download a predictions file
    
    Provide the filename returned from the /predict endpoint to download the results.
    """
    file_path = os.path.join(OUTPUT_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


@app.get("/model-info", tags=["Model"])
async def get_model_info():
    """Get information about the current model"""
    if not os.path.exists(MODEL_PATH):
        return {
            "model_exists": False,
            "message": "No model found. Please train a model first."
        }
    
    model_stats = os.stat(MODEL_PATH)
    
    return {
        "model_exists": True,
        "model_path": MODEL_PATH,
        "model_size_mb": round(model_stats.st_size / (1024 * 1024), 2),
        "last_modified": datetime.fromtimestamp(model_stats.st_mtime).isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
