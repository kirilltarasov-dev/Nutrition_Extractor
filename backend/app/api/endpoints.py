"""API endpoints for nutrition and allergen extraction"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
import logging

from app.services.simple_nutrition_extractor import SimpleNutritionExtractor
from app.models.schemas import ExtractResponse, HealthCheck
from app.core.config import settings

router = APIRouter()
nutrition_extractor = SimpleNutritionExtractor()
logger = logging.getLogger(__name__)

@router.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint"""
    return HealthCheck()

@router.post("/extract", response_model=ExtractResponse)
async def extract_nutrition_data(
    file: UploadFile = File(..., description="PDF file to analyze"),
    gemini_api_key: str = Form(..., description="Your Gemini API key")
):
    """
    Extract allergens and nutrients from uploaded PDF using Gemini.
    
    Args:
        file: PDF file containing product specifications
        gemini_api_key: Google Gemini API key
    
    Returns:
        ExtractResponse with allergens and nutrients
    """
    try:
        # File validation
        if not file.filename or not file.filename.lower().endswith(tuple(settings.ALLOWED_EXTENSIONS)):
            raise HTTPException(400, f"Only {', '.join(settings.ALLOWED_EXTENSIONS)} files are allowed")
        
        # Read file
        pdf_data = await file.read()
        
        if len(pdf_data) == 0:
            raise HTTPException(400, "Empty file")
        
        if len(pdf_data) > settings.MAX_FILE_SIZE:
            raise HTTPException(400, f"File too large (max {settings.MAX_FILE_SIZE / (1024 * 1024):.0f}MB)")
        
        # API key validation
        if not gemini_api_key:
            raise HTTPException(400, "Gemini API key required")
        
        logger.info("Starting extraction with Gemini")
        
        # Data extraction
        result = await nutrition_extractor.extract_from_pdf(
            pdf_data=pdf_data,
            gemini_key=gemini_api_key
        )
        
        logger.info("Extraction completed successfully")
        return ExtractResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Processing error: {str(e)}")
        raise HTTPException(500, f"Processing error: {str(e)}")
