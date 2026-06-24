"""
Streamlit UI for Deal Win Probability Prediction Tool

A modern, interactive web interface for generating synthetic data,
training models, and predicting deal outcomes.
"""

import streamlit as st
import pandas as pd
import os
import sys
import subprocess
import joblib
from datetime import datetime
import io
import re
import numpy as np
from sklearn.preprocessing import LabelEncoder

import plotly.express as px

def get_deal_score_breakdown(row):
    # Map row values using ordinal_mappings if they are text
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
        "Price Alignment": {"On par with Client Budget": 5, "Above Client Budget with Rationale/Caveats": 3, "Above Client Budget": 0, "Client Budget Info not available": 2},
        "Price Position": {"Lowest": 5, "Competitive": 3, "Expensive": 0},
        "Current RFP Stage": {"Negotiation": 15, "Defence Cleared": 10, "Proposal Submitted": 5, "RFP Received": 0}
    }
    
    # We need to get the mapped value (numeric) for each attribute in the row
    def get_mapped_val(col, default_val=2):
        val = row.get(col)
        if pd.isna(val):
            return default_val
        if isinstance(val, (int, float, np.integer, np.floating)):
            return float(val)
        val_str = str(val).strip()
        # Look up in normalization maps if needed, or direct mapping
        # First check direct mapping
        mapping = ordinal_mappings.get(col, {})
        if val_str in mapping:
            return mapping[val_str]
        # Check substring match
        for k, v in mapping.items():
            if k.lower() in val_str.lower() or val_str.lower() in k.lower():
                return v
        return default_val

    # Get scores for each field
    eng_val = row.get("Account Engagement", "Unknown")
    eng_pts = {5: 10, 3: 5, 2: 2, 0: 0}.get(get_mapped_val("Account Engagement"), 0)
    
    rel_val = row.get("Client Relationship", "Unknown")
    rel_pts = {5: 10, 3: 5, 2: 2, 0: 0}.get(get_mapped_val("Client Relationship"), 0)
    
    coach_val = row.get("Deal Coach", "Unknown")
    coach_pts = {5: 10, 3: 5, 2: 2, 0: 0}.get(get_mapped_val("Deal Coach"), 0)
    
    rank_val = row.get("Bidder Rank", "Unknown")
    rank_pts = {5: 15, 3: 5, 2: 2, 0: 0}.get(get_mapped_val("Bidder Rank"), 0)
    
    inc_val = row.get("Incumbency Share", "Unknown")
    inc_pts = {5: 10, 3: 5, 2: 2, 0: 0}.get(get_mapped_val("Incumbency Share"), 0)
    
    ref_val = row.get("References", "Unknown")
    ref_pts = {5: 7, 3: 3, 2: 1, 0: 0}.get(get_mapped_val("References"), 0)
    
    sol_val = row.get("Solution Strength", "Unknown")
    sol_pts = {5: 7, 3: 3, 2: 1, 0: 0}.get(get_mapped_val("Solution Strength"), 0)
    
    imp_val = row.get("Client Impression", "Unknown")
    imp_pts = {5: 6, 3: 3, 2: 1, 0: 0}.get(get_mapped_val("Client Impression"), 0)
    
    orals_val = row.get("Orals Score", "Unknown")
    orals_pts = {5: 15, 3: 8, 2: 4, 0: 0}.get(get_mapped_val("Orals Score"), 0)
    
    pa_val = row.get("Price Alignment", "Unknown")
    pa_pts = {5: 5, 0: 2, 2: 0}.get(get_mapped_val("Price Alignment", 2), 0)
    
    pp_val = row.get("Price Position", "Unknown")
    pp_pts = {5: 5, 3: 2, 0: 0}.get(get_mapped_val("Price Position"), 0)
    
    # Calculate group totals
    relationship_score = eng_pts + rel_pts + coach_pts
    competition_score = rank_pts + inc_pts
    solution_score = ref_pts + sol_pts + imp_pts
    orals_score = orals_pts
    price_score = pa_pts + pp_pts
    
    total = relationship_score + competition_score + solution_score + orals_score + price_score
    
    return {
        "groups": {
            "Relationship": {
                "score": relationship_score,
                "max": 30,
                "details": [
                    {"parameter": "Account Engagement", "value": eng_val, "points": eng_pts, "max_pts": 10},
                    {"parameter": "Client Relationship", "value": rel_val, "points": rel_pts, "max_pts": 10},
                    {"parameter": "Deal Coach", "value": coach_val, "points": coach_pts, "max_pts": 10}
                ]
            },
            "Competition": {
                "score": competition_score,
                "max": 25,
                "details": [
                    {"parameter": "Bidder Rank", "value": rank_val, "points": rank_pts, "max_pts": 15},
                    {"parameter": "Incumbency Share", "value": inc_val, "points": inc_pts, "max_pts": 10}
                ]
            },
            "Solution": {
                "score": solution_score,
                "max": 20,
                "details": [
                    {"parameter": "References", "value": ref_val, "points": ref_pts, "max_pts": 7},
                    {"parameter": "Solution Strength", "value": sol_val, "points": sol_pts, "max_pts": 7},
                    {"parameter": "Client Impression", "value": imp_val, "points": imp_pts, "max_pts": 6}
                ]
            },
            "Orals": {
                "score": orals_score,
                "max": 15,
                "details": [
                    {"parameter": "Orals Score", "value": orals_val, "points": orals_pts, "max_pts": 15}
                ]
            },
            "Price": {
                "score": price_score,
                "max": 10,
                "details": [
                    {"parameter": "Price Alignment", "value": pa_val, "points": pa_pts, "max_pts": 5},
                    {"parameter": "Price Position", "value": pp_val, "points": pp_pts, "max_pts": 5}
                ]
            }
        },
        "total": total
    }

