# Docker Installation and Setup Guide

## 📋 Prerequisites

Before building Docker images, you need to install Docker Desktop.

### Install Docker Desktop for Windows

1. **Download Docker Desktop**
   - Visit: https://www.docker.com/products/docker-desktop
   - Click "Download for Windows"

2. **System Requirements**
   - Windows 10 64-bit: Pro, Enterprise, or Education (Build 19041 or higher)
   - OR Windows 11 64-bit
   - WSL 2 feature enabled
   - 4GB RAM minimum (8GB recommended)

3. **Install Docker Desktop**
   - Run the installer
   - Follow the installation wizard
   - Enable WSL 2 when prompted
   - Restart your computer

4. **Verify Installation**
   ```powershell
   docker --version
   docker-compose --version
   ```

## 🚀 Quick Start (After Docker Installation)

### Option 1: Automated Build and Run (Recommended)

```powershell
# Navigate to docker folder
cd docker

# Build images
.\build.ps1

# Run containers
.\run.ps1
```

### Option 2: Manual Build and Run

```powershell
# Build Streamlit UI
docker build -f docker/Dockerfile.streamlit -t deal-win-probability-ui .

# Build FastAPI
docker build -f docker/Dockerfile.api -t deal-win-probability-api .

# Run with docker-compose
cd docker
docker-compose up -d
```

## 📁 Docker Folder Structure

```
docker/
├── Dockerfile.streamlit      # Streamlit UI container definition
├── Dockerfile.api            # FastAPI backend container definition
├── docker-compose.yml        # Multi-container orchestration
├── build.ps1                 # Automated build script
├── run.ps1                   # Automated run script
├── README.md                 # Docker usage guide
└── INSTALL.md               # This file
```

## 🐳 What Gets Built

### Streamlit UI Image
- **Name**: `deal-win-probability-ui:latest`
- **Base**: Python 3.11-slim
- **Size**: ~1.2 GB
- **Port**: 8501
- **Purpose**: Interactive web interface for predictions

### FastAPI Image
- **Name**: `deal-win-probability-api:latest`
- **Base**: Python 3.11-slim
- **Size**: ~1.1 GB
- **Port**: 8000
- **Purpose**: REST API for programmatic access

## 🔧 Configuration

### Environment Variables

You can customize the containers using environment variables in `docker-compose.yml`:

```yaml
environment:
  - PYTHONUNBUFFERED=1
  - STREAMLIT_SERVER_PORT=8501
  - STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

### Volume Mounts

Data and models are mounted as volumes for persistence:

```yaml
volumes:
  - ../data:/app/data
  - ../models:/app/models
```

## 🌐 Accessing the Application

After running the containers:

- **Streamlit UI**: http://localhost:8501
- **FastAPI Backend**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **API Redoc**: http://localhost:8000/redoc

## 📊 Managing Containers

### View Running Containers
```powershell
docker ps
# or
cd docker && docker-compose ps
```

### View Logs
```powershell
# All logs
cd docker && docker-compose logs -f

# Streamlit only
docker logs -f deal-win-probability-ui

# API only
docker logs -f deal-win-probability-api
```

### Stop Containers
```powershell
cd docker && docker-compose stop
```

### Restart Containers
```powershell
cd docker && docker-compose restart
```

### Remove Containers
```powershell
# Stop and remove
cd docker && docker-compose down

# Remove with volumes
cd docker && docker-compose down -v
```

## 🐛 Troubleshooting

### Docker Desktop Not Starting
- Ensure WSL 2 is installed and enabled
- Check Windows features: Hyper-V and Containers
- Restart Docker Desktop service

### Build Fails
```powershell
# Clear Docker cache
docker system prune -a

# Rebuild without cache
docker build --no-cache -f docker/Dockerfile.streamlit -t deal-win-probability-ui .
```

### Port Already in Use
```powershell
# Find process using port
netstat -ano | findstr :8501

# Change port in docker-compose.yml
ports:
  - "8502:8501"  # Use 8502 instead
```

### Container Won't Start
```powershell
# Check logs
docker logs deal-win-probability-ui

# Inspect container
docker inspect deal-win-probability-ui

# Check health
docker ps -a
```

### Volume Mount Issues
- Ensure Docker Desktop has access to the drive
- Settings → Resources → File Sharing
- Add the project directory

## 🔒 Security Best Practices

1. **Don't run as root** (already configured in Dockerfiles)
2. **Scan for vulnerabilities**:
   ```powershell
   docker scan deal-win-probability-ui
   ```
3. **Keep images updated**:
   ```powershell
   docker pull python:3.11-slim
   .\build.ps1
   ```
4. **Use secrets for sensitive data** (not hardcoded in images)

## 📦 Deploying to Cloud

### Push to Docker Hub
```powershell
# Login
docker login

# Tag
docker tag deal-win-probability-ui:latest yourusername/deal-win-ui:latest

# Push
docker push yourusername/deal-win-ui:latest
```

### Deploy to AWS ECS, Google Cloud Run, or Azure
See `docs/DEPLOYMENT.md` for detailed cloud deployment instructions.

## 💡 Tips

1. **Faster Builds**: Use `.dockerignore` to exclude unnecessary files
2. **Smaller Images**: Multi-stage builds (already implemented)
3. **Development**: Mount code as volume for live reload
4. **Production**: Build optimized images without dev dependencies

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Best Practices](https://docs.docker.com/develop/dev-best-practices/)
