# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies (1 minute)
```bash
pip install -r requirements.txt
```

### Step 2: Choose Your Interface

#### Option A: Web UI (Streamlit) - Recommended for Beginners
```bash
python -m streamlit run app.py
```
Then open: http://localhost:8501

**What you can do:**
- Generate synthetic training data with one click
- Train the XGBoost model visually
- Upload Excel files and get predictions
- Download results instantly

#### Option B: REST API (FastAPI) - For Developers
```bash
python api.py
```
Then open: http://localhost:8000/swagger

**What you can do:**
- Test API endpoints interactively
- Integrate with other applications
- Use Postman collection
- Programmatic access

#### Option C: Both Interfaces
```bash
# Terminal 1
python api.py

# Terminal 2
python -m streamlit run app.py
```

### Step 3: Complete the Workflow

#### Using Streamlit UI:
1. Click "📁 Data Generation" → Generate Data
2. Click "🤖 Model Training" → Train Model
3. Click "🔮 Predictions" → Upload your Excel file
4. Download the predictions

#### Using FastAPI:
1. Go to http://localhost:8000/swagger
2. POST `/generate-synthetic-data`
3. POST `/train-model`
4. POST `/predict` (upload file)
5. GET `/download-predictions/{filename}`

## 📁 Your First Prediction

### Prepare Your Data
Create an Excel file with columns like:
- CRM ID
- Account Name
- Opportunity Name
- Expected TCV
- Deal Size bucket
- Type of Business
- Primary L1, L2
- Secondary L1, L2
- etc.

### Upload and Predict
1. Open the UI at http://localhost:8501
2. Go to "🔮 Predictions"
3. Upload your Excel file
4. Click "Generate Predictions"
5. Download the results with predictions added!

## 🎯 What's Next?

### Explore the Documentation
- **README.md** - Complete project documentation
- **MODULARIZATION_SUMMARY.md** - What's been built
- **RESTRUCTURING_GUIDE.md** - How to improve the structure
- **docs/FASTAPI_GUIDE.md** - API details
- **docs/STREAMLIT_GUIDE.md** - UI details

### Customize the Tool
- Adjust model parameters in `src/train_xgb_classifier.py`
- Modify synthetic data in `src/generate_synthetic_data.py`
- Customize UI in `app.py`

### Deploy to Production
- Follow Docker instructions in README.md
- Use the provided Dockerfile
- Deploy to cloud platforms

## 🆘 Troubleshooting

### Port Already in Use
```bash
# For Streamlit
streamlit run app.py --server.port 8502

# For FastAPI
python api.py --port 8001
```

### Missing Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Model Not Found
1. Generate synthetic data first
2. Train the model
3. Then make predictions

## 📞 Need Help?

- Check the comprehensive README.md
- Review the API documentation at /swagger
- See the RESTRUCTURING_GUIDE.md for advanced setup

---

**You're all set! Start predicting deal outcomes now! 🎉**