# Page configuration
st.set_page_config(
    page_title="Deal Win Probability Tool",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 0.5rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Project paths
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "xgb_classifier.pkl")
SYNTHETIC_DATA_PATH = os.path.join(PROJECT_ROOT, "data", "output", "synthetic_data_v3.xlsx")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data", "output")

# Initialize session state
if 'model_trained' not in st.session_state:
    st.session_state.model_trained = os.path.exists(MODEL_PATH)
if 'synthetic_data_generated' not in st.session_state:
    st.session_state.synthetic_data_generated = os.path.exists(SYNTHETIC_DATA_PATH)
if 'last_prediction_file' not in st.session_state:
    st.session_state.last_prediction_file = None

# Header
st.markdown('<div class="main-header">📊 Deal Win Probability Prediction Tool</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/300x100/1f77b4/ffffff?text=Deal+Win+AI", use_container_width=True)
    st.markdown("### 🎯 Navigation")
    
    # Developer Mode Toggle
    show_dev = st.checkbox("Show Developer Options", value=False)
    
    # Navigation Options
    nav_options = ["🏠 Home", "🔮 Predictions", "📈 Audit Trail", "ℹ️ About"]
    if show_dev:
        nav_options.insert(1, "📁 Data Generation")
        nav_options.insert(2, "🤖 Model Training")
    
    page = st.radio(
        "Select a page:",
        nav_options,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### 📊 System Status")
    
    # Status indicators
    if st.session_state.synthetic_data_generated:
        st.success("✅ Synthetic Data Ready")
    else:
        st.warning("⚠️ No Synthetic Data")
    
    if st.session_state.model_trained:
        st.success("✅ Model Trained")
        if os.path.exists(MODEL_PATH):
            model_size = os.path.getsize(MODEL_PATH) / (1024 * 1024)
            st.caption(f"Model Size: {model_size:.2f} MB")
    else:
        st.warning("⚠️ Model Not Trained")

# Home Page
if page == "🏠 Home":
    st.markdown('<div class="section-header">Welcome to the Deal Win Probability Tool</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>📁 Step 1: Generate Data</h3>
            <p>Create synthetic training data with realistic deal scenarios and outcomes.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🤖 Step 2: Train Model</h3>
            <p>Train an XGBoost classifier on the synthetic data to learn patterns.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>🔮 Step 3: Predict</h3>
            <p>Upload your deal data and get instant win probability predictions.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick Stats
    st.markdown('<div class="section-header">Quick Statistics</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.session_state.synthetic_data_generated:
            df = pd.read_excel(SYNTHETIC_DATA_PATH)
            st.metric("Training Records", len(df))
        else:
            st.metric("Training Records", "N/A")
    
    with col2:
        st.metric("Model Type", "XGBoost")
    
    with col3:
        if st.session_state.model_trained:
            st.metric("Model Status", "Ready")
        else:
            st.metric("Model Status", "Not Trained")
    
    with col4:
        output_files = len([f for f in os.listdir(OUTPUT_DIR) if f.startswith("predictions_")]) if os.path.exists(OUTPUT_DIR) else 0
        st.metric("Predictions Made", output_files)

# Data Generation Page
elif page == "📁 Data Generation":
    st.markdown('<div class="section-header">Generate Synthetic Training Data</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
    This tool generates synthetic deal data with realistic patterns including:
    <ul>
        <li>Deal characteristics (SBU, TCV, Deal Size)</li>
        <li>Primary, Secondary, and Tertiary factors (L1/L2 tags)</li>
        <li>Deal outcomes (Won, Lost, Aborted)</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        num_records = st.slider("Number of records to generate:", 10, 1000, 1000)
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        generate_btn = st.button("🚀 Generate Synthetic Data", type="primary", use_container_width=True)
    
    if generate_btn:
        with st.spinner("Generating synthetic data..."):
            try:
                script_path = os.path.join(PROJECT_ROOT, "src", "generate_synthetic_data.py")
                result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
                
                if result.returncode == 0:
                    st.session_state.synthetic_data_generated = True
                    df = pd.read_excel(SYNTHETIC_DATA_PATH)
                    
                    st.markdown(f"""
                    <div class="success-box">
                        ✅ Successfully generated {len(df)} synthetic records!
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Show preview
                    st.markdown("### 📊 Data Preview")
                    st.dataframe(df.head(10), use_container_width=True)
                    
                    # Show statistics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Records", len(df))
                    with col2:
                        won_count = len(df[df['Deal Status'] == 'Won'])
                        st.metric("Won Deals", won_count)
                    with col3:
                        lost_count = len(df[df['Deal Status'] == 'Lost'])
                        st.metric("Lost Deals", lost_count)
                else:
                    st.markdown(f"""
                    <div class="error-box">
                        ❌ Error generating data: {result.stderr}
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f"""
                <div class="error-box">
                    ❌ Error: {str(e)}
                </div>
                """, unsafe_allow_html=True)
    
    # Show existing data if available
    if st.session_state.synthetic_data_generated and not generate_btn:
        st.markdown("### 📊 Current Synthetic Data")
        df = pd.read_excel(SYNTHETIC_DATA_PATH)
        st.dataframe(df, use_container_width=True)
        
        # Download button
        buffer = io.BytesIO()
        df.to_excel(buffer, index=False)
        buffer.seek(0)
        st.download_button(
            label="📥 Download Synthetic Data",
            data=buffer,
            file_name="synthetic_deals.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# Model Training Page
elif page == "🤖 Model Training":
    st.markdown('<div class="section-header">Train XGBoost Classifier</div>', unsafe_allow_html=True)
    
    if not st.session_state.synthetic_data_generated:
        st.markdown("""
        <div class="error-box">
            ⚠️ Please generate synthetic data first before training the model.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="info-box">
        The XGBoost classifier will be trained on the synthetic data to predict deal outcomes.
        Training typically takes 10-30 seconds depending on data size.
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        
        with col2:
            train_btn = st.button("🎯 Train Model", type="primary", use_container_width=True)
        
        if train_btn:
            with st.spinner("Training model... This may take a moment."):
                try:
                    script_path = os.path.join(PROJECT_ROOT, "src", "train_xgb_classifier.py")
                    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        st.session_state.model_trained = True
                        
                        # Try to extract accuracy from output
                        accuracy = "N/A"
                        # Look for "Accuracy :" in the output
                        if "Accuracy :" in result.stdout:
                            try:
                                # Get all lines with accuracy
                                accuracy_lines = [line for line in result.stdout.split('\n') if 'Accuracy :' in line]
                                if accuracy_lines:
                                    # Take the last one (final accuracy)
                                    accuracy_line = accuracy_lines[-1]
                                    # Format is "Accuracy : 0.85" or similar
                                    accuracy = accuracy_line.split(':')[1].strip()
                                    # Convert to percentage
                                    acc_val = float(accuracy)
                                    accuracy = f"{acc_val:.2%}"
                            except:
                                pass
                        
                        st.markdown(f"""
                        <div class="success-box">
                            ✅ Model trained successfully!<br>
                            Validation Accuracy: {accuracy}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Show model info
                        if os.path.exists(MODEL_PATH):
                            model_size = os.path.getsize(MODEL_PATH) / (1024 * 1024)
                            st.metric("Model Size", f"{model_size:.2f} MB")
                    else:
                        st.markdown(f"""
                        <div class="error-box">
                            ❌ Training failed: {result.stderr}
                        </div>
                        """, unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f"""
                    <div class="error-box">
                        ❌ Error: {str(e)}
                    </div>
                    """, unsafe_allow_html=True)
        
        # Show model info if already trained
        if st.session_state.model_trained and not train_btn:
            st.markdown("### 📊 Model Information")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Model Type", "XGBoost Classifier")
            
            with col2:
                if os.path.exists(MODEL_PATH):
                    model_size = os.path.getsize(MODEL_PATH) / (1024 * 1024)
                    st.metric("Model Size", f"{model_size:.2f} MB")
            
            with col3:
                if os.path.exists(MODEL_PATH):
                    mod_time = datetime.fromtimestamp(os.path.getmtime(MODEL_PATH))
                    st.metric("Last Trained", mod_time.strftime("%Y-%m-%d %H:%M"))

# Predictions Page
elif page == "🔮 Predictions":
    st.markdown('<div class="section-header">Predict Deal Outcomes</div>', unsafe_allow_html=True)
    
    # Check if we need to display deal calculation details
    if "show_calc" in st.query_params:
        crm_id = st.query_params["show_calc"]
        selected_deal = None
        
        # 1. Check if we have predicted_df in session state
        if 'predicted_df' in st.session_state and st.session_state.predicted_df is not None:
            df_to_search = st.session_state.predicted_df
            match = df_to_search[df_to_search['CRM ID'].astype(str).str.strip() == str(crm_id).strip()]
            if not match.empty:
                selected_deal = match.iloc[0]
                
        # 2. Fallback: check last prediction file
        if selected_deal is None and st.session_state.last_prediction_file and os.path.exists(st.session_state.last_prediction_file):
            try:
                df_latest = pd.read_excel(st.session_state.last_prediction_file)
                match = df_latest[df_latest['CRM ID'].astype(str).str.strip() == str(crm_id).strip()]
                if not match.empty:
                    selected_deal = match.iloc[0]
            except Exception:
                pass
                
        # 3. Fallback: scan prediction files in output directory
        if selected_deal is None and os.path.exists(OUTPUT_DIR):
            pred_files = [f for f in os.listdir(OUTPUT_DIR) if f.startswith("predictions_") and f.endswith(".xlsx")]
            pred_files.sort(reverse=True)
            for file in pred_files[:5]:
                try:
                    df_latest = pd.read_excel(os.path.join(OUTPUT_DIR, file))
                    match = df_latest[df_latest['CRM ID'].astype(str).str.strip() == str(crm_id).strip()]
                    if not match.empty:
                        selected_deal = match.iloc[0]
                        break
                except Exception:
                    pass
                    
        if selected_deal is not None:
            breakdown = get_deal_score_breakdown(selected_deal)
            
            with st.container(border=True):
                st.markdown(f"### 🔍 Score Calculation Breakdown for CRM ID: **{crm_id}**")
                
                # Setup side-by-side Close button and summary
                col_txt, col_btn = st.columns([6, 1])
                with col_txt:
                    st.write(f"**Account Name:** {selected_deal.get('Account Name', 'N/A')} | **Opportunity Name:** {selected_deal.get('Opportunity Name', 'N/A')}")
                with col_btn:
                    if st.button("✖ Close", type="secondary", use_container_width=True):
                        st.query_params.clear()
                        st.rerun()
                
                # Metric cards
                cols = st.columns(5)
                group_colors = {
                    "Relationship": "#1f77b4",
                    "Competition": "#ff7f0e",
                    "Solution": "#2ca02c",
                    "Orals": "#d62728",
                    "Price": "#9467bd"
                }
                for i, (g_name, g_data) in enumerate(breakdown["groups"].items()):
                    with cols[i]:
                        pct = (g_data['score'] / g_data['max']) * 100
                        st.markdown(f"""
                        <div style="background-color:#f8f9fa; padding:12px; border-radius:5px; border-left: 5px solid {group_colors[g_name]}; margin-bottom: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                            <span style="font-size:12px; color:#555; font-weight:bold;">{g_name} (Max {g_data['max']})</span><br>
                            <span style="font-size:22px; font-weight:bold; color:{group_colors[g_name]};">{g_data['score']} pts</span><br>
                            <span style="font-size:12px; color:#888;">{pct:.0f}% of Max</span>
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown(f"### **Total Business Logic Score: {breakdown['total']}%**")
                
                # Detailed breakdown table
                table_rows = []
                for g_name, g_data in breakdown["groups"].items():
                    for d in g_data["details"]:
                        table_rows.append({
                            "Category Group": g_name,
                            "Factor/Parameter": d["parameter"],
                            "Value Entered": d["value"],
                            "Points Awarded": d["points"],
                            "Max Points Possible": d["max_pts"]
                        })
                st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)
                st.markdown("---")
        else:
            st.warning(f"Could not find calculation details for CRM ID: {crm_id}. Please run the prediction first.")
    
    if not st.session_state.model_trained:
        st.markdown("""
        <div class="error-box">
            ⚠️ Please train the model first before making predictions.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="info-box">
        Upload an Excel file with deal data to get instant predictions.
        The file should have the same structure as the training data.
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose an Excel file",
            type=['xlsx', 'xls'],
            help="Upload your deal data in Excel format"
        )
        
        if uploaded_file is not None:
            try:
                # Read the uploaded file
                raw_df = pd.read_excel(uploaded_file)
                
                st.markdown("### 📊 Input Data Preview")
                st.dataframe(raw_df.head(10), use_container_width=True)
                st.caption(f"Total records: {len(raw_df)}")
                
                predict_btn = st.button("🔮 Generate Predictions", type="primary", use_container_width=True)
                
                if predict_btn:
                    import numpy as np
                    
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
                        st.error(f"Exception Error - Missing mandatory columns in the uploaded file: {', '.join(missing_cols)}. Please check the input file.")
                        st.stop()
                        
                    # Check for empty cells in any of the mandatory columns (only for Active deals)
                    raw_df["Stage Description"] = raw_df["Stage Description"].astype(str).str.strip()
                    active_rows = raw_df[raw_df["Stage Description"].str.lower() == "active"]
                    
                    validation_warnings = []
                    for col in mandatory_cols:
                        if col in raw_df.columns:
                            empty_mask = active_rows[col].isna() | (active_rows[col].astype(str).str.strip().replace({'nan': '', 'None': '', 'NaN': '', 'none': '', 'null': '', 'NULL': ''}) == '')
                            if empty_mask.any():
                                empty_indices = empty_mask[empty_mask].index.tolist()
                                # Get row numbers matching the original raw_df indices
                                row_numbers = [idx + 2 for idx in empty_indices[:5]] # +2 offset for excel 1-based index and header row
                                rows_str = ", ".join(map(str, row_numbers))
                                if len(empty_indices) > 5:
                                    rows_str += "..."
                                validation_warnings.append(f"'{col}' Field empty at Excel row(s): {rows_str}. Enter Input")
                                
                    if validation_warnings:
                        warnings_text = "\n".join([f"- {w}" for w in validation_warnings])
                        st.warning(f"⚠️ **Validation Warning:** Some mandatory fields are empty. Using default/neutral assumptions to proceed:\n\n{warnings_text}")
                            
                    with st.spinner("Generating predictions..."):
                        try:
                            # Load model and label encoder
                            model = joblib.load(MODEL_PATH)
                            encoder_path = os.path.join(PROJECT_ROOT, "models", "label_encoder.pkl")
                            le = joblib.load(encoder_path)
                            
                            # Load synthetic data to get expected column structure
                            if not os.path.exists(SYNTHETIC_DATA_PATH):
                                st.error("Synthetic data not found. Please generate and train the model first.")
                                st.stop()
                            
                            synthetic_df = pd.read_excel(SYNTHETIC_DATA_PATH)
                            drop_cols = ["CRM ID", "Opportunity Name", "Account Name", "Detailed Remarks", "Deal Status", "Stage Description", "SST Sales Stage"]
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
                            
                            # --- Data Cleaning & Normalization (MATCHING TRAINING SCRIPT) ---
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
                                    "on par": "On par with Client Budget", "budget": "On par with Client Budget", "aligned": "On par with Client Budget",
                                    "caveats": "Above Client Budget with Rationale/Caveats", "rationale": "Above Client Budget with Rationale/Caveats",
                                    "above": "Above Client Budget", "deviating": "Above Client Budget",
                                    "info not available": "Client Budget Info not available", "no intel": "Client Budget Info not available"
                                },
                                "Solution Strength": {
                                    "high": "Strong (Covers all)", "strong": "Strong (Covers all)",
                                    "medium": "Average (Gaps)", "average": "Average (Gaps)",
                                    "low": "Weak", "weak": "Weak"
                                }
                            }
                            
                            for col, mapping in normalization_map.items():
                                if col in X_input.columns:
                                    def normalize_val(val):
                                        if pd.isna(val): return val
                                        s = str(val).lower().strip()
                                        for key, target in mapping.items():
                                            if key in s:
                                                 return target
                                        return val
                                    X_input[col] = X_input[col].apply(normalize_val)
                            
                            # Identify numeric vs categorical
                            numeric_cols = X_input.select_dtypes(include=['int64', 'float64']).columns.tolist()
                            categorical_cols = X_input.select_dtypes(include=['object']).columns.tolist()
                            
                            # --- BUSINESS LOGIC: Explicit Ordinal Mapping ---
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
                                "Price Alignment": {"On par with Client Budget": 5, "Above Client Budget with Rationale/Caveats": 3, "Above Client Budget": 0, "Client Budget Info not available": 2},
                                "Price Position": {"Lowest": 5, "Competitive": 3, "Expensive": 0},
                                "Current RFP Stage": {"Negotiation": 15, "Defence Cleared": 10, "Proposal Submitted": 5, "RFP Received": 0}
                            }
                            
                            for col, mapping in ordinal_mappings.items():
                                if col in X_input.columns:
                                    X_input[col] = pd.to_numeric(X_input[col].map(mapping).fillna(2), errors='coerce').fillna(2)
                                    if col in categorical_cols: categorical_cols.remove(col)
                                    if col not in numeric_cols: numeric_cols.append(col)
                                    
                            for col in categorical_cols:
                                X_input[col] = X_input[col].fillna("UNKNOWN")
                                
                            for col in numeric_cols:
                                if X_input[col].isna().any():
                                    median_val = X_input[col].median()
                                    if pd.isna(median_val):
                                        median_val = 0.0
                                    X_input[col] = X_input[col].fillna(median_val)
                                    
                            # Determine Active vs Non-Active Deals based on Stage Description
                            raw_df["Stage Description"] = raw_df["Stage Description"].astype(str).str.strip()
                            active_mask = raw_df["Stage Description"].str.lower() == "active"
                            non_active_mask = ~active_mask
                            
                            # Initialize output columns in result_df
                            result_df = raw_df.copy()
                            result_df["Predicted Deal Status"] = ""
                            result_df["Business Logic Score"] = ""
                            result_df["Business Logic Status"] = ""
                            result_df["Win Probability"] = ""
                            
                            for class_name in le.classes_:
                                result_df[f"Probability_{class_name}"] = ""
                                
                            # Define the helper score calculators locally
                            def calculate_business_score(row):
                                score = 0
                                score += {5: 10, 3: 5, 2:2, 0: 0}.get(row.get("Account Engagement", 0), 0)
                                score += {5: 10, 3: 5, 2:2, 0: 0}.get(row.get("Client Relationship", 0), 0)
                                score += {5: 10, 3: 5, 2:2, 0: 0}.get(row.get("Deal Coach", 0), 0)
                                score += {5: 15, 3: 5, 2:2, 0: 0}.get(row.get("Bidder Rank", 0), 0)
                                score += {5: 10, 3: 5, 2:2, 0: 0}.get(row.get("Incumbency Share", 0), 0)
                                score += {5: 7, 3: 3, 2:1, 0: 0}.get(row.get("References", 0), 0)
                                score += {5: 7, 3: 3, 2:1, 0: 0}.get(row.get("Solution Strength", 0), 0)
                                score += {5: 6, 3: 3, 2:1, 0: 0}.get(row.get("Client Impression", 0), 0)
                                score += {5: 15, 3: 8, 2:4, 0: 0}.get(row.get("Orals Score", 0), 0)
                                score += {5: 5, 0: 2, 2: 0}.get(row.get("Price Alignment", 0), 0)
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
                                
                            # Get base URL for links
                            try:
                                host = st.context.headers.get("host", "localhost:8501")
                                protocol = "https" if st.context.headers.get("x-forwarded-proto") == "https" else "http"
                                base_url = f"{protocol}://{host}"
                            except Exception:
                                base_url = "http://localhost:8501"
                                
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
                                result_df.loc[active_mask, "Predicted Deal Status"] = pred_labels_active
                                
                                # Business Logic Score formatted as hyperlink URL
                                result_df.loc[active_mask, "Business Logic Score"] = [
                                    f"{base_url}/?show_calc={crm_id}&score={int(score)}%"
                                    for crm_id, score in zip(raw_df.loc[active_mask, "CRM ID"], active_business_scores)
                                ]
                                
                                win_idx = list(le.classes_).index("Won") if "Won" in list(le.classes_) else 0
                                active_win_probs = pred_probs_active[:, win_idx]
                                result_df.loc[active_mask, "Win Probability"] = [get_prob_category(p) for p in active_win_probs]
                                
                                for idx, class_name in enumerate(le.classes_):
                                    result_df.loc[active_mask, f"Probability_{class_name}"] = [
                                        f"{round(p * 100)}%" for p in pred_probs_active[:, idx]
                                    ]
                                    
                            # Process Non-Active Deals (statuses won, lost, hold etc. displayed as is)
                            if non_active_mask.any():
                                clean_statuses = raw_df.loc[non_active_mask, "Stage Description"].str.strip()
                                result_df.loc[non_active_mask, "Predicted Deal Status"] = clean_statuses
                                result_df.loc[non_active_mask, "Business Logic Status"] = clean_statuses
                                result_df.loc[non_active_mask, "Business Logic Score"] = "N/A"
                                result_df.loc[non_active_mask, "Win Probability"] = "N/A"
                                
                                for class_name in le.classes_:
                                    result_df.loc[non_active_mask, f"Probability_{class_name}"] = "N/A"
                                    
                            # Remove Deal Status column if it exists in raw_df to avoid duplication
                            if "Deal Status" in result_df.columns:
                                result_df = result_df.drop(columns=["Deal Status"])
                                
                            # Cache the predicted dataframe in session state for lookup
                            st.session_state.predicted_df = result_df
                            
                            # Save to output - create clean export file without local URLs in score column
                            export_df = result_df.copy()
                            for idx, row in export_df.iterrows():
                                score_val = row["Business Logic Score"]
                                if pd.notna(score_val) and str(score_val).startswith("http"):
                                    match = re.search(r"score=([^&]*)", str(score_val))
                                    if match:
                                        export_df.at[idx, "Business Logic Score"] = match.group(1)
                                        
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            output_filename = f"predictions_{timestamp}.xlsx"
                            output_path = os.path.join(OUTPUT_DIR, output_filename)
                            
                            os.makedirs(OUTPUT_DIR, exist_ok=True)
                            export_df.to_excel(output_path, index=False)
                            st.session_state.last_prediction_file = output_path
                            
                            st.markdown("""
                            <div class="success-box">
                                ✅ Predictions generated successfully!
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Show results
                            st.markdown("### 📊 Prediction Results")
                            
                            # Filter columns for display
                            display_cols = ["CRM ID", "Account Name", "Opportunity Name", "SST Sales Stage", "Stage Description", "Predicted Deal Status", "Win Probability", "Business Logic Status", "Business Logic Score"]
                            prob_cols = [col for col in result_df.columns if col.startswith("Probability_")]
                            display_cols.extend(prob_cols)
                            
                            valid_cols = [c for c in display_cols if c in result_df.columns]
                            
                            # Display with LinkColumn formatting for Business Logic Score
                            st.dataframe(
                                result_df[valid_cols],
                                column_config={
                                    "Business Logic Score": st.column_config.LinkColumn(
                                        label="Business Logic Score",
                                        display_text=r"score=([^&]*)"
                                    )
                                },
                                use_container_width=True
                            )
                            
                            # Statistics
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("Total Predictions", len(result_df))
                            with col2:
                                won_count = len(result_df[result_df['Predicted Deal Status'].astype(str).str.strip().str.lower().str.startswith('won')])
                                st.metric("Predicted Won", won_count)
                            with col3:
                                lost_count = len(result_df[result_df['Predicted Deal Status'].astype(str).str.strip().str.lower().str.startswith('lost')])
                                st.metric("Predicted Lost", lost_count)
                            with col4:
                                aborted_count = len(result_df[result_df['Predicted Deal Status'].astype(str).str.strip().str.lower().str.startswith('aborted')])
                                st.metric("Predicted Aborted", aborted_count)
                            
                            # Download button
                            buffer = io.BytesIO()
                            export_df.to_excel(buffer, index=False)
                            buffer.seek(0)
                            st.download_button(
                                label="📥 Download Predictions",
                                data=buffer,
                                file_name=output_filename,
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                type="primary"
                            )
                            
                        except Exception as e:
                            st.markdown(f"""
                            <div class="error-box">
                                ❌ Prediction error: {str(e)}
                            </div>
                            """, unsafe_allow_html=True)
            
            except Exception as e:
                st.markdown(f"""
                <div class="error-box">
                    ❌ Error reading file: {str(e)}
                </div>
                """, unsafe_allow_html=True)

# Audit Trail Page
elif page == "📈 Audit Trail":
    st.markdown('<div class="section-header">Prediction Audit Trail</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
    View the history of all predictions made by the tool. Analyze trends, distribution of outcomes, and download past reports.
    </div>
    """, unsafe_allow_html=True)
    
    # Scan for prediction files
    if os.path.exists(OUTPUT_DIR):
        pred_files = [f for f in os.listdir(OUTPUT_DIR) if f.startswith("predictions_") and f.endswith(".xlsx")]
        pred_files.sort(reverse=True) # Newest first
    else:
        pred_files = []
    
    if not pred_files:
        st.warning("No prediction history found.")
    else:
        all_preds = []
        
        # Progress bar for loading files
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, file in enumerate(pred_files):
            try:
                # Extract timestamp from filename
                # Format: predictions_YYYYMMDD_HHMMSS.xlsx
                ts_str = file.replace("predictions_", "").replace(".xlsx", "")
                try:
                    timestamp = datetime.strptime(ts_str, "%Y%m%d_%H%M%S")
                except ValueError:
                    # Fallback to file creation time if format doesn't match
                    timestamp = datetime.fromtimestamp(os.path.getctime(os.path.join(OUTPUT_DIR, file)))
                
                df = pd.read_excel(os.path.join(OUTPUT_DIR, file))
                
                # Add metadata
                df['Prediction_Date'] = timestamp
                df['Source_File'] = file
                
                # Ensure we have the predicted status column
                if 'Predicted Deal Status' in df.columns:
                    all_preds.append(df)
            except Exception as e:
                st.error(f"Error reading {file}: {str(e)}")
            
            # Update progress
            progress = (i + 1) / len(pred_files)
            progress_bar.progress(progress)
            status_text.text(f"Loading file {i+1} of {len(pred_files)}...")
        
        progress_bar.empty()
        status_text.empty()
        
        if all_preds:
            combined_df = pd.concat(all_preds, ignore_index=True)
            
            # --- Visualizations ---
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📊 Outcome Distribution")
                # Pie chart of Won/Lost/Aborted
                outcome_counts = combined_df['Predicted Deal Status'].value_counts().reset_index()
                outcome_counts.columns = ['Status', 'Count']
                
                fig_pie = px.pie(
                    outcome_counts, 
                    values='Count', 
                    names='Status', 
                    title='Overall Predicted Deal Outcomes',
                    color='Status',
                    color_discrete_map={'Won': '#2ecc71', 'Lost': '#e74c3c', 'Aborted': '#95a5a6'}
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                st.markdown("### 📈 Predictions Over Time")
                # Bar chart of predictions per day
                combined_df['Date'] = combined_df['Prediction_Date'].dt.date
                daily_counts = combined_df.groupby(['Date', 'Predicted Deal Status']).size().reset_index(name='Count')
                
                fig_bar = px.bar(
                    daily_counts, 
                    x='Date', 
                    y='Count', 
                    color='Predicted Deal Status',
                    title='Daily Prediction Volume by Outcome',
                    color_discrete_map={'Won': '#2ecc71', 'Lost': '#e74c3c', 'Aborted': '#95a5a6'}
                )
                st.plotly_chart(fig_bar, use_container_width=True)
            
            # Probability Distribution
            st.markdown("### 🎯 Win Probability Distribution")
            if 'Probability_Won' in combined_df.columns:
                fig_hist = px.histogram(
                    combined_df, 
                    x='Probability_Won', 
                    nbins=20, 
                    title='Distribution of Win Probabilities',
                    labels={'Probability_Won': 'Win Probability'},
                    color_discrete_sequence=['#3498db']
                )
                st.plotly_chart(fig_hist, use_container_width=True)
            
            # --- Raw Data Table ---
            st.markdown("### 📝 Detailed History")
            
            # Filter options
            col_filter1, col_filter2 = st.columns(2)
            with col_filter1:
                selected_status = st.multiselect(
                    "Filter by Status", 
                    options=combined_df['Predicted Deal Status'].unique(),
                    default=combined_df['Predicted Deal Status'].unique()
                )
            
            with col_filter2:
                selected_files = st.multiselect(
                    "Filter by Source File",
                    options=combined_df['Source_File'].unique(),
                    default=combined_df['Source_File'].unique()
                )
            
            filtered_df = combined_df[
                (combined_df['Predicted Deal Status'].isin(selected_status)) & 
                (combined_df['Source_File'].isin(selected_files))
            ]
            
            st.dataframe(
                filtered_df[['Prediction_Date', 'Source_File', 'Predicted Deal Status', 'Probability_Won'] + [c for c in filtered_df.columns if c not in ['Prediction_Date', 'Source_File', 'Predicted Deal Status', 'Probability_Won', 'Date']]], 
                use_container_width=True
            )
            
            st.caption(f"Showing {len(filtered_df)} records out of {len(combined_df)} total.")
            
        else:
            st.warning("No valid prediction data found in the files.")

# About Page
elif page == "ℹ️ About":
    st.markdown('<div class="section-header">About This Tool</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 🎯 Purpose
    This tool uses machine learning to predict the probability of winning deals based on historical patterns
    and deal characteristics.
    
    ### 🔧 Technology Stack
    - **Frontend:** Streamlit
    - **ML Model:** XGBoost Classifier
    - **Data Processing:** Pandas, Scikit-learn
    - **API:** FastAPI (available separately)
    
    ### 📊 Features
    1. **Synthetic Data Generation:** Create realistic training data
    2. **Model Training:** Train XGBoost classifier on synthetic data
    3. **Predictions:** Upload Excel files and get instant predictions
    4. **Interactive UI:** Easy-to-use web interface
    
    ### 🚀 How to Use
    1. Navigate to **Data Generation** and create synthetic training data
    2. Go to **Model Training** and train the XGBoost model
    3. Visit **Predictions** to upload your deal data and get predictions
    
    ### 📝 Version
    **Version:** 1.0.0  
    **Last Updated:** November 2025
    
    ### 🔗 Additional Resources
    - FastAPI endpoint available at `http://localhost:8000/swagger`
    - Postman collection included in project
    - Full documentation in `docs/` folder
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #7f8c8d;'>Deal Win Probability Tool v1.0.0 | Powered by XGBoost & Streamlit</div>",
    unsafe_allow_html=True
)
