# Troubleshooting Guide

## Common Issues and Solutions

### 1. Missing Module Errors

#### Error: "No module named 'pyarrow'"
**Solution:**
```bash
pip install pyarrow
```

#### Error: "No module named 'streamlit'"
**Solution:**
```bash
pip install streamlit
```

#### Error: "No module named 'fastapi'"
**Solution:**
```bash
pip install fastapi uvicorn
```

#### Error: "No module named 'xgboost'"
**Solution:**
```bash
pip install xgboost
```

**General Solution for All Dependencies:**
```bash
pip install -r requirements.txt
```

### 2. Port Already in Use

#### Error: "Address already in use" (Port 8000)
**Solution:**
```bash
# Option 1: Use a different port
uvicorn api:app --port 8001

# Option 2: Kill the process using port 8000 (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Option 2: Kill the process (Linux/Mac)
lsof -ti:8000 | xargs kill -9
```

#### Error: "Address already in use" (Port 8501)
**Solution:**
```bash
# Option 1: Use a different port
streamlit run app.py --server.port 8502

# Option 2: Kill the process (Windows)
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

### 3. File Upload Issues

#### Error: "Only Excel files (.xlsx, .xls) are supported"
**Solution:**
- Ensure your file has .xlsx or .xls extension
- Convert CSV to Excel if needed
- Check file is not corrupted

#### Error: "File not found"
**Solution:**
- Check file path is correct
- Ensure file exists in data/input/ directory
- Verify file permissions

#### Error: "Permission denied" when saving predictions
**Solution:**
- Close the Excel file if it's open
- Check write permissions on data/output/ folder
- The app will automatically create a timestamped file if the default is locked

### 4. Model Errors

#### Error: "Trained model not found"
**Solution:**
1. Generate synthetic data first:
   - UI: Go to "📁 Data Generation" → Click "Generate Data"
   - API: POST /generate-synthetic-data

2. Train the model:
   - UI: Go to "🤖 Model Training" → Click "Train Model"
   - API: POST /train-model

#### Error: "Synthetic data not found"
**Solution:**
```bash
# Run data generation
python src/generate_synthetic_data.py

# Or use the UI/API
```

#### Error: "Feature mismatch" or "Column alignment error"
**Solution:**
- Ensure input file has same columns as training data
- Check column names match exactly
- Missing columns will be filled with default values

### 5. Streamlit Issues

#### Error: "This app has encountered an error"
**Solution:**
1. Check the terminal for detailed error message
2. Restart Streamlit:
   ```bash
   # Press Ctrl+C to stop
   # Then restart
   streamlit run app.py
   ```

#### Error: "Connection error" or "WebSocket error"
**Solution:**
1. Refresh the browser page
2. Clear browser cache
3. Try a different browser
4. Check firewall settings

#### Error: "Module not found" in Streamlit
**Solution:**
```bash
# Restart Streamlit after installing dependencies
pip install -r requirements.txt
# Then restart the app
```

### 6. API Issues

#### Error: "404 Not Found"
**Solution:**
- Check the endpoint URL is correct
- Ensure API is running (python api.py)
- Verify the route exists in the API

#### Error: "422 Unprocessable Entity"
**Solution:**
- Check request body format
- Ensure required fields are provided
- Verify file upload format (multipart/form-data)

#### Error: "500 Internal Server Error"
**Solution:**
- Check API logs in terminal
- Verify all dependencies are installed
- Ensure data files exist

### 7. Excel File Issues

#### Error: "BadZipFile" or "File is not a zip file"
**Solution:**
- File may be corrupted
- Ensure it's a valid Excel file
- Try opening in Excel first
- Re-save the file

#### Error: "openpyxl not installed"
**Solution:**
```bash
pip install openpyxl
```

#### Error: "xlrd not installed" (for .xls files)
**Solution:**
```bash
pip install xlrd
```

### 8. Performance Issues

#### Issue: Slow predictions
**Solution:**
- Reduce file size (split large files)
- Close other applications
- Check system resources
- Consider batch processing

#### Issue: High memory usage
**Solution:**
- Process files in smaller batches
- Restart the application
- Increase system RAM if possible

### 9. Installation Issues

#### Error: "pip not found"
**Solution:**
```bash
# Windows
python -m pip install --upgrade pip

