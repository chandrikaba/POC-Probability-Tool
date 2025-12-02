# Deployment Scripts Documentation

This folder contains scripts to easily deploy, start, and stop the Deal Win Probability Tool application.

## 📁 Folder Structure

```
deployment/
├── deployment.sh       # Setup script for Linux/macOS
├── deployment.bat      # Setup script for Windows
├── start_services.sh   # Start script for Linux/macOS
├── start_services.bat  # Start script for Windows
├── stop_services.sh    # Stop script for Linux/macOS
└── stop_services.bat   # Stop script for Windows
```

## 🚀 Quick Start

### Windows

1. **Setup & Deploy**:
   Double-click `deployment.bat` or run in CMD:
   ```cmd
   deployment.bat
   ```
   This will:
   - Check prerequisites (Python, Docker)
   - Setup virtual environment
   - Install dependencies
   - Create necessary directories

2. **Start Services**:
   Double-click `start_services.bat`:
   ```cmd
   start_services.bat
   ```
   This will start:
   - FastAPI Backend (http://localhost:8000)
   - Streamlit UI (http://localhost:8501)

3. **Stop Services**:
   Double-click `stop_services.bat`:
   ```cmd
   stop_services.bat
   ```

### Linux / macOS

1. **Make scripts executable**:
   ```bash
   chmod +x deployment/*.sh
   ```

2. **Setup & Deploy**:
   ```bash
   ./deployment/deployment.sh
   ```

3. **Start Services**:
   ```bash
   ./deployment/start_services.sh
   ```

4. **Stop Services**:
   ```bash
   ./deployment/stop_services.sh
   ```

## 🐳 Docker Support

All scripts support Docker deployment. When prompted, choose option `1) Docker` to use containerized deployment.

**Prerequisites for Docker:**
- Docker Desktop installed and running
- Docker Compose installed

## 🐍 Native Python Support

If you prefer running directly on your machine, choose option `2) Native Python`.

**Prerequisites for Native:**
- Python 3.10+
- pip

## 🔧 Troubleshooting

- **Port Conflicts**: If ports 8000 or 8501 are in use, the scripts may fail. Edit the scripts to change `API_PORT` or `STREAMLIT_PORT`.
- **Permission Denied**: Ensure scripts have executable permissions (`chmod +x`).
- **Python Not Found**: Ensure Python is added to your system PATH.
