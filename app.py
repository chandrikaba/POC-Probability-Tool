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
from sklearn.preprocessing import LabelEncoder

import plotly.express as px

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
SYNTHETIC_DATA_PATH = os.path.join(PROJECT_ROOT, "data", "output", "synthetic_deals.xlsx")
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
    
    page = st.radio(
        "Select a page:",
        ["🏠 Home", "📁 Data Generation", "🤖 Model Training", "🔮 Predictions", "📈 Audit Trail", "ℹ️ About"],
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
        The file should have the same structure as the training data (first row will be skipped).
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
                raw_df = pd.read_excel(uploaded_file, skiprows=1)
                
                st.markdown("### 📊 Input Data Preview")
                st.dataframe(raw_df.head(10), use_container_width=True)
                st.caption(f"Total records: {len(raw_df)}")
                
                predict_btn = st.button("🔮 Generate Predictions", type="primary", use_container_width=True)
                
                if predict_btn:
                    with st.spinner("Generating predictions..."):
                        try:
                            import numpy as np
                            
                            # Load model and label encoder
                            model = joblib.load(MODEL_PATH)
                            encoder_path = os.path.join(PROJECT_ROOT, "models", "label_encoder.pkl")
                            le = joblib.load(encoder_path)
                            
                            # Load synthetic data to get expected column structure
                            if not os.path.exists(SYNTHETIC_DATA_PATH):
                                st.error("Synthetic data not found. Please generate and train the model first.")
                                st.stop()
                            
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
                            
                            st.session_state.last_prediction_file = output_path
                            
                            st.markdown("""
                            <div class="success-box">
                                ✅ Predictions generated successfully!
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Show results
                            st.markdown("### 📊 Prediction Results")
                            
                            # Filter columns for display
                            display_cols = ["CRM ID", "Account Name", "Predicted Deal Status"]
                            # Add probability columns dynamically based on classes
                            prob_cols = [col for col in result_df.columns if col.startswith("Probability_")]
                            display_cols.extend(prob_cols)
                            
                            # Ensure columns exist before selecting
                            valid_cols = [c for c in display_cols if c in result_df.columns]
                            st.dataframe(result_df[valid_cols], use_container_width=True)
                            
                            # Statistics
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("Total Predictions", len(result_df))
                            with col2:
                                won_count = len(result_df[result_df['Predicted Deal Status'] == 'Won'])
                                st.metric("Predicted Won", won_count)
                            with col3:
                                lost_count = len(result_df[result_df['Predicted Deal Status'] == 'Lost'])
                                st.metric("Predicted Lost", lost_count)
                            with col4:
                                aborted_count = len(result_df[result_df['Predicted Deal Status'] == 'Aborted'])
                                st.metric("Predicted Aborted", aborted_count)
                            
                            # Download button
                            buffer = io.BytesIO()
                            result_df.to_excel(buffer, index=False)
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
