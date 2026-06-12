# src/predict_xgb_classifier.py
"""
Predict the deal outcome using the XGBoost classifier trained on the synthetic data.

The script expects an input Excel file named **Data-Input.xlsx** located in the
`data/input` directory. It loads the saved model (`models/xgb_classifier.pkl`),
applies the same preprocessing steps used during training (one‑hot encoding
and column alignment), and writes the predictions to
`data/output/predictions.xlsx`.

Requirements
------------
- pandas
- scikit‑learn
- xgboost
- joblib

Usage
-----
```bash
python src/predict_xgb_classifier.py
```
"""

import os
import pandas as pd
import numpy as np
import joblib

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
model_path   = os.path.join(project_root, "models", "xgb_classifier.pkl")
encoder_path = os.path.join(project_root, "models", "label_encoder.pkl")
input_path   = os.path.join(project_root, "data", "input", "Data-Input.xlsx")
output_path  = os.path.join(project_root, "data", "output", "predictions.xlsx")

if not os.path.exists(model_path):
    raise FileNotFoundError(f"Trained model not found at {model_path}")
if not os.path.exists(encoder_path):
    raise FileNotFoundError(f"Label encoder not found at {encoder_path}")
if not os.path.exists(input_path):
    raise FileNotFoundError(f"Input file not found at {input_path}")

# ---------------------------------------------------------------------------
# Load model, encoder and data
# ---------------------------------------------------------------------------
import traceback

