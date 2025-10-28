from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging_config import setup_logging
from app.api.endpoints import router
import logging

# Configure logging
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API for extracting allergens and nutritional values from PDF documents",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS
if settings.BACKEND_CORS_ORIGINS == ["*"]:
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=".*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {
        "message": "Nutrition Extractor API",
        "version": settings.VERSION,
        "description": "API для извлечения аллергенов и пищевой ценности из PDF документов"
    }

@app.get("/health")
async def health_check():
    logger.info(" Health check endpoint accessed")
    return {"status": "healthy", "version": settings.VERSION}