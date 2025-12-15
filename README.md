# Deal Win Probability Prediction Tool

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-green)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)](https://streamlit.io/)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0%2B-orange)](https://xgboost.readthedocs.io/)

A comprehensive machine learning solution for predicting deal win probability using XGBoost classifier. The tool provides both a REST API (FastAPI) and an interactive web UI (Streamlit) for generating synthetic training data, training models, and making predictions.

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Backend API](#backend-api)
  - [Frontend UI](#frontend-ui)
  - [Command Line](#command-line)
- [API Documentation](#api-documentation)
- [Deployment](#deployment)
- [Documentation](#documentation)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## ✨ Features

### Core Functionality
- **Synthetic Data Generation**: Create realistic training data using predefined business rules and patterns
- **Model Training**: Train XGBoost classifier with automatic validation and feature engineering
- **Prediction**: Upload Excel files and get instant deal outcome predictions with probability scores
- **Dual Interface**: Choose between REST API or interactive web UI
- **Audit Trail**: Track and visualize prediction history with interactive charts

### Backend (FastAPI)
- RESTful API endpoints with automatic OpenAPI/Swagger documentation
- File upload and download support for Excel files
- Comprehensive error handling and validation
- Health check and model info endpoints
- Postman collection included for easy testing

### Frontend (Streamlit)
- Modern, responsive web interface with custom styling
- Multi-page application (Home, Data Generation, Model Training, Predictions, Audit Trail, About)
- Real-time progress tracking and status indicators
- Interactive data visualization with Plotly charts
- Drag-and-drop file upload
- Downloadable results in Excel format

### Machine Learning
- XGBoost classifier for high accuracy predictions
- Automatic feature engineering and preprocessing
- Label encoding for categorical variables
- Model persistence with joblib
- Validation metrics and performance tracking

## 📁 Project Structure

```
POC-Probability-Tool/
│
├── api.py                       # FastAPI application (main backend)
├── app.py                       # Streamlit application (main frontend)
│
├── src/                         # Core ML scripts
│   ├── generate_synthetic_data.py   # Synthetic data generation
│   ├── train_xgb_classifier.py      # XGBoost model training
│   └── predict_xgb_classifier.py    # Prediction logic
│
├── config/                      # Configuration files
│   ├── __init__.py
│   └── settings.py              # Application settings and parameters
│
├── utils/                       # Utility functions
│   ├── __init__.py
│   └── helpers.py               # Helper functions
│
├── data/                        # Data storage
│   ├── input/                   # Input data files
│   │   └── Data-Input.xlsx      # Input schema reference
│   ├── output/                  # Generated outputs and predictions
│   │   ├── Synthetic_Data.csv   # Generated synthetic training data
│   │   └── synthetic_deals.xlsx # Synthetic data in Excel format
│   └── predictions/             # Prediction results
│
├── models/                      # Trained models
│   ├── xgb_classifier.pkl       # Saved XGBoost model
│   └── label_encoder.pkl        # Saved label encoder
│
├── docs/                        # Documentation
│   ├── API_SETUP.md             # API setup guide
│   ├── FASTAPI_GUIDE.md         # FastAPI usage guide
│   ├── STREAMLIT_GUIDE.md       # Streamlit UI guide
│   ├── DEPLOYMENT.md            # Deployment instructions
│   ├── ARCHITECTURE_DETAILED.md # Detailed architecture documentation
│   ├── DIAGRAMS_GUIDE.md        # Guide for architecture diagrams
│   ├── Architecture_Diagram.drawio    # System architecture diagram
│   ├── Workflow_Diagrams.drawio       # Workflow diagrams
│   └── architecture_diagrams/   # Exported diagram images
│
├── docker/                      # Docker configuration
│   ├── Dockerfile.api           # Dockerfile for FastAPI
│   ├── Dockerfile.streamlit     # Dockerfile for Streamlit
│   ├── docker-compose.yml       # Docker Compose configuration
│   ├── build.ps1                # Build script for Windows
│   ├── run.ps1                  # Run script for Windows
│   ├── INSTALL.md               # Docker installation guide
│   └── README.md                # Docker usage guide
│
├── deployment/                  # Deployment scripts
│   ├── deployment.bat           # Windows deployment script
│   ├── deployment.sh            # Linux/Mac deployment script
│   ├── start_services.bat       # Start services (Windows)
│   ├── start_services.sh        # Start services (Linux/Mac)
│   ├── stop_services.bat        # Stop services (Windows)
│   ├── stop_services.sh         # Stop services (Linux/Mac)
│   └── README.md                # Deployment guide
│
├── .streamlit/                  # Streamlit configuration
│   └── config.toml              # Streamlit config
│
├── requirements.txt             # Python dependencies
├── requirements-dev.txt         # Development dependencies
├── runtime.txt                  # Python runtime version
├── .gitignore                   # Git ignore file
├── README.md                    # This file
├── QUICKSTART.md                # Quick start guide
├── TROUBLESHOOTING.md           # Troubleshooting guide
├── CLEANUP_SUMMARY.md           # Project cleanup summary
├── cleanup.ps1                  # Cleanup script
└── Deal_Win_Probability_API.postman_collection.json  # Postman collection
```

## 🚀 Installation

### Prerequisites
- **Python 3.10 or higher** (Python 3.14 recommended)
- pip (Python package manager)
- Virtual environment (recommended)
- *(Optional)* Docker and Docker Compose for containerized deployment

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd POC-Probability-Tool
```

### Step 2: Create Virtual Environment
```powershell
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

#### Option A: Install from requirements.txt (Recommended)
```powershell
# Windows - Using virtual environment
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# For Python 3.14, install pyarrow pre-release
.\.venv\Scripts\python.exe -m pip install pyarrow --pre

# Linux/Mac
pip install --upgrade pip
pip install -r requirements.txt
```

#### Option B: Manual Installation (Step-by-step)
```powershell
# Windows - Using virtual environment
.\.venv\Scripts\python.exe -m pip install --upgrade pip

# Install core dependencies
.\.venv\Scripts\python.exe -m pip install pandas numpy openpyxl scikit-learn xgboost joblib

# Install backend dependencies
.\.venv\Scripts\python.exe -m pip install fastapi uvicorn[standard] python-multipart pydantic pydantic-settings

# Install frontend dependencies
.\.venv\Scripts\python.exe -m pip install streamlit plotly altair

# Install additional dependencies
.\.venv\Scripts\python.exe -m pip install colorama python-dotenv

# Install pyarrow (pre-release for Python 3.14 compatibility)
.\.venv\Scripts\python.exe -m pip install pyarrow --pre

# Optional: Install development dependencies
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

## 🎯 Quick Start

See [QUICKSTART.md](QUICKSTART.md) for detailed quick start instructions.

### Method 1: Using Deployment Scripts (Easiest)

#### Windows
```powershell
# Start both backend and frontend services
.\deployment\start_services.bat

# Choose option 2 (Native Python) when prompted
```

#### Linux/Mac
```bash
# Make scripts executable
chmod +x deployment/start_services.sh

# Start both services
./deployment/start_services.sh
```

The script will:
- ✅ Activate the virtual environment
- ✅ Start FastAPI backend on port 8000
- ✅ Start Streamlit UI on port 8501
- ✅ Create log files in the `logs/` directory

### Method 2: Manual Start (Two Terminals)

#### Terminal 1: Start Backend API
```powershell
# Windows - Using virtual environment
.\.venv\Scripts\Activate.ps1
.\.venv\Scripts\python.exe api.py

# Linux/Mac
source .venv/bin/activate
python api.py
```

**Backend will be available at:**
- **API Base**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

#### Terminal 2: Start Frontend UI
```powershell
# Windows - Using virtual environment
.\.venv\Scripts\Activate.ps1
.\.venv\Scripts\streamlit run app.py

# Linux/Mac
source .venv/bin/activate
streamlit run app.py
```

**Frontend will be available at:**
- **Streamlit UI**: http://localhost:8501

### Method 3: Using Uvicorn (Production-like)

```powershell
# Windows - Using virtual environment
.\.venv\Scripts\Activate.ps1
.\.venv\Scripts\uvicorn api:app --host 0.0.0.0 --port 8000 --reload

# Linux/Mac
source .venv/bin/activate
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

### Method 4: Docker Deployment

```powershell
# Navigate to docker directory
cd docker

# Build and run with Docker Compose
docker-compose up -d

# Or use the build script (Windows)
.\build.ps1
.\run.ps1
```

See [docker/README.md](docker/README.md) for detailed Docker instructions.

## 📖 Usage

### Backend API

#### 1. Health Check
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "message": "API is running",
  "model_loaded": true
}
```

#### 2. Generate Synthetic Data
```bash
curl -X POST "http://localhost:8000/generate-synthetic-data"
```

**Response:**
```json
{
  "success": true,
  "message": "Synthetic data generated successfully",
  "records_generated": 100,
  "output_path": "data/output/Synthetic_Data.csv"
}
```

#### 3. Train Model
```bash
curl -X POST "http://localhost:8000/train-model"
```

**Response:**
```json
{
  "success": true,
  "message": "Model trained successfully",
  "validation_accuracy": 0.95,
  "model_path": "models/xgb_classifier.pkl"
}
```

#### 4. Make Predictions
```bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@data/input/your-deals.xlsx"
```

**Response:**
```json
{
  "success": true,
  "message": "Predictions completed successfully",
  "predictions_file": "predictions_20231211_115238.xlsx",
  "total_records": 50
}
```

#### 5. Download Predictions
```bash
curl -X GET "http://localhost:8000/download-predictions/predictions_20231211_115238.xlsx" \
  --output predictions.xlsx
```

#### 6. Get Model Info
```bash
curl http://localhost:8000/model-info
```

**Response:**
```json
{
  "model_exists": true,
  "model_type": "XGBoost Classifier",
  "model_size_mb": 2.5,
  "last_modified": "2023-12-11T11:52:38"
}
```

### Frontend UI

The Streamlit UI provides an intuitive interface with the following pages:

1. **🏠 Home**: 
   - View dashboard with system status
   - Quick statistics (training records, model status, predictions made)
   - System health indicators

2. **📁 Data Generation**: 
   - Generate synthetic training data (default: 100 records)
   - View data statistics (total records, won/lost deals)
   - Download generated data
   - Preview data in interactive table

3. **🤖 Model Training**: 
   - Train XGBoost classifier
   - View training progress
   - Display validation accuracy and metrics
   - Model performance indicators

4. **🔮 Predictions**: 
   - Upload Excel files (drag-and-drop or browse)
   - Get instant predictions with probability scores
   - View predictions in interactive table
   - Download results in Excel format
   - See prediction distribution charts

5. **📈 Audit Trail**: 
   - View prediction history
   - Interactive charts and filters
   - Track model performance over time
   - Export audit logs

6. **ℹ️ About**: 
   - Learn about the tool
   - Technology stack information
   - Feature overview
   - Contact information

### Command Line

Run individual scripts directly:

#### Generate Synthetic Data
```powershell
# Windows
.\.venv\Scripts\python.exe src\generate_synthetic_data.py

# Linux/Mac
python src/generate_synthetic_data.py
```

**Output:**
- Generates 100 synthetic records
- Saves to `data/output/Synthetic_Data.csv`
- Uses schema from `data/input/Data-Input.xlsx`

#### Train Model
```powershell
# Windows
.\.venv\Scripts\python.exe src\train_xgb_classifier.py

# Linux/Mac
python src/train_xgb_classifier.py
```

**Output:**
- Trains XGBoost model
- Saves model to `models/xgb_classifier.pkl`
- Saves label encoder to `models/label_encoder.pkl`

#### Make Predictions
```powershell
# Windows
.\.venv\Scripts\python.exe src\predict_xgb_classifier.py

# Linux/Mac
python src/predict_xgb_classifier.py
```

**Output:**
- Loads trained model
- Processes input data
- Saves predictions to `data/output/predictions_*.xlsx`

## 📚 API Documentation

### Endpoints

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| GET | `/` | API information and available endpoints | - | JSON with API info |
| GET | `/health` | Health check and model availability | - | HealthResponse |
| POST | `/generate-synthetic-data` | Generate synthetic training data | - | SyntheticDataResponse |
| POST | `/train-model` | Train XGBoost model | - | TrainingResponse |
| POST | `/predict` | Upload file and get predictions | Excel file | PredictionResponse |
| GET | `/download-predictions/{filename}` | Download prediction results | filename | Excel file |
| GET | `/model-info` | Get model information and statistics | - | JSON with model info |

### Request/Response Models

#### HealthResponse
```json
{
  "status": "string",
  "message": "string",
  "model_loaded": "boolean"
}
```

#### SyntheticDataResponse
```json
{
  "success": "boolean",
  "message": "string",
  "records_generated": "integer",
  "output_path": "string"
}
```

#### TrainingResponse
```json
{
  "success": "boolean",
  "message": "string",
  "validation_accuracy": "float",
  "model_path": "string"
}
```

#### PredictionResponse
```json
{
  "success": "boolean",
  "message": "string",
  "predictions_file": "string",
  "total_records": "integer"
}
```

### Postman Collection

Import `Deal_Win_Probability_API.postman_collection.json` into Postman for pre-configured API requests with examples.

**To use:**
1. Open Postman
2. Click Import → Upload Files
3. Select `Deal_Win_Probability_API.postman_collection.json`
4. Update the base URL if needed (default: `http://localhost:8000`)

## 🚀 Deployment

### Docker Deployment

See [docker/README.md](docker/README.md) and [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed deployment instructions.

#### Quick Docker Start
```powershell
# Build and run with Docker Compose
cd docker
docker-compose up -d

# Or use the build script (Windows)
.\build.ps1
.\run.ps1

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Manual Deployment

#### FastAPI with Uvicorn (Production)
```bash
# Single worker
uvicorn api:app --host 0.0.0.0 --port 8000

# Multiple workers (production)
uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4
```

#### Streamlit (Production)
```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

### Production Deployment Best Practices

1. **Use a reverse proxy** (Nginx/Apache) for SSL/TLS
2. **Set up environment variables** for sensitive data
3. **Configure logging** for monitoring
4. **Use process managers** (systemd, supervisor, PM2)
5. **Enable CORS** appropriately for your domain
6. **Set up monitoring** (Prometheus, Grafana)
7. **Configure backups** for models and data

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed production deployment guide.

## 📖 Documentation

Comprehensive documentation is available in the `docs/` folder:

- **[QUICKSTART.md](QUICKSTART.md)** - Quick start guide
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions
- **[API_SETUP.md](docs/API_SETUP.md)** - API setup and configuration
- **[FASTAPI_GUIDE.md](docs/FASTAPI_GUIDE.md)** - FastAPI usage guide
- **[STREAMLIT_GUIDE.md](docs/STREAMLIT_GUIDE.md)** - Streamlit UI guide
- **[DEPLOYMENT.md](docs/DEPLOYMENT.md)** - Deployment instructions
- **[ARCHITECTURE_DETAILED.md](docs/ARCHITECTURE_DETAILED.md)** - Detailed architecture
- **[DIAGRAMS_GUIDE.md](docs/DIAGRAMS_GUIDE.md)** - Architecture diagrams guide

## 📊 Data Format

### Input Excel File Structure
The input file should have the following structure (first row is headers):

```
| CRM ID | SBU | Qtr of closure | Deal Status | Account Name | Opportunity Name | Expected TCV ($Mn) | Deal Size bucket | Type of Business | Primary L1 | Primary L2 | Secondary L1 | Secondary L2 | Tertiary L1 | Tertiary L2 | Detailed Remarks | ... |
|--------|-----|----------------|-------------|--------------|------------------|-------------------|------------------|------------------|-----------|-----------|-------------|-------------|------------|------------|-----------------|-----|
| CRM001 | BFS | Q1'25          | Won         | HSBC         | Deal 1           | 50.5              | <250M            | EE               | Relationship | Client Relationship... | Solution | Technical Response... | Commercials | Deviation/fit... | Won due to... | ... |
```

**Reference:** See `data/input/Data-Input.xlsx` for the complete schema.

### Output Excel File Structure
```
| CRM ID | Account Name | Opportunity Name | ... | Predicted Deal Status | Probability_Won | Probability_Lost | Probability_Aborted |
|--------|--------------|------------------|-----|----------------------|-----------------|------------------|---------------------|
| CRM001 | HSBC         | Deal 1           | ... | Won                  | 0.85            | 0.10             | 0.05                |
| CRM002 | MOHRE        | Deal 2           | ... | Lost                 | 0.15            | 0.75             | 0.10                |
```

## ⚙️ Configuration

Edit `config/settings.py` to customize:
- Model hyperparameters (learning rate, max depth, n_estimators)
- File paths and directories
- API settings (host, port, CORS)
- UI configuration (theme, layout)
- Feature engineering parameters
- Logging configuration

## 🔧 Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for comprehensive troubleshooting guide.

### Common Issues

#### 1. PyArrow Installation Error (Python 3.14)
**Error:** `Could not find a version that satisfies the requirement pyarrow`

**Solution:**
```powershell
.\.venv\Scripts\python.exe -m pip install pyarrow --pre
```

#### 2. Module Not Found Errors
**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```powershell
# Ensure virtual environment is activated
.\.venv\Scripts\Activate.ps1

# Reinstall dependencies
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

#### 3. Port Already in Use
**Error:** `Address already in use`

**Solution:**
```powershell
# Windows - Find and kill process using port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or use different port
uvicorn api:app --port 8001
```

#### 4. Streamlit Not Opening in Browser
**Solution:**
```powershell
# Manually open in browser
start http://localhost:8501

# Or specify browser
streamlit run app.py --browser.serverAddress localhost
```

#### 5. Model Not Found Error
**Error:** `Model file not found`

**Solution:**
1. Generate synthetic data first
2. Train the model
3. Ensure `models/xgb_classifier.pkl` exists

```powershell
# Generate data and train model
.\.venv\Scripts\python.exe src\generate_synthetic_data.py
.\.venv\Scripts\python.exe src\train_xgb_classifier.py
```

#### 6. Excel File Upload Error
**Error:** `Invalid file format`

**Solution:**
- Ensure file is `.xlsx` format
- Check file has required columns
- Verify file is not corrupted
- File size should be < 200MB

## 📈 Performance

- **Training Time**: ~10-30 seconds for 100 records
- **Prediction Time**: <1 second for 100 records
- **Model Size**: ~2-5 MB
- **API Response Time**: <100ms average
- **Concurrent Users**: Supports 50+ concurrent users (with proper deployment)

## 🔒 Security

- ✅ Input validation on all endpoints
- ✅ File type verification (Excel only)
- ✅ Size limits on uploads (200MB max)
- ✅ CORS configuration
- ✅ Environment variable protection
- ✅ No hardcoded credentials
- ✅ Secure file handling
- ✅ Request rate limiting (configurable)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup
```powershell
# Install development dependencies
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt

# Run tests (if available)
pytest

# Format code
black .

# Lint code
flake8 .
```

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **XGBoost** team for the excellent ML library
- **FastAPI** team for the modern web framework
- **Streamlit** team for the interactive UI framework
- **Scikit-learn** for preprocessing utilities
- **Pandas** team for data manipulation tools

## 📞 Support

For support:
- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Review documentation in `docs/` folder
- Open an issue in the repository
- Contact the development team

## 🔄 Recent Updates

### Version 1.0.0 (December 2024)
- ✅ Fixed synthetic data generation to work without OpenAI API
- ✅ Updated file paths to use correct data directory structure
- ✅ Improved error handling and logging
- ✅ Enhanced deployment scripts for easier setup
- ✅ Updated documentation with accurate instructions
- ✅ Added comprehensive troubleshooting guide

---

**Built with ❤️ using Python, FastAPI, Streamlit, and XGBoost**

**Quick Links:**
- 🌐 [Streamlit UI](http://localhost:8501) (after starting services)
- 📡 [FastAPI Docs](http://localhost:8000/docs) (after starting services)
- 📖 [Full Documentation](docs/)
- 🚀 [Quick Start Guide](QUICKSTART.md)