try:
    # ---------------------------------------------------------------------------
    # Load model, encoder and data
    # ---------------------------------------------------------------------------
    model = joblib.load(model_path)
    le = joblib.load(encoder_path)

    # Load data without skipping rows (assuming headers are in the first row as in generation script)
    raw_df = pd.read_excel(input_path)

    # ---------------------------------------------------------------------------
    # Pre-processing – prepare features similar to training
    # ---------------------------------------------------------------------------
    # Find the latest synthetic data file to use as schema template
    output_dir = os.path.join(project_root, "data", "output")
    files = [f for f in os.listdir(output_dir) if f.startswith("synthetic_data") and f.endswith(".xlsx") and not f.startswith("~$")]
    files.sort(key=lambda x: os.path.getmtime(os.path.join(output_dir, x)), reverse=True)

    if not files:
        raise FileNotFoundError("No synthetic data found to use as schema template. Please train the model first.")

    SYNTHETIC_DATA_PATH = os.path.join(output_dir, files[0])
    print(f"Using schema from: {SYNTHETIC_DATA_PATH}")

    synthetic_df = pd.read_excel(SYNTHETIC_DATA_PATH)
    
    # Define columns to drop (must match training script + outcome variables)
    drop_cols = [
        "CRM ID", "Opportunity Name", "Account Name", "Detailed Remarks", "Deal Status",
        "Calculated Score",
        "Primary L1", "Primary L2", "Secondary L1", "Secondary L2", "Tertiary L1", "Tertiary L2"
    ]
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

    # Drop identifier and long-text columns from features (same as training)
    X_input = raw_df.drop(columns=[c for c in drop_cols if c in raw_df.columns], errors="ignore").copy()

    # Convert columns to match expected types from training
    # Convert columns to match expected types from training
    for col in X_input.columns:
        if col in expected_types:
            if expected_types[col] in ['int64', 'float64']:
                # This should be numeric
                X_input[col] = pd.to_numeric(X_input[col], errors='coerce')
            else:
                # This should be categorical
                X_input[col] = X_input[col].astype(str).str.strip().replace({'nan': np.nan, 'None': np.nan, '': np.nan, 'NaN': np.nan})

    # --- Data Cleaning & Normalization ---
    # Map shorthand/variant inputs to model categories
    normalization_map = {
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
        "Incumbency Share": {
            "high": "High (>50%)", ">50%": "High (>50%)",
            "medium": "Medium (20-50%)", "20-50%": "Medium (20-50%)",
            "low": "Low (<20%)", "<20%": "Low (<20%)", "none": "None"
        },
        "Bidder Rank": {
            "1": "Top", "top": "Top", "first": "Top",
            "2": "Middle", "middle": "Middle", "second": "Middle",
            "3": "Bottom", "bottom": "Bottom", "last": "Bottom"
        },
        "Price Alignment": {
            "high": "Aligned", "standard": "Aligned", "aligned": "Aligned",
            "low": "Deviating", "deviating": "Deviating", "bad": "Deviating"
        },
        "Solution Strength": {
            "high": "Strong (Covers all)", "strong": "Strong (Covers all)",
            "medium": "Average (Gaps)", "average": "Average (Gaps)",
            "low": "Weak", "weak": "Weak"
        }
    }

    for col, mapping in normalization_map.items():
        if col in X_input.columns:
            # Normalize to lowercase for matching, then map
            def normalize_val(val):
                if pd.isna(val): return val
                s = str(val).lower().strip()
                for key, target in mapping.items():
                    if key in s: # simple substring match
                         return target
                return val # Return original if no match
            
            X_input[col] = X_input[col].apply(normalize_val)

    # --- BUSINESS LOGIC: Explicit Ordinal Mapping (Must align with training) ---
    ordinal_mappings = {
        "Account Engagement": {"High (Existing+Good)": 5, "Medium (Existing+Poor)": 3, "Low (New Account)": 0},
        "Client Relationship": {"Strong": 5, "Neutral": 3, "Weak": 0},
        "Deal Coach": {"Active & Available": 5, "Passive": 3, "Not Available": 0},
        "Bidder Rank": {"Top": 5, "Middle": 3, "Bottom": 0},
        "Incumbency Share": {"High (>50%)": 5, "Medium (20-50%)": 3, "Low (<20%)": 0, "None": 0},
        "References": {"Strong (Domain+Tech)": 5, "Average": 3, "Weak/None": 0},
        "Solution Strength": {"Strong (Covers all)": 5, "Average (Gaps)": 3, "Weak": 0},
        "Client Impression": {"Positive": 5, "Neutral": 3, "Negative": 0},
        "Orals Score": {"Strong": 5, "At Par": 3, "Weak": 0},
        "Price Alignment": {"Aligned": 5, "Deviating": 0, "No Intel": 2},
        "Price Position": {"Lowest": 5, "Competitive": 3, "Expensive": 0}
    }

    # Apply mappings
    for col, mapping in ordinal_mappings.items():
        if col in X_input.columns:
            # Map values, fill unknown with 2 (Neutral)
            # Force numeric conversion so dtype becomes int/float instead of object
            X_input[col] = pd.to_numeric(X_input[col].map(mapping).fillna(2), errors='coerce').fillna(2)

    # Now identify numeric vs categorical based on actual dtypes
    numeric_cols = X_input.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = X_input.select_dtypes(include=['object']).columns.tolist()

    # DEBUG: Check against model expectations
    try:
        preprocessor = model.named_steps['prep']
        
        # 1. Check Numeric Columns
        num_trans = [t for t in preprocessor.transformers_ if t[0] == 'num'][0]
        model_num_cols = num_trans[2]
        
        # 2. Check One-Hot Categorical Columns
        cat_trans = [t for t in preprocessor.transformers_ if t[0] == 'onehot'][0]
        model_cat_cols = cat_trans[2]
        
        all_model_cols = list(model_num_cols) + list(model_cat_cols)
        
        print("\n--- DEBUG: Checking Input Data Quality ---")
        missing_cols = [c for c in all_model_cols if c not in X_input.columns]
        if missing_cols:
            print(f"❌ CRITICAL ERROR: The following columns are MISSING from the input file:\n   {missing_cols}")
            print("   (These will be treated as 0 or UNKNOWN, heavily penalizing the score!)")
        
        # Check specific values
        print("\n--- Checking Key Feature Values ---")
        for col in all_model_cols:
            if col in X_input.columns:
                val = X_input[col].iloc[0]
                if pd.isna(val) or val == "pd.nan" or val == "nan" or str(val).strip() == "":
                    print(f"⚠️  WARNING: Column '{col}' is EMPTY/NaN. (Will be treated as lowest score)")
                elif str(val) == "UNKNOWN":
                     print(f"⚠️  WARNING: Column '{col}' is marked UNKNOWN.")
    except Exception as e:
        print(f"Debug check failed: {e}")
        traceback.print_exc()

    # Clean remaining categorical columns
    for col in categorical_cols:
        X_input[col] = X_input[col].str.strip()
        X_input[col] = X_input[col].fillna("UNKNOWN")

    # Impute numeric columns
    for col in numeric_cols:
        if X_input[col].isna().any():
            median_val = X_input[col].median()
            if pd.isna(median_val):
                median_val = 0.0
            X_input[col] = X_input[col].fillna(median_val)

    # ---------------------------------------------------------------------------
    # Prediction
    # ---------------------------------------------------------------------------
    # The pipeline handles preprocessing automatically
    pred_numeric = model.predict(X_input)

    # Convert numeric labels back to original string labels
    pred_labels = le.inverse_transform(pred_numeric)

    # Get prediction probabilities
    pred_probs = model.predict_proba(X_input)

    # Append predictions to the original dataframe for easy reference
    result_df = raw_df.copy()
    result_df["Predicted Deal Status"] = pred_labels

    # Add probability columns for each class
    for idx, class_name in enumerate(le.classes_):
        result_df[f"Probability_{class_name}"] = pred_probs[:, idx]

    # Remove 'Deal Status' column from output if it exists
    if "Deal Status" in result_df.columns:
        result_df = result_df.drop(columns=["Deal Status"])

    # ---------------------------------------------------------------------------
    # Save predictions
    # ---------------------------------------------------------------------------
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        result_df.to_excel(output_path, index=False)
        print(f"Predictions written to {output_path}")
        print(f"Total records processed: {len(result_df)}")
        print(f"Prediction distribution:")
        for class_name in le.classes_:
            count = (pred_labels == class_name).sum()
            print(f"  {class_name}: {count} ({count/len(pred_labels)*100:.1f}%)")
    except PermissionError:
        print(f"⚠️ Could not write to {output_path} (File might be open).")
        # Try a fallback name
        import time
        timestamp = int(time.time())
        fallback_path = output_path.replace(".xlsx", f"_{timestamp}.xlsx")
        result_df.to_excel(fallback_path, index=False)
        print(f"Predictions written to {fallback_path}")

except Exception as e:
    traceback.print_exc()





