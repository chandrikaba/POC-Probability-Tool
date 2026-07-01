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
SYNTHETIC_DATA_PATH = os.path.join(PROJECT_ROOT, "data", "output", "synthetic_data_v3.xlsx")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data", "output")

# Global mappings for normalization and scoring
NORMALIZATION_MAP = {
    "Account Engagement": {
        "high": "High (Existing+Good)", "good": "High (Existing+Good)",
        "medium": "Medium (Existing+Poor)", "average": "Medium (Existing+Poor)",
        "low": "Low (New Account)", "new": "Low (New Account)", "none": "Low (New Account)"
    },
    "Client Relationship": {
        "high": "Strong", "strong": "Strong", "good": "Strong",
        "medium": "Neutral", "neutral": "Neutral", "average": "Neutral",
        "low": "Weak", "weak": "Weak", "poor": "Weak", "new": "Weak", "none": "Weak"
    },
    "Deal Coach": {
        "active": "Active & Available", "available": "Active & Available",
        "passive": "Passive",
        "not": "Not Available", "none": "Not Available"
    },
    "Incumbency Share": {
        "high": "High (>50%)", ">50%": "High (>50%)",
        "medium": "Medium (20-50%)", "20-50%": "Medium (20-50%)",
        "low": "Low (<20%)", "<20%": "Low (<20%)", "none": "None"
    },
    "Bidder Rank": {
        "1": "Top", "top": "Top", "first": "Top", "high": "Top",
        "2": "Middle", "middle": "Middle", "second": "Middle", "medium": "Middle",
        "3": "Bottom", "bottom": "Bottom", "last": "Bottom", "low": "Bottom"
    },
    "References": {
        "strong": "Strong (Domain+Tech)",
        "average": "Average", "medium": "Average",
        "weak": "Weak/None", "none": "Weak/None"
    },
    "Solution Strength": {
        "high": "Strong (Covers all)", "strong": "Strong (Covers all)",
        "medium": "Average (Gaps)", "average": "Average (Gaps)",
        "low": "Weak", "weak": "Weak"
    },
    "Client Impression": {
        "positive": "Positive", "good": "Positive",
        "neutral": "Neutral", "medium": "Neutral",
        "negative": "Negative", "bad": "Negative"
    },
    "Orals Score": {
        "strong": "Strong", "high": "Strong",
        "par": "At Par", "medium": "At Par", "average": "At Par",
        "weak": "Weak", "low": "Weak"
    },
    "Price Alignment": {
        "on par": "On par with Client Budget", "budget": "On par with Client Budget", "aligned": "On par with Client Budget", "high": "On par with Client Budget",
        "caveats": "Above Client Budget with Rationale/Caveats", "rationale": "Above Client Budget with Rationale/Caveats", "medium": "Above Client Budget with Rationale/Caveats",
        "above": "Above Client Budget", "deviating": "Above Client Budget", "low": "Above Client Budget",
        "info not available": "Client Budget Info not available", "no intel": "Client Budget Info not available"
    },
    "Price Position": {
        "lowest": "Lowest", "low": "Lowest",
        "competitive": "Competitive", "medium": "Competitive",
        "expensive": "Expensive", "high": "Expensive"
    }
}

