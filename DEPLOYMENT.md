# Deployment Guide

## Quick Deploy

### Railway (Recommended)

Railway is the easiest platform to deploy this application.

**Steps:**

1. **Connect to Railway:**
   - Go to [railway.app](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

2. **Deploy:**
   - Railway will automatically detect Python
   - Uses Nixpacks builder for Tesseract OCR support
   - No additional configuration needed

3. **Access:**
   - Railway provides a public URL
   - Update frontend API URL to the Railway backend URL

**Railway will automatically:**
- Install Python dependencies from `backend/requirements.txt`
- Install Tesseract OCR via `nixpacks.toml`
- Start with: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Configuration Files:**
- `railway.toml` - Railway configuration
- `backend/Procfile` - Start command
- `nixpacks.toml` - System dependencies

See [RAILWAY.md](./RAILWAY.md) for detailed guide.

### Vercel

**Backend:**
- Uses `api/index.py` as serverless handler
- Vercel auto-detects Python functions
- No special configuration needed

**Frontend:**
- Uses `vercel.json` configuration
- Static build served by Vercel
- Environment variables in Vercel dashboard

### Manual Deployment

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run build
npx serve -s build
```

## Environment Variables

### Required:
- None (all settings have defaults)

### Optional:
- `LOG_LEVEL`: INFO, DEBUG, WARNING, ERROR
- `MAX_FILE_SIZE`: 10485760 (10MB)
- `OCR_DPI`: 300

## Production Considerations

1. **CORS:** Configure allowed origins
2. **HTTPS:** Use reverse proxy (nginx)
3. **Rate Limiting:** Implement request throttling
4. **Monitoring:** Add logging and metrics
5. **Scaling:** Consider load balancer

## Troubleshooting

**Port Issues:**
- Railway uses `$PORT` environment variable
- Ensure app listens on `0.0.0.0`

**OCR Not Working:**
- Railway: Automatically installed via Nixpacks
- Other platforms: Install Tesseract system package

**Build Failures:**
- Check `requirements.txt` for all dependencies
- Verify Python version (3.12+)

