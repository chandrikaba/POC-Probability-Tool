# Deployment Guide for Deal Win Probability Tool

## 🚀 Streamlit Community Cloud Deployment (Recommended)

Streamlit Community Cloud is the easiest way to deploy this application for free.

### Prerequisites
1. A GitHub account
2. Your code pushed to a GitHub repository

### Steps to Deploy

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

2. **Go to Streamlit Community Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io/)
   - Sign in with your GitHub account

3. **Deploy your app**
   - Click "New app"
   - Select your repository
   - Set the main file path: `app.py`
   - Click "Deploy"

4. **Configuration**
   - The `.streamlit/config.toml` file is automatically detected
   - Dependencies from `requirements.txt` are automatically installed
   - Python version is set in `runtime.txt`

### Important Notes for Streamlit Cloud

- **File Persistence**: Streamlit Cloud has ephemeral storage. Generated models and predictions will be lost on restart.
- **Solution**: Consider using:
  - Streamlit Secrets for API keys
  - Cloud storage (AWS S3, Google Cloud Storage) for persistent data
  - Pre-trained models committed to the repository

---

## 🐳 Docker Deployment (Alternative)

For self-hosted deployments or cloud platforms that support Docker.

### Build and Run with Docker

```bash
# Build the image
docker build -t deal-win-probability .

# Run the container
docker run -p 8501:8501 deal-win-probability
```

### Using Docker Compose (Both UI and API)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Access the application:**
- Streamlit UI: http://localhost:8501
- FastAPI: http://localhost:8000

---

## ☁️ Cloud Platform Deployments

### AWS (Elastic Beanstalk)
```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p docker deal-win-probability

# Create environment and deploy
eb create deal-win-env
eb open
```

### Google Cloud Run
```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/deal-win-probability

# Deploy to Cloud Run
gcloud run deploy deal-win-probability \
  --image gcr.io/PROJECT_ID/deal-win-probability \
  --platform managed \
  --port 8501
```

### Azure Container Instances
```bash
# Build and push to Azure Container Registry
az acr build --registry REGISTRY_NAME --image deal-win-probability .

# Deploy to ACI
az container create \
  --resource-group RESOURCE_GROUP \
  --name deal-win-probability \
  --image REGISTRY_NAME.azurecr.io/deal-win-probability \
  --dns-name-label deal-win-app \
  --ports 8501
```

---

## 📦 Environment Variables (Optional)

If you need to configure environment variables:

### For Streamlit Cloud
Add secrets in the Streamlit Cloud dashboard under "Settings" → "Secrets"

### For Docker
Create a `.env` file:
```env
PYTHONUNBUFFERED=1
MODEL_PATH=/app/models/xgb_classifier.pkl
DATA_PATH=/app/data
```

Then update `docker-compose.yml`:
```yaml
env_file:
  - .env
```

---

## 🔒 Security Considerations

1. **Never commit sensitive data** to the repository
2. Use `.gitignore` to exclude:
   - `*.pkl` (model files if they contain sensitive data)
   - `.env` files
   - API keys
3. For production, add authentication (e.g., Streamlit-Authenticator)
4. Use HTTPS in production

---

## 📊 Monitoring and Logs

### Streamlit Cloud
- View logs in the Streamlit Cloud dashboard
- Monitor app health and resource usage

### Docker
```bash
# View logs
docker logs deal-win-probability-ui

# Monitor resource usage
docker stats
```

---

## 🛠️ Troubleshooting

### Common Issues

**Issue**: App crashes on Streamlit Cloud
- **Solution**: Check logs for missing dependencies, add them to `requirements.txt`

**Issue**: Models not found
- **Solution**: Pre-generate and commit models to the repository, or implement cloud storage

**Issue**: Out of memory
- **Solution**: Reduce model size, optimize data processing, or upgrade to a paid tier

---

## 📚 Additional Resources

- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-community-cloud)
- [Docker Documentation](https://docs.docker.com/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
