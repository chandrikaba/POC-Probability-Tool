# FastAPI Setup and Usage Guide

## Overview
This project now includes a FastAPI-based REST API for the Deal Win Probability prediction tool.

## Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Running the API

### Start the server:
```bash
python api.py
```

Or using uvicorn directly:
```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

## API Documentation

### Swagger UI (Interactive API Documentation)
Once the server is running, access the interactive Swagger documentation at:
```
http://localhost:8000/swagger
```

### ReDoc (Alternative Documentation)
Alternative documentation format available at:
```
http://localhost:8000/redoc
```

## Available Endpoints

### 1. Health Check
- **Endpoint:** `GET /health`
- **Description:** Check API health and model availability
- **Response:**
```json
{
  "status": "healthy",
  "message": "API is running",
  "model_loaded": true
}
```

### 2. Generate Synthetic Data
- **Endpoint:** `POST /generate-synthetic-data`
- **Description:** Generate synthetic training data
- **Response:**
```json
{
  "success": true,
  "message": "Synthetic data generated successfully",
  "records_generated": 30,
  "output_path": "path/to/synthetic_deals.xlsx"
}
```

### 3. Train Model
- **Endpoint:** `POST /train-model`
- **Description:** Train the XGBoost classifier
- **Response:**
```json
{
  "success": true,
  "message": "Model trained successfully",
  "validation_accuracy": 0.85,
  "model_path": "path/to/xgb_classifier.pkl"
}
```

### 4. Predict Deal Outcomes
- **Endpoint:** `POST /predict`
- **Description:** Upload Excel file and get predictions
- **Request:** Multipart form data with file upload
- **Response:**
```json
{
  "success": true,
  "message": "Predictions generated successfully",
  "predictions_file": "predictions_20250127_203000.xlsx",
  "total_records": 10
}
```

### 5. Download Predictions
- **Endpoint:** `GET /download-predictions/{filename}`
- **Description:** Download the predictions file
- **Response:** Excel file download

### 6. Get Model Info
- **Endpoint:** `GET /model-info`
- **Description:** Get information about the current model
- **Response:**
```json
{
  "model_exists": true,
  "model_path": "path/to/model",
  "model_size_mb": 2.5,
  "last_modified": "2025-01-27T20:30:00"
}
```

## Using Postman

### Import the Collection
1. Open Postman
2. Click **Import**
3. Select the file: `Deal_Win_Probability_API.postman_collection.json`
4. The collection will be imported with all endpoints pre-configured

### Collection Variables
The collection includes a variable:
- `base_url`: Default is `http://localhost:8000`

You can modify this in Postman's environment settings if your server runs on a different host/port.

### Testing the Workflow

1. **Check Health:**
   - Run the "Health Check" request
   - Verify the API is running

2. **Generate Data:**
   - Run "Generate Synthetic Data"
   - This creates training data

3. **Train Model:**
   - Run "Train Model"
   - This trains the XGBoost classifier

4. **Make Predictions:**
   - Run "Predict Deal Outcomes"
   - Upload your Excel file (Data-Input.xlsx)
   - Note the `predictions_file` name in the response

5. **Download Results:**
   - Update the filename in "Download Predictions"
   - Run the request to download the Excel file with predictions

## cURL Examples

### Health Check
```bash
curl -X GET "http://localhost:8000/health"
```

### Generate Synthetic Data
```bash
curl -X POST "http://localhost:8000/generate-synthetic-data"
```

### Train Model
```bash
curl -X POST "http://localhost:8000/train-model"
```

### Predict (Upload File)
```bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@data/input/Data-Input.xlsx"
```

### Download Predictions
```bash
curl -X GET "http://localhost:8000/download-predictions/predictions_20250127_203000.xlsx" \
  --output predictions.xlsx
```

## Production Deployment

### Using Gunicorn (Recommended for Production)
```bash
pip install gunicorn
gunicorn api:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Using Docker
Create a `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t deal-win-api .
docker run -p 8000:8000 deal-win-api
```

## Troubleshooting

### Port Already in Use
If port 8000 is already in use, change the port:
```bash
uvicorn api:app --port 8001
```

### Model Not Found Error
Ensure you've trained the model first:
1. Run `/generate-synthetic-data`
2. Run `/train-model`
3. Then try `/predict`

### File Upload Issues
- Ensure the file is a valid Excel file (.xlsx or .xls)
- Check that the file structure matches the expected format
- The first row will be skipped (assumed to be a title row)

## Security Considerations

For production deployment:
1. Add authentication (e.g., API keys, OAuth2)
2. Enable CORS if needed
3. Add rate limiting
4. Use HTTPS
5. Validate and sanitize all inputs
6. Set up proper logging and monitoring
