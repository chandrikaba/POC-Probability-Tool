# Streamlit UI Guide

## Overview
This project includes a beautiful, modern Streamlit web interface for the Deal Win Probability prediction tool.

## Installation

Install Streamlit (if not already installed):
```bash
pip install streamlit
```

Or install all dependencies:
```bash
pip install -r requirements.txt
```

## Running the Streamlit App

### Start the application:
```bash
streamlit run app.py
```

The app will automatically open in your default browser at: `http://localhost:8501`

## Features

### 🏠 Home Page
- Overview of the tool and workflow
- Quick statistics dashboard
- System status indicators

### 📁 Data Generation
- Generate synthetic training data
- Configure number of records
- Preview generated data
- Download synthetic data as Excel

### 🤖 Model Training
- Train XGBoost classifier
- View training progress
- See validation accuracy
- Model information and statistics

### 🔮 Predictions
- Upload Excel files for prediction
- Real-time prediction generation
- Preview input and output data
- Download predictions as Excel
- View prediction statistics

### ℹ️ About
- Tool information
- Technology stack
- Usage instructions
- Version information

## User Interface Features

### Modern Design
- Clean, professional interface
- Color-coded status indicators
- Responsive layout
- Custom CSS styling

### Interactive Elements
- File upload with drag-and-drop
- Real-time progress indicators
- Interactive data tables
- Download buttons for results

### Status Tracking
The sidebar shows real-time status of:
- Synthetic data availability
- Model training status
- Model size and information

## Workflow

1. **Generate Data**
   - Navigate to "📁 Data Generation"
   - Click "Generate Synthetic Data"
   - View and download the generated data

2. **Train Model**
   - Go to "🤖 Model Training"
   - Click "Train Model"
   - Wait for training to complete
   - View validation accuracy

3. **Make Predictions**
   - Visit "🔮 Predictions"
   - Upload your Excel file
   - Click "Generate Predictions"
   - View results and download

## Tips

### File Upload
- Supported formats: .xlsx, .xls
- First row will be skipped (assumed to be title)
- Ensure column structure matches training data

### Performance
- Training typically takes 10-30 seconds
- Predictions are generated instantly
- Large files (>1000 rows) may take longer

### Data Requirements
- Input file should have same columns as training data
- Missing columns will be filled with default values
- Extra columns will be ignored

## Customization

### Changing Port
```bash
streamlit run app.py --server.port 8502
```

### Running on Network
```bash
streamlit run app.py --server.address 0.0.0.0
```

### Configuration
Create `.streamlit/config.toml` for custom settings:
```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
port = 8501
enableCORS = false
```

## Troubleshooting

### Port Already in Use
If port 8501 is already in use:
```bash
streamlit run app.py --server.port 8502
```

### Module Not Found
Install missing dependencies:
```bash
pip install -r requirements.txt
```

### File Upload Issues
- Check file format (.xlsx or .xls)
- Ensure file is not corrupted
- Try with a smaller file first

## Comparison: Streamlit vs FastAPI

### Use Streamlit When:
- You want a quick, interactive UI
- Users need to upload files manually
- Visual feedback is important
- Running locally or for demos

### Use FastAPI When:
- Building a production API
- Need programmatic access
- Integrating with other systems
- Require REST endpoints

Both interfaces can run simultaneously:
- Streamlit: `http://localhost:8501`
- FastAPI: `http://localhost:8000`

## Screenshots

The UI includes:
- 📊 Dashboard with metrics
- 📁 File upload interface
- 📈 Data preview tables
- ✅ Success/error notifications
- 📥 Download buttons
- 🎨 Color-coded status indicators

## Production Deployment

### Using Streamlit Cloud
1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Deploy with one click

### Using Docker
Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

Build and run:
```bash
docker build -t deal-win-streamlit .
docker run -p 8501:8501 deal-win-streamlit
```

## Support

For issues or questions:
- Check the About page in the app
- Review the FastAPI documentation
- Consult the project README