# Linux/Mac
python3 -m pip install --upgrade pip
```

#### Error: "Permission denied" during installation
**Solution:**
```bash
# Install for current user only
pip install --user -r requirements.txt

# Or use virtual environment (recommended)
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

#### Error: "Failed building wheel for pyarrow"
**Solution:**
```bash
# Install pre-built binary
pip install pyarrow --only-binary :all:

# Or skip pyarrow (may have limited functionality)
pip install pandas openpyxl
```

### 10. Data Issues

#### Error: "Empty DataFrame"
**Solution:**
- Check input file has data
- Verify skiprows parameter is correct
- Ensure file format is correct

#### Error: "KeyError: 'Deal Status'"
**Solution:**
- Check column names in input file
- Ensure "Deal Status" column exists in training data
- Verify column name spelling and case

### 11. Windows-Specific Issues

#### Error: "streamlit: command not found"
**Solution:**
```bash
# Use python module syntax
python -m streamlit run app.py
```

#### Error: "uvicorn: command not found"
**Solution:**
```bash
# Use python module syntax
python -m uvicorn api:app --reload
```

#### Error: Path issues with backslashes
**Solution:**
- Code already uses os.path.join for cross-platform compatibility
- If manually entering paths, use forward slashes: `data/input/file.xlsx`

### 12. Browser Issues

#### Issue: Swagger UI not loading
**Solution:**
1. Clear browser cache
2. Try different browser
3. Check if API is running
4. Verify URL: http://localhost:8000/swagger

#### Issue: Streamlit not opening automatically
**Solution:**
1. Manually open: http://localhost:8501
2. Check if port is correct
3. Verify Streamlit is running

## Quick Fixes

### Reset Everything
```bash
# Stop all running processes (Ctrl+C in terminals)

# Reinstall dependencies
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# Restart applications
python api.py  # Terminal 1
python -m streamlit run app.py  # Terminal 2
```

### Clean Start
```bash
# Delete generated files
rm -rf data/output/*
rm -rf models/*

# Regenerate everything
python src/generate_synthetic_data.py
python src/train_xgb_classifier.py
python src/predict_xgb_classifier.py
```

### Verify Installation
```bash
# Check Python version (should be 3.10+)
python --version

# Check installed packages
pip list | grep -E "pandas|streamlit|fastapi|xgboost"

# Verify project structure
python scripts/verify_structure.py
```

## Getting Help

### Check Logs
1. **API Logs**: Check terminal running `python api.py`
2. **Streamlit Logs**: Check terminal running `streamlit run app.py`
3. **Browser Console**: F12 → Console tab

### Debug Mode

#### Enable Streamlit Debug Mode:
```bash
streamlit run app.py --logger.level=debug
```

#### Enable FastAPI Debug Mode:
```bash
uvicorn api:app --reload --log-level debug
```

### Common Log Locations
- **Streamlit**: Terminal output
- **FastAPI**: Terminal output
- **Browser**: F12 → Console

## Prevention Tips

1. **Use Virtual Environment**: Isolate dependencies
2. **Keep Dependencies Updated**: Regular `pip install --upgrade`
3. **Check File Formats**: Ensure Excel files are valid
4. **Monitor Resources**: Watch CPU/Memory usage
5. **Regular Backups**: Save important data files
6. **Version Control**: Use Git for code changes

## Still Having Issues?

1. Check the error message carefully
2. Search for the error in this guide
3. Check the README.md for setup instructions
4. Review the API documentation at /swagger
5. Verify all dependencies are installed
6. Try the Quick Fixes section above

## Contact Support

If issues persist:
1. Note the exact error message
2. Check which step fails
3. Verify system requirements
4. Review installation steps
5. Open an issue with details

---

**Last Updated**: November 2025  
**Version**: 1.0.0
