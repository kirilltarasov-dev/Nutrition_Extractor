# Nutrition & Allergen Extractor

Automatically extract allergens and nutritional values from PDF documents using AI-powered text extraction.

🌐 **Live Demo:** [https://nutrition_extractor.app/](https://frontend-tau-rosy-29.vercel.app/)

## Documentation

Comprehensive documentation is available for different user types:

- **[Developer Guide](./DEVELOPER_GUIDE.md)** - Technical documentation for developers
- **[Deployment Guide](./DEPLOYMENT.md)** - Deployment instructions for production
- **[Railway Guide](./RAILWAY.md)** - Railway deployment guide
- **[Scaling Roadmap](./SCALING_ROADMAP.md)** - Future scalability plans

## Features

- **PDF Support**: Works with both real PDFs and scanned (image-based) PDFs
- **AI-Powered**: Uses Google Gemini for intelligent data extraction
- **Multi-language**: Supports English and Hungarian (with language switcher)
- **Comprehensive**: Extracts all 10 major allergens and 6 nutritional values
- **Fast**: Processing time typically under 5 seconds
- **Modern UI**: Beautiful, responsive web interface
- **Progress Bar**: Visual feedback during processing
- **API Key Storage**: Saves your Gemini API key in localStorage
- **Language Switcher**: Switch between English and Hungarian

🔗 **Try it now:** [Live Demo](https://frontend-4n40acdm1-kirilltarasovdev-4570s-projects.vercel.app/)

## Extracted Data

### Allergens (10 Major)
- Gluten, Egg, Crustaceans, Fish, Peanut
- Soy, Milk, Tree nuts, Celery, Mustard

### Nutritional Values (6 Core)
- Energy (kJ/kcal), Fat (g), Carbohydrate (g)
- Sugar (g), Protein (g), Sodium (g)

## Quick Start

### Prerequisites

- Python 3.12+ - [Download](https://www.python.org/downloads/)
- Node.js 16+ - [Download](https://nodejs.org/)
- Google Gemini API Key - [Get one here](https://ai.google.dev/)

### Installation

```bash
# 1. Clone the repository
git clone <repository-url>
cd nutrition-extractor

# 2. Setup Backend
cd backend
python -m venv ../venv
source ../venv/bin/activate  # Windows: ..\venv\Scripts\activate
pip install -r requirements.txt

# 3. Setup Frontend
cd ../frontend
npm install
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
- Local: http://localhost:3000
- Live: [https://frontend-4n40acdm1-kirilltarasovdev-4570s-projects.vercel.app/](https://frontend-4n40acdm1-kirilltarasovdev-4570s-projects.vercel.app/)

## 📖 Usage

1. **Enter API Key** - Get your Gemini API key from [Google AI Studio](https://ai.google.dev/)
2. **Upload PDF** - Drag & drop or click to select a PDF file
3. **Extract Data** - Click "Extract Data" button
4. **View Results** - See nutritional values and allergens extracted
5. **Export** - Copy or download results as JSON

For detailed development instructions, see [DEVELOPER_GUIDE.md](./DEVELOPER_GUIDE.md).

## 🔌 API

Interactive API documentation available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Quick API Example

```bash
curl -X POST "http://localhost:8000/api/v1/extract" \
  -F "file=@product.pdf" \
  -F "gemini_api_key=your_api_key"
```

See [DEVELOPER_GUIDE.md](./DEVELOPER_GUIDE.md) for complete API documentation.

## Project Structure

```
nutrition-extractor/
├── api/                  # Vercel serverless handler
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── core/        # Configuration
│   │   ├── models/      # Data models
│   │   └── services/    # Business logic
│   ├── Procfile         # Railway/Heroku deployment
│   ├── railway.toml     # Railway configuration
│   └── tests/           # Test suite
├── frontend/            # React frontend
│   └── src/
│       ├── App.js       # Main component
│       └── locales/     # Translations
├── nixpacks.toml        # System dependencies
├── railway.toml         # Railway config
├── railway.json          # Railway JSON config
├── vercel.json          # Vercel deployment
├── DEVELOPER_GUIDE.md    # Developer documentation
├── DEPLOYMENT.md         # Deployment guide
└── RAILWAY.md           # Railway deployment guide
```

## 🚀 Deployment

### Railway (Recommended)

Quick deployment with automatic OCR setup:

```bash
1. Go to railway.app
2. Connect your GitHub repo
3. Railway automatically:
   - Installs Python dependencies
   - Installs Tesseract OCR
   - Deploys your backend
4. Get public URL
```

See [RAILWAY.md](./RAILWAY.md) for detailed guide.

### Vercel

Serverless deployment:

```bash
1. Connect repo to Vercel
2. Automatic deployment
3. API runs as serverless functions
```

See [DEPLOYMENT.md](./DEPLOYMENT.md) for details.

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# With coverage
pytest --cov=app --cov-report=html

# Frontend tests
cd frontend
npm test
```

**Current Status:**
- 133 tests passing
- 78% code coverage
- Core functionality: 80%+ coverage
- PDF processor: 79%
- Simple extractor: 80%

## Technology Stack

**Backend:**
- FastAPI - Modern Python web framework
- Google Gemini API - AI-powered text extraction
- PyPDF2 - PDF text extraction
- pytesseract - OCR for scanned documents
- Pydantic - Data validation

**Frontend:**
- React - User interface
- Axios - HTTP client
- i18n - Multi-language support

## 📊 Troubleshooting

**Need help?** Check out:
- [DEVELOPER_GUIDE.md - Development Issues](./DEVELOPER_GUIDE.md#troubleshooting-development-issues)
- [DEPLOYMENT.md - Deployment Issues](./DEPLOYMENT.md#troubleshooting)
- [RAILWAY.md - Railway Troubleshooting](./RAILWAY.md#troubleshooting)

Common issues:
- API key errors → Check Gemini API key
- File upload errors → Ensure PDF is < 10MB
- Connection refused → Check backend is running
- Extraction errors → Verify PDF format and quality

## License

MIT License - See LICENSE file for details.

## Contributing

Contributions are welcome! Please see:
1. [DEVELOPER_GUIDE.md](./DEVELOPER_GUIDE.md#contributing) for contribution guidelines
2. Create a feature branch
3. Add tests
4. Submit pull request

## Support

- **Documentation**: See DEVELOPER_GUIDE.md and RAILWAY.md
- **Issues**: Open an issue on GitHub
- **Questions**: Check the troubleshooting sections

## Acknowledgments

- Google Gemini for AI-powered extraction
- FastAPI for the excellent web framework
- React community for amazing tools
- All open source contributors
