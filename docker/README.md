# Docker Build and Run Scripts

## 🐳 Quick Start

### Build and Run Streamlit UI Only
```bash
cd docker
docker build -f Dockerfile.streamlit -t deal-win-probability-ui ..
docker run -p 8501:8501 -v ../data:/app/data -v ../models:/app/models deal-win-probability-ui
```

### Build and Run FastAPI Only
```bash
cd docker
docker build -f Dockerfile.api -t deal-win-probability-api ..
docker run -p 8000:8000 -v ../data:/app/data -v ../models:/app/models deal-win-probability-api
```

### Build and Run Both Services (Recommended)
```bash
cd docker
docker-compose up -d
```

## 📋 Available Commands

### Build Images
```bash
# Build Streamlit UI
docker build -f docker/Dockerfile.streamlit -t deal-win-probability-ui .

# Build FastAPI
docker build -f docker/Dockerfile.api -t deal-win-probability-api .

# Build both with docker-compose
cd docker && docker-compose build
```

### Run Containers
```bash
# Run Streamlit UI
docker run -d -p 8501:8501 --name ui deal-win-probability-ui

# Run FastAPI
docker run -d -p 8000:8000 --name api deal-win-probability-api

# Run both with docker-compose
cd docker && docker-compose up -d
```

### View Logs
```bash
# Streamlit logs
docker logs -f deal-win-probability-ui

# API logs
docker logs -f deal-win-probability-api

# All logs with docker-compose
cd docker && docker-compose logs -f
```

### Stop and Remove
```bash
# Stop containers
docker stop deal-win-probability-ui deal-win-probability-api

# Remove containers
docker rm deal-win-probability-ui deal-win-probability-api

# Stop and remove with docker-compose
cd docker && docker-compose down

# Remove with volumes
cd docker && docker-compose down -v
```

## 🌐 Access the Application

After running the containers:
- **Streamlit UI**: http://localhost:8501
- **FastAPI Backend**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🔧 Advanced Usage

### Build with Custom Tag
```bash
docker build -f docker/Dockerfile.streamlit -t myregistry/deal-win-ui:v1.0 .
```

### Run with Environment Variables
```bash
docker run -p 8501:8501 \
  -e PYTHONUNBUFFERED=1 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/models:/app/models \
  deal-win-probability-ui
```

### Push to Docker Registry
```bash
# Tag the image
docker tag deal-win-probability-ui myregistry/deal-win-ui:latest

# Push to registry
docker push myregistry/deal-win-ui:latest
```

### Run with Docker Compose in Production
```bash
cd docker
docker-compose -f docker-compose.yml up -d --build
```

## 🐛 Troubleshooting

### Container won't start
```bash
# Check logs
docker logs deal-win-probability-ui

# Inspect container
docker inspect deal-win-probability-ui
```

### Port already in use
```bash
# Find process using port 8501
netstat -ano | findstr :8501

# Kill the process or use different port
docker run -p 8502:8501 deal-win-probability-ui
```

### Volume mount issues on Windows
```bash
# Use absolute paths
docker run -p 8501:8501 -v C:/path/to/data:/app/data deal-win-probability-ui
```

## 📦 Image Size Optimization

Current image sizes:
- Streamlit UI: ~1.2 GB
- FastAPI: ~1.1 GB

To reduce size:
1. Use multi-stage builds
2. Remove unnecessary dependencies
3. Use Alpine-based images (requires compilation of some packages)

## 🔒 Security Best Practices

1. **Don't run as root**: Add a non-root user in Dockerfile
2. **Scan for vulnerabilities**: 
   ```bash
   docker scan deal-win-probability-ui
   ```
3. **Use specific base image versions**: Avoid `latest` tag
4. **Limit container resources**:
   ```bash
   docker run --memory="512m" --cpus="1.0" deal-win-probability-ui
   ```
