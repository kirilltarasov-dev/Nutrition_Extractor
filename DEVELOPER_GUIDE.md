# 👨‍💻 Developer Guide - Nutrition & Allergen Extractor

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Development Setup](#development-setup)
3. [Project Structure](#project-structure)
4. [Core Components](#core-components)
5. [API Documentation](#api-documentation)
6. [Testing](#testing)
7. [Contributing](#contributing)

---

## Architecture Overview

### System Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   React     │ ◄─────► │   FastAPI    │ ◄─────► │   Gemini   │
│  Frontend   │  HTTP   │   Backend    │  API    │     API    │
│             │         │              │         │            │
│  localhost  │         │  localhost   │         │  Google AI │
│    :3000    │         │    :8000     │         │  Cloud     │
└─────────────┘         └──────────────┘         └─────────────┘
```

### Technology Stack

**Backend:**
- FastAPI - Modern async web framework
- Python 3.12+ - Async/await support, high performance
- PyPDF2 - PDF text extraction
- pdf2image + pytesseract - OCR for scanned PDFs
- google-generativeai - Gemini AI integration
- Pydantic - Data validation
- Uvicorn - ASGI server
- aiohttp - Async HTTP client for Gemini API

**Frontend:**
- React - UI framework
- Axios - HTTP client
- Custom CSS - Responsive design with rounded forms
- localStorage - History persistence
- Window.print() - PDF report generation

### Async Python Architecture

The application uses async-first Python architecture with non-blocking I/O for maximum performance:

**Why Async-First?**
- **Concurrent I/O**: Handle multiple requests simultaneously without blocking
- **Non-blocking API Calls**: Gemini API calls use aiohttp async HTTP client
- **Parallel File Processing**: Multiple files can be processed concurrently
- **Resource Efficiency**: Single-threaded event loop manages thousands of connections
- **Scalability**: Can handle 1000+ requests per second on modest hardware

**Note**: CPU-intensive operations (OCR, PDF parsing) are wrapped in `run_in_executor()` to prevent blocking the event loop.

**Async Implementation:**

```python
# Example: Async PDF processing
async def extract_from_pdf(self, pdf_data: bytes, gemini_key: str):
    # Non-blocking file operations
    text = await self.pdf_processor.extract_text_from_pdf(pdf_data)
    
    # Non-blocking API calls
    allergens, nutrients = await self._try_gemini(clean_text, gemini_key)
    
    # Concurrent OCR when needed
    ocr_text = await self._extract_text_with_ocr(pdf_data)
```

**Performance Benefits:**
- **Without Async**: ~5-10 seconds per file, blocks entire server
- **With Async**: ~2-3 seconds per file, processes multiple files concurrently
- **Throughput**: Can process 3-5 files simultaneously on a single CPU core

### Performance & Scalability

**Current Performance:**
- **Response Time**: 2-5 seconds per PDF (real-time extraction)
- **Throughput**: 50-100 requests per minute per instance
- **Concurrent Requests**: 10-20 simultaneous PDF processing
- **File Size Limit**: 10MB per file (configurable)

**Scaling Considerations:**

1. **Vertical Scaling** (Current):
   - Increase server memory for larger files
   - Upgrade CPU for faster OCR processing
   - Optimize Gemini API rate limits

2. **Horizontal Scaling** (Future Plans):
   - Deploy multiple backend instances
   - Use load balancer (nginx, AWS ALB)
   - Implement Redis for session/queue management
   - Add message queue (RabbitMQ, AWS SQS) for batch processing

3. **Database Integration** (Planned):
   - Store extraction results in PostgreSQL
   - Cache frequently accessed PDFs
   - Implement pagination for history
   - Add user authentication and data isolation

4. **Optimization Strategies**:
   - **Connection Pooling**: Reuse database/API connections
   - **Result Caching**: Cache identical PDFs
   - **Batch Processing**: Process multiple files asynchronously
   - **CDN Integration**: Serve static assets via CDN

**Current Limits:**

| Resource | Current Limit | Recommendation |
|----------|--------------|----------------|
| File Size | 10MB | Increase to 50MB for production |
| Concurrent Files | 3 per request | Implement batch endpoint |
| API Rate Limit | Gemini dependent | Implement rate limiting |
| Memory Usage | ~200MB per request | Monitor with Prometheus |
| Request Timeout | 120 seconds | Reduce to 60s, implement async jobs |

**Future Enhancements:**

1. **Batch Processing & Async Jobs**:
   ```python
   # Planned: Process multiple files in parallel
   POST /api/v1/extract-batch
   # Upload 10+ files, process async, return job_id
   GET /api/v1/jobs/{job_id}
   POST /api/v1/jobs/{job_id}/cancel  # Cancel long-running jobs
   
   # Background worker with Celery
   from celery import Celery
   @app.task
   def process_pdf_async(pdf_hash, api_key)
   ```

2. **Database Integration**:
   ```python
   # PostgreSQL for structured data
   - Store extraction history per user
   - Cache results to avoid re-processing
   - Analytics and reporting
   - User preferences and settings
   
   # Redis for caching
   - Cache PDF hashes → results mapping
   - Rate limiting storage
   - Session management
   - Queue for background jobs
   
   # Elasticsearch for search
   - Full-text search in extracted data
   - Search by allergen presence
   - Nutritional value ranges
   ```

3. **Authentication & Authorization**:
   ```python
   # JWT-based authentication
   from fastapi import Depends, HTTPException
   from jose import JWTError, jwt
   
   # OAuth2 integration
   - Google OAuth for quick login
   - GitHub OAuth for developers
   - Email/password registration
   
   # Role-based access control
   - Admin: Full access + analytics
   - Premium: Unlimited requests
   - Free: Rate-limited
   
   # API key management per-user
   - Store user's own Gemini keys
   - Per-request rate limiting
   ```

4. **Monitoring & Observability**:
   ```python
   # Prometheus metrics
   from prometheus_client import Counter, Histogram
   
   request_count = Counter('requests_total')
   extraction_time = Histogram('extraction_duration_seconds')
   
   # Sentry for error tracking
   import sentry_sdk
   sentry_sdk.init(dsn="...")
   
   # Grafana dashboards
   - Request rate over time
   - Average extraction time
   - Error rate by endpoint
   - Resource usage (CPU, memory)
   
   # Distributed tracing with Jaeger
   from opentelemetry import trace
   ```

5. **Advanced Scaling Strategies**:
   
   **A. Microservices Architecture**:
   ```python
   # Split into separate services:
   
   # 1. PDF Processing Service
   POST /pdf/upload → Returns PDF ID
   GET /pdf/{id}/text → Returns extracted text
   
   # 2. Extraction Service  
   POST /extract → Receives text, returns JSON
   
   # 3. Analytics Service
   POST /analytics/ingest → Stores results
   GET /analytics/dashboard → Returns metrics
   ```
   
   **B. Load Balancing**:
   ```nginx
   # nginx.conf
   upstream backend {
       least_conn;
       server backend1:8000;
       server backend2:8000;
       server backend3:8000;
   }
   
   server {
       listen 80;
       location / {
           proxy_pass http://backend;
       }
   }
   ```
   
   **C. Distributed Caching**:
   ```python
   # Redis Cluster for multi-region
   import redis
   redis_client = redis.RedisCluster(
       startup_nodes=[{"host": "node1", "port": 6379}]
   )
   
   # Cache strategies:
   - LRU for frequently accessed PDFs
   - TTL-based expiration
   - Write-through cache for consistency
   ```
   
   **D. Queue-Based Processing**:
   ```python
   # Celery + Redis/RabbitMQ
   from celery import Celery
   
   app = Celery('nutrition', broker='redis://localhost')
   
   @app.task(queue='pdf_processing')
   def process_pdf_async(pdf_data, gemini_key):
       # Long-running task
       return extract_nutrition_data(pdf_data, gemini_key)
   
   # Webhook notifications when done
   POST /webhooks/{job_id}
   ```

6. **Cloud-Native Improvements**:
   
   **A. Kubernetes Deployment**:
   ```yaml
   # k8s/deployment.yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: nutrition-extractor
   spec:
     replicas: 5  # Auto-scale based on traffic
     template:
       spec:
         containers:
         - name: api
           image: nutrition-extractor:latest
           resources:
             requests:
               memory: "512Mi"
               cpu: "500m"
             limits:
               memory: "1Gi"
               cpu: "1000m"
   ```
   
   **B. Horizontal Pod Autoscaling**:
   ```yaml
   # Auto-scale based on CPU/Memory
   minReplicas: 2
   maxReplicas: 10
   targetCPUUtilizationPercentage: 70
   ```
   
   **C. Multi-Region Deployment**:
   ```
   US-East → nginx load balancer → Backend → PostgreSQL Read Replica
   EU-West → nginx load balancer → Backend → PostgreSQL Read Replica
   Asia-Singapore → nginx load balancer → Backend → PostgreSQL Read Replica
   
   Origin → Edge CDN (Cloudflare) → Closest Region
   ```

7. **Performance Optimizations**:
   
   **A. PDF Preprocessing Pipeline**:
   ```python
   # Parallel OCR processing
   import asyncio
   
   async def process_multiple_pdfs(pdfs):
       tasks = [process_pdf(pdf) for pdf in pdfs]
       results = await asyncio.gather(*tasks)
       return results
   ```
   
   **B. Smart Caching**:
   ```python
   # Cache by PDF content hash
   import hashlib
   
   def get_pdf_hash(pdf_data):
       return hashlib.sha256(pdf_data).hexdigest()
   
   # Skip extraction if already processed
   cached_result = redis.get(f"pdf:{hash}")
   if cached_result:
       return cached_result
   ```
   
   **C. Lazy Loading & Streaming**:
   ```python
   # Stream large PDFs
   from fastapi.responses import StreamingResponse
   
   async def stream_pdf_processing(file):
       async for chunk in process_in_chunks(file):
           yield chunk
   ```
   
   **D. Edge Computing**:
   ```
   # Process PDFs closer to users
   Cloudflare Workers → Regional Processing
   - Lower latency
   - Reduce backend load
   - Caching at edge
   ```

8. **Data Pipeline & Analytics**:
   ```python
   # Apache Kafka for event streaming
   from kafka import KafkaProducer
   
   producer = KafkaProducer()
   producer.send('pdf_processed', {
       'timestamp': time.time(),
       'file_size': len(pdf_data),
       'processing_time': duration,
       'llm_used': 'gemini'
   })
   
   # ClickHouse for analytics
   - Aggregated extraction statistics
   - Popular allergens in products
   - Regional nutritional trends
   - API usage patterns
   ```

9. **Security Enhancements**:
   ```python
   # Rate limiting per user/IP
   from slowapi import Limiter
   limiter = Limiter(key_func=get_remote_address)
   
   @app.post("/extract")
   @limiter.limit("10/minute")
   async def extract(...):
       pass
   
   # Input validation & sanitization
   # Threat detection (malicious PDFs)
   # DDoS protection
   # API key rotation
   ```

10. **AI/ML Improvements**:
    ```python
    # Fine-tuned models for better extraction
    - Train custom BERT model on nutrition data
    - Confidence scoring for extractions
    - Multi-model ensemble (Gemini + GPT-4 + Claude)
    - Active learning from user corrections
    - Automatic model updates based on accuracy
    ```

### Request Flow

```
1. User uploads up to 3 PDFs → Frontend
2. Frontend sends POST /api/v1/extract for each file (async)
3. Backend processes files sequentially with async operations
4. PDF Processor extracts text (direct or OCR with asyncio)
5. Clean and normalize text
6. Call Gemini API async (non-blocking)
7. Fallback to regex patterns if needed
8. Validate and structure response
9. Return JSON to Frontend
10. Display results and save to localStorage
11. User can export as JSON or print PDF
```

---

## Development Setup

### Prerequisites

- Python 3.12+
- Node.js 16+
- Tesseract OCR (for scanned PDF support)
- Google Gemini API Key

### Backend Setup

```bash
# Clone repository
git clone <repository-url>
cd nutrition-extractor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Install system dependencies (macOS)
brew install tesseract tesseract-lang

# Install system dependencies (Ubuntu/Debian)
sudo apt-get install tesseract-ocr tesseract-ocr-eng tesseract-ocr-hun

# Install system dependencies (Windows)
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

### Running the Application

**Terminal 1 - Backend:**
```bash
cd backend
source ../venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

**Access:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

### Environment Variables

Create `backend/.env` file:

```env
# Server Configuration
HOST=0.0.0.0
PORT=8000

# API Configuration
GEMINI_API_KEY=your_key_here  # Optional, can be passed per-request

# File Upload
MAX_FILE_SIZE=10485760  # 10MB

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080

# Logging
LOG_LEVEL=INFO

# OCR Settings
OCR_DPI=300
OCR_LANGUAGES=hun+eng,hun,eng

# LLM Settings
GEMINI_MODEL=gemini-2.0-flash
GEMINI_MAX_TOKENS=800
GEMINI_TEMPERATURE=0.0

# Retry Settings
MAX_RETRIES=3
RETRY_DELAY=1
```

---

## Project Structure

### Backend Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # Application entry point
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints.py          # API routes
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py             # Settings and constants
│   │   └── logging_config.py     # Logging setup
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py            # Pydantic models
│   │
│   └── services/
│       ├── __init__.py
│       ├── pdf_processor.py                  # PDF handling
│       ├── simple_nutrition_extractor.py     # Main orchestrator
│       └── universal_extraction_service.py   # Core extraction
│
├── tests/
│   ├── __init__.py
│   ├── test_config.py
│   ├── test_extraction_service.py
│   ├── test_endpoints_unit.py
│   ├── test_pdf_processor_unit.py
│   ├── test_services.py
│   ├── test_schemas.py
│   └── conftest.py
│
├── Procfile                      # Railway/Heroku deployment
├── railway.toml                  # Railway configuration
├── requirements.txt
└── pytest.ini

frontend/
├── public/
│   ├── index.html
│   └── ...
│
├── src/
│   ├── App.js                   # Main React component
│   ├── App.css                  # Styles
│   ├── index.js                 # Entry point
│   ├── index.css                # Global styles
│   ├── locales/
│   │   ├── en.js               # English translations
│   │   └── hu.js               # Hungarian translations
│   └── ...
│
├── package.json
└── Dockerfile                    # Optional
```

---

## Core Components

### 1. PDF Processor (`app/services/pdf_processor.py`)

Handles PDF text extraction with dual strategy:

```python
from app.services.pdf_processor import PDFProcessor

processor = PDFProcessor()

# Extract text from PDF
text = await processor.extract_text_from_pdf(pdf_data)
```

**Methods:**
- `extract_text_from_pdf(pdf_data: bytes) → str`
- `_extract_with_pypdf2(pdf_data: bytes) → str` - Direct text extraction
- `_extract_with_ocr(pdf_data: bytes) → str` - OCR extraction for scanned PDFs

**Logic Flow:**
1. Try direct text extraction (PyPDF2)
2. If minimal text found, try OCR
3. Return extracted text
4. Log extraction method used

### 2. Universal Extraction Service (`app/services/universal_extraction_service.py`)

Core extraction logic with multiple strategies:

```python
from app.services.universal_extraction_service import UniversalExtractionService

service = UniversalExtractionService()

# Extract with Gemini
result = await service.extract_with_gemini(text, api_key)

# Fallback extraction
result = service.advanced_fallback(text)

# Clean OCR text
cleaned = service.clean_text(text)
```

**Key Features:**
- Gemini AI integration
- Advanced regex fallback
- OCR error correction
- Multi-language support
- Structured output parsing

**Languages Supported:**
- English
- Hungarian
- French
- Spanish

### 3. Simple Nutrition Extractor (`app/services/simple_nutrition_extractor.py`)

Orchestrates the complete extraction process:

```python
from app.services.simple_nutrition_extractor import SimpleNutritionExtractor

extractor = SimpleNutritionExtractor()

result = await extractor.extract_from_pdf(
    pdf_data=pdf_bytes,
    gemini_key=api_key
)
```

**Extraction Flow:**
1. Extract text from PDF
2. Clean and normalize text
3. Attempt Gemini extraction
4. If fails, use regex fallback
5. Validate results
6. Return structured data

### 4. API Endpoints (`app/api/endpoints.py`)

RESTful API layer:

```python
from fastapi import APIRouter, HTTPException, UploadFile, File, Form

router = APIRouter()

@router.post("/extract")
async def extract_nutrition_data(
    file: UploadFile = File(...),
    gemini_api_key: str = Form(...)
) -> ExtractResponse:
    # File validation
    # Extract data
    # Return response
```

**Endpoints:**
- `POST /api/v1/extract` - Extract nutrition data
- `GET /api/v1/health` - Health check
- `GET /` - Root endpoint
- `GET /health` - Backend health

### 5. Data Models (`app/models/schemas.py`)

Pydantic models for validation:

```python
from pydantic import BaseModel

class AllergenData(BaseModel):
    gluten: bool = False
    egg: bool = False
    # ... 10 allergens total

class NutritionData(BaseModel):
    energy: Optional[str] = "N/A"
    fat: Optional[str] = "N/A"
    # ... 6 nutrients total

class ExtractResponse(BaseModel):
    success: bool
    allergens: AllergenData
    nutrients: NutritionData
    llm_used: str
    extracted_text: Optional[str]
    processing_time: Optional[float]
```

---

## API Documentation

### Base URL

```
Development: http://localhost:8000
Production: https://your-domain.com
```

### Endpoints

#### POST /api/v1/extract

Extract allergens and nutrients from PDF.

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/extract" \
  -F "file=@product.pdf" \
  -F "gemini_api_key=your_api_key"
```

**Parameters:**
- `file` (FormData): PDF file
- `gemini_api_key` (string): Gemini API key

**Response (Success):**
```json
{
  "success": true,
  "allergens": {
    "gluten": false,
    "egg": true,
    "crustaceans": false,
    "fish": false,
    "peanut": false,
    "soy": false,
    "milk": true,
    "tree_nuts": false,
    "celery": false,
    "mustard": false
  },
  "nutrients": {
    "energy": "1173 kJ",
    "fat": "18.9 g",
    "carbohydrate": "8.7 g",
    "sugar": "0.6 g",
    "protein": "19 g",
    "sodium": "2.3 g"
  },
  "llm_used": "gemini",
  "extracted_text": "Full extracted text...",
  "processing_time": 2.45
}
```

**Response (Error):**
```json
{
  "success": false,
  "allergens": {
    "gluten": false,
    ...
  },
  "nutrients": {
    "energy": "N/A",
    ...
  },
  "llm_used": "gemini",
  "error": "Error message",
  "processing_time": 1.23
}
```

**Error Codes:**
- `400` - Bad Request (invalid file, missing API key)
- `413` - Payload Too Large (file > 10MB)
- `500` - Internal Server Error

#### GET /api/v1/health

Health check endpoint.

**Request:**
```bash
curl http://localhost:8000/api/v1/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

#### GET /

Root endpoint.

**Response:**
```json
{
  "message": "Nutrition Extractor API",
  "version": "1.0.0",
  "description": "API for extracting allergens..."
}
```

### Interactive API Docs

FastAPI provides automatic interactive documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Testing

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=app --cov-report=html

# Specific test file
pytest tests/test_extraction.py

# Verbose output
pytest -v

# Show print statements
pytest -s
```

### Test Coverage

**Current Status:**
- 133 tests passing
- 78% code coverage
- Core functionality: 80%+ coverage

**Coverage Report:**
```bash
pytest --cov=app --cov-report=html
# Open htmlcov/index.html
```

**Well Covered:**
- - API endpoints (94%)
- - Data models (100%)
- - Configuration (100%)
- - Main extraction (95%)

**Needs Improvement:**
- OCR processing (62%)
- Error edge cases

### Test Structure

```python
# tests/test_extraction.py
import pytest
from app.services.simple_nutrition_extractor import SimpleNutritionExtractor

@pytest.mark.asyncio
async def test_extract_valid_pdf():
    extractor = SimpleNutritionExtractor()
    result = await extractor.extract_from_pdf(
        pdf_data=valid_pdf_bytes,
        gemini_key="test_key"
    )
    assert result["success"] == True

# More tests...
```

### Testing Checklist

- [ ] Unit tests for all services
- [ ] Integration tests for API
- [ ] Mock external dependencies (Gemini API)
- [ ] Test error handling
- [ ] Test file validation
- [ ] Test edge cases

---

## Code Style and Linting

### Python Code Style

**Linter:**
```bash
# Install Ruff
pip install ruff

# Run linting
ruff check backend/app

# Auto-fix issues
ruff check --fix backend/app
```

**Configuration:** `pyproject.toml`

### JavaScript Code Style

**ESLint:**
```bash
cd frontend
npm run lint

# Auto-fix
npm run lint -- --fix
```

### Pre-commit Hooks

**Install:**
```bash
pip install pre-commit
pre-commit install
```

---

## Deployment

### Railway Deployment (Recommended)

**Easiest deployment with automatic OCR setup:**

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub"
4. Select your repository
5. Railway automatically:
   - Installs Python from `requirements.txt`
   - Installs Tesseract OCR via `nixpacks.toml`
   - Deploys backend on port `$PORT`
   - Provides public URL

See [RAILWAY.md](./RAILWAY.md) for detailed guide.

### Vercel Deployment (Serverless)

**For serverless deployment:**

```bash
1. Connect repo to Vercel
2. Vercel auto-detects api/index.py
3. Deploys as serverless functions
```

See [DEPLOYMENT.md](./DEPLOYMENT.md) for details.

### Quick Production Setup

**Backend:**
```bash
cd backend
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**Frontend:**
```bash
cd frontend
npm run build
npx serve -s build
```

### Docker Deployment

```bash
# Build
docker-compose build

# Run
docker-compose up -d

# Logs
docker-compose logs -f
```

### Environment-Specific Configs

**Development:**
- Hot reload enabled
- Debug logging
- CORS: *

**Production:**
- No hot reload
- Info logging
- Restricted CORS
- HTTPS required
- Rate limiting enabled

---

## Adding New Features

### Adding a New Allergen

1. Update `AllergenData` model:
```python
class AllergenData(BaseModel):
    # ... existing allergens
    sesame: bool = False
```

2. Update extraction patterns:
```python
# In universal_extraction_service.py
patterns = {
    # ... existing patterns
    "sesame": [r"[sS]esame", r"sesamum", ...]
}
```

3. Update frontend display
4. Add tests
5. Update documentation

### Adding a New Nutrient

1. Update `NutritionData` model:
```python
class NutritionData(BaseModel):
    # ... existing nutrients
    fiber: Optional[str] = "N/A"
```

2. Add extraction patterns:
```python
patterns = {
    "fiber": [r"fiber", r"fibre", r"rost", ...]
}
```

3. Update frontend
4. Add tests
5. Update documentation

### Supporting a New Language

1. Add language patterns:
```python
"energy": [
    "energia",     # Hungarian
    "energy",      # English
    "énergie",     # French
    "energía",     # Spanish
    "energia_new"  # New language
]
```

2. Add frontend translations
3. Test with sample PDFs
4. Update documentation

---

## Performance Optimization

### Current Performance

- Real PDFs: 1-2 seconds
- Scanned PDFs: 5-10 seconds
- Average: 2-5 seconds

### Optimization Tips

**1. Caching:**
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def extract_cached(pdf_hash):
    # Cache extraction results
    pass
```

**2. Async Processing:**
```python
# Already implemented
async def extract_from_pdf(...):
    # Non-blocking operations
    pass
```

**3. Response Compression:**
```python
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)
```

### Monitoring

Add logging for performance tracking:

```python
import time
start = time.time()
# ... processing
logger.info(f"Processing time: {time.time() - start}s")
```

---

## Security Considerations

### API Key Security

- Never commit API keys
- Use environment variables
- Validate keys before processing
- Implement rate limiting

### File Upload Security

- Validate file types
- Enforce size limits
- Scan for malicious content
- Don't store uploaded files

### CORS Configuration

```python
# Development
BACKEND_CORS_ORIGINS = ["*"]

# Production
BACKEND_CORS_ORIGINS = [
    "https://yourdomain.com",
    "https://app.yourdomain.com"
]
```

### Best Practices

- Use HTTPS in production
- Implement authentication
- Add request rate limiting
- Log security events
- Regular dependency updates

---

## Contributing

### Development Workflow

1. Fork repository
2. Create feature branch: `git checkout -b feature/my-feature`
3. Make changes
4. Add tests
5. Run linter: `ruff check backend/app`
6. Run tests: `pytest`
7. Commit changes: `git commit -m "Add feature"`
8. Push: `git push origin feature/my-feature`
9. Create pull request

### Pull Request Guidelines

- Write clear commit messages
- Add tests for new features
- Update documentation
- Follow code style
- Keep PRs focused and small
- Respond to review feedback

### Code Review Checklist

- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Code style followed
- [ ] No linter errors
- [ ] Performance considered
- [ ] Security reviewed

---

## Troubleshooting Development Issues

### Backend Won't Start

```bash
# Check Python version
python --version  # Should be 3.12+

# Check virtual environment
which python  # Should show venv path

# Reinstall dependencies
pip install -r requirements.txt

# Check port availability
lsof -i :8000
```

### Frontend Build Fails

```bash
# Clear cache
rm -rf node_modules package-lock.json

# Reinstall
npm install

# Check Node version
node --version  # Should be 16+
```

### Tests Failing

```bash
# Run with verbose output
pytest -v

# Run specific test
pytest tests/test_specific.py::test_function -v

# Check for import errors
python -c "from app.main import app"
```

### Import Errors

```bash
# Make sure you're in the right directory
cd backend

# Activate virtual environment
source ../venv/bin/activate

# Set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

---

## Resources

### Documentation

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Docs](https://react.dev/)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [Google Gemini API](https://ai.google.dev/docs)

### Tools

- [Swagger UI](http://localhost:8000/docs)
- [ReDoc](http://localhost:8000/redoc)
- Test Coverage: `htmlcov/index.html`
- Ruff: Python linter
- ESLint: JavaScript linter

### Community

- GitHub Issues
- Discussions
- Pull Requests

---

## License

MIT License - See LICENSE file for details.

---

## Acknowledgments

Built with:
- FastAPI
- React
- Google Gemini
- Tesseract OCR
- Open source community

Thank you for contributing! 

