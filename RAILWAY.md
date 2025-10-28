# Railway Deployment Guide

## Quick Start

### 1. Connect to Railway

1. Go to [railway.app](https://railway.app)
2. Sign up / Sign in with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Select your repository: `nutrition-extractor_final_version`

### 2. Deploy Backend

Railway will automatically detect:
- Python project (from `backend/requirements.txt`)
- Uses `nixpacks.toml` for system dependencies (Tesseract OCR)
- Starts with Procfile: `web: cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 3. Environment Variables (Optional)

Railway will use defaults from `app/core/config.py`. If you want to customize:

```bash
LOG_LEVEL=INFO
MAX_FILE_SIZE=10485760
OCR_DPI=300
```

### 4. Get Public URL

Railway provides a public URL like:
```
https://your-app-name.up.railway.app
```

### 5. Update Frontend API URL

Once deployed, update your frontend to use the Railway URL:

```javascript
// In frontend/src/App.js
const API_URL = 'https://your-app-name.up.railway.app/api/v1';
```

## Configuration Files

Railway uses these files:
- `railway.toml` - Railway configuration
- `nixpacks.toml` - System dependencies
- `backend/Procfile` - Start command
- `backend/requirements.txt` - Python dependencies

## What Gets Installed

**Python Packages** (from requirements.txt):
- FastAPI, Uvicorn, PyPDF2, pytesseract, etc.

**System Packages** (from nixpacks.toml):
- tesseract - OCR engine
- poppler_utils - PDF utilities

## Testing Deployment

```bash
# Health check
curl https://your-app-name.up.railway.app/api/v1/health

# Extract test
curl -X POST "https://your-app-name.up.railway.app/api/v1/extract" \
  -F "file=@test.pdf" \
  -F "gemini_api_key=your_key"
```

## Troubleshooting

### OCR Not Working

Railway automatically installs Tesseract via Nixpacks. If issues:
1. Check logs: `railway logs`
2. Verify Tesseract: `railway run tesseract --version`

### Port Conflicts

Railway uses the `$PORT` environment variable. The app should:
```python
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Build Failures

1. Check `requirements.txt` is complete
2. Verify Python version (3.12+)
3. Check Railway logs for errors

## Monitoring

View logs:
```bash
railway logs
```

View metrics:
- CPU Usage
- Memory Usage
- Request Count
- Response Times

## Custom Domain

1. Go to Railway dashboard
2. Click on your service
3. Go to "Settings" → "Domains"
4. Add custom domain
5. Update DNS records

## Cost

Railway offers:
- **Free tier**: $5 credit/month
- **Hobby**: $20/month (includes more resources)
- **Pro**: Enterprise features

For this app, free tier is sufficient.

## Next Steps

1. Deploy backend on Railway
2. Get public URL
3. Deploy frontend separately (or use same Railway project)
4. Configure CORS if needed
5. Test full flow

## Support

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- Project Issues: GitHub Issues