ORDINAL_MAPPINGS = {
    "Account Engagement": {"High (Existing+Good)": 5, "Medium (Existing+Poor)": 3, "Low (New Account)": 0},
    "Client Relationship": {"Strong": 5, "Neutral": 3, "Weak": 0},
    "Deal Coach": {"Active & Available": 5, "Passive": 3, "Not Available": 0},
    "Bidder Rank": {"Top": 5, "Middle": 3, "Bottom": 0},
    "Incumbency Share": {"High (>50%)": 5, "Medium (20-50%)": 3, "Low (<20%)": 0, "None": 0},
    "References": {"Strong (Domain+Tech)": 5, "Average": 3, "Weak/None": 0},
    "Solution Strength": {"Strong (Covers all)": 5, "Average (Gaps)": 3, "Weak": 0},
    "Client Impression": {"Positive": 5, "Neutral": 3, "Negative": 0},
    "Orals Score": {"Strong": 5, "At Par": 3, "Weak": 0},
    "Price Alignment": {"On par with Client Budget": 5, "Above Client Budget with Rationale/Caveats": 3, "Above Client Budget": 0, "Client Budget Info not available": 2},
    "Price Position": {"Lowest": 5, "Competitive": 3, "Expensive": 0},
    "Current RFP Stage": {"Negotiation": 15, "Defence Cleared": 10, "Proposal Submitted": 5, "RFP Received": 0}
}

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
    warnings: List[str] = []

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
        raw_df = pd.read_excel(io.BytesIO(contents))
        
        # Load model and label encoder
        model = joblib.load(MODEL_PATH)
        le = joblib.load(encoder_path)
        
        validation_warnings = []
        
        # Load synthetic data to get expected column structure
        if not os.path.exists(SYNTHETIC_DATA_PATH):
            raise HTTPException(status_code=400, detail="Synthetic data not found. Please train the model first.")
        
        synthetic_df = pd.read_excel(SYNTHETIC_DATA_PATH)
        drop_cols = ["CRM ID", "Opportunity Name", "Account Name", "Detailed Remarks", "Deal Status", "Stage Description", "SST Sales Stage"]
        expected_cols = [c for c in synthetic_df.columns if c not in drop_cols]
        
        # 1. Normalize column names to strip spaces and handle casing variations
        raw_df.columns = raw_df.columns.astype(str).str.strip()
        
        standard_cols = [
            "SBU", "Account Name", "Opportunity Name", "SST Sales Stage", "Stage Description",
            "Type of Business", "Account Engagement", "Client Relationship", "Deal Coach",
            "References", "Solution Strength", "Client Impression", "Orals Score", "Price Alignment",
            "Expected TCV ($Mn)"
        ]
        
        # Create mapping from lowercase standard name to standard name
        standard_map = {col.lower(): col for col in standard_cols}
        standard_map["expected tcv ($mn) "] = "Expected TCV ($Mn)"
        standard_map["expected tcv"] = "Expected TCV ($Mn)"
        standard_map["sales description"] = "Stage Description"
        
        # Rename columns in raw_df that match standard columns case-insensitively
        new_columns = []
        for col in raw_df.columns:
            col_lower = col.lower()
            if col_lower in standard_map:
                new_columns.append(standard_map[col_lower])
            else:
                new_columns.append(col)
        raw_df.columns = new_columns
        
        tcv_col = "Expected TCV ($Mn)"
        
        # 2. Enforce all mandatory columns are present and not empty
        mandatory_cols = [
            "SBU", "Account Name", "Opportunity Name", "SST Sales Stage", "Stage Description",
            "Type of Business", "Account Engagement", "Client Relationship", "Deal Coach",
            "References", "Solution Strength", "Client Impression", "Orals Score", "Price Alignment",
            tcv_col
        ]
        
        # Check if any mandatory column is missing entirely
        missing_cols = [col for col in mandatory_cols if col not in raw_df.columns]
        if missing_cols:
            raise HTTPException(status_code=400, detail=f"Missing mandatory columns: {', '.join(missing_cols)}")
            
        # Check for empty cells in any of the mandatory columns (only for Active deals)
        raw_df["Stage Description"] = raw_df["Stage Description"].astype(str).str.strip()
        inactive_statuses = ["won", "lost", "aborted", "hold", "nan", "none", ""]
        active_mask = ~raw_df["Stage Description"].str.lower().isin(inactive_statuses)
        active_rows = raw_df[active_mask]
        
        for col in mandatory_cols:
            if col in raw_df.columns:
                empty_mask = active_rows[col].isna() | (active_rows[col].astype(str).str.strip().replace({'nan': '', 'None': '', 'NaN': '', 'none': '', 'null': '', 'NULL': ''}) == '')
                if empty_mask.any():
                    empty_indices = empty_mask[empty_mask].index.tolist()
                    row_numbers = [idx + 2 for idx in empty_indices[:5]] # +2 offset for excel 1-based index and header row
                    rows_str = ", ".join(map(str, row_numbers))
                    if len(empty_indices) > 5:
                        rows_str += "..."
                    validation_warnings.append(f"'{col}' Field empty at Excel row(s): {rows_str}. Enter Input")
        
        # Add missing columns with appropriate default values based on expected type
        expected_types = {}
        for col in expected_cols:
            expected_types[col] = synthetic_df[col].dtype
            
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
                    X_input[col] = pd.to_numeric(X_input[col], errors='coerce')
                else:
                    X_input[col] = X_input[col].astype(str)
        
        # Now identify numeric vs categorical based on actual dtypes
        numeric_cols = X_input.select_dtypes(include=['int64', 'float64']).columns.tolist()
        categorical_cols = X_input.select_dtypes(include=['object']).columns.tolist()
        
        # Clean categorical columns
        for col in categorical_cols:
            X_input[col] = X_input[col].str.strip()
            X_input[col] = X_input[col].replace({'nan': np.nan, 'None': np.nan, '': np.nan, 'NaN': np.nan})
            X_input[col] = X_input[col].fillna("UNKNOWN")
        
        # Apply normalization mapping
        for col, mapping in NORMALIZATION_MAP.items():
            if col in X_input.columns:
                def normalize_val(val):
                    if pd.isna(val): return val
                    s = str(val).lower().strip()
                    for key, target in mapping.items():
                        if key in s:
                             return target
                    return val
                X_input[col] = X_input[col].apply(normalize_val)
        
        # Impute numeric columns
        for col in numeric_cols:
            if X_input[col].isna().any():
                median_val = X_input[col].median()
                if pd.isna(median_val):
                    median_val = 0.0
                X_input[col] = X_input[col].fillna(median_val)
                
        # --- BUSINESS LOGIC: Explicit Ordinal Mapping ---
        # Map values to numbers for business logic calculations and predictions
        for col, mapping in ORDINAL_MAPPINGS.items():
            if col in X_input.columns:
                X_input[col] = pd.to_numeric(X_input[col].map(mapping).fillna(2), errors='coerce').fillna(2)
                
        # Determine Active vs Non-Active Deals based on Stage Description
        raw_df["Stage Description"] = raw_df["Stage Description"].astype(str).str.strip()
        inactive_statuses = ["won", "lost", "aborted", "hold", "nan", "none", ""]
        active_mask = ~raw_df["Stage Description"].str.lower().isin(inactive_statuses)
        non_active_mask = ~active_mask
        
        # Initialize output columns in result_df
        result_df = raw_df.copy()
        result_df["Predicted Deal Status"] = ""
        result_df["Business Logic Score"] = ""
        result_df["Business Logic Status"] = ""
        result_df["Win Probability"] = ""
        
        for class_name in le.classes_:
            result_df[f"Probability_{class_name}"] = ""
            
        def calculate_business_score(row):
            score = 0
            score += {5: 10, 3: 5, 2: 2, 0: 0}.get(row.get("Account Engagement", 0), 0)
            score += {5: 10, 3: 5, 2: 2, 0: 0}.get(row.get("Client Relationship", 0), 0)
            score += {5: 10, 3: 5, 2: 2, 0: 0}.get(row.get("Deal Coach", 0), 0)
            score += {5: 15, 3: 5, 2: 2, 0: 0}.get(row.get("Bidder Rank", 0), 0)
            score += {5: 10, 3: 5, 2: 2, 0: 0}.get(row.get("Incumbency Share", 0), 0)
            score += {5: 7, 3: 3, 2: 1, 0: 0}.get(row.get("References", 0), 0)
            score += {5: 7, 3: 3, 2: 1, 0: 0}.get(row.get("Solution Strength", 0), 0)
            score += {5: 6, 3: 3, 2: 1, 0: 0}.get(row.get("Client Impression", 0), 0)
            score += {5: 15, 3: 8, 2: 4, 0: 0}.get(row.get("Orals Score", 0), 0)
            score += {5: 5, 3: 3, 2: 2, 0: 0}.get(row.get("Price Alignment", 0), 0)
            score += {5: 5, 3: 2, 0: 0}.get(row.get("Price Position", 0), 0)
            return score
            
        def get_logic_status(score):
            if score >= 60: return "Won"
            if score <= 40: return "Lost"
            return "Aborted/Risk"
            
        def get_prob_category(p):
            pct = round(p * 100)
            if pct > 80: return "Very High"
            elif pct >= 61: return "High"
            elif pct >= 41: return "Medium"
            else: return "Low"
            
        # Process Active Deals
        if active_mask.any():
            X_input_active = X_input[active_mask].copy()
            X_input_active.columns = X_input_active.columns.astype(str)
            
            # Predict using model
            pred_numeric_active = model.predict(X_input_active)
            pred_labels_active = le.inverse_transform(pred_numeric_active)
            pred_probs_active = model.predict_proba(X_input_active)
            
            # Business logic score
            active_business_scores = X_input_active.apply(calculate_business_score, axis=1)
            
            result_df.loc[active_mask, "Business Logic Status"] = active_business_scores.apply(get_logic_status)
            result_df.loc[active_mask, "Business Logic Score"] = [f"{int(s)}%" for s in active_business_scores]
            
            # Override Predicted Deal Status and Win Probability based on Business Logic Score to align ML output with business rules
            result_df.loc[active_mask, "Predicted Deal Status"] = result_df.loc[active_mask, "Business Logic Status"]
            result_df.loc[active_mask, "Win Probability"] = [get_prob_category(score / 100.0) for score in active_business_scores]
            
            for idx, class_name in enumerate(le.classes_):
                result_df.loc[active_mask, f"Probability_{class_name}"] = [
                    f"{round(p * 100)}%" for p in pred_probs_active[:, idx]
                ]
                
        # Process Non-Active Deals
        if non_active_mask.any():
            clean_statuses = raw_df.loc[non_active_mask, "Stage Description"].str.strip()
            result_df.loc[non_active_mask, "Predicted Deal Status"] = clean_statuses
            result_df.loc[non_active_mask, "Business Logic Status"] = clean_statuses
            result_df.loc[non_active_mask, "Business Logic Score"] = "N/A"
            result_df.loc[non_active_mask, "Win Probability"] = "N/A"
            
            for class_name in le.classes_:
                result_df.loc[non_active_mask, f"Probability_{class_name}"] = "N/A"
                
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
            total_records=len(result_df),
            warnings=validation_warnings
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
