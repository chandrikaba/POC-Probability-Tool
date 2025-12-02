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
model = joblib.load(model_path)
le = joblib.load(encoder_path)

# Skip the first row as requested by user (likely a title row)
raw_df = pd.read_excel(input_path, skiprows=1)

# ---------------------------------------------------------------------------
# Pre-processing – prepare features similar to training
# ---------------------------------------------------------------------------
SYNTHETIC_DATA_PATH = os.path.join(project_root, "data", "output", "synthetic_deals.xlsx")

# Load synthetic data to get expected column structure
if not os.path.exists(SYNTHETIC_DATA_PATH):
    raise FileNotFoundError(f"Synthetic data not found at {SYNTHETIC_DATA_PATH}. Please train the model first.")

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

# Drop identifier and long-text columns from features (same as training)
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




