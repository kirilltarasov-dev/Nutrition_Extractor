from pydantic import BaseModel
from typing import Optional

# Removed LLMProvider enum - now only using Gemini
# Removed ExtractRequest - no longer needed

class NutritionData(BaseModel):
    energy: Optional[str] = "N/A"
    fat: Optional[str] = "N/A"
    carbohydrate: Optional[str] = "N/A"
    sugar: Optional[str] = "N/A"
    protein: Optional[str] = "N/A"
    sodium: Optional[str] = "N/A"

class AllergenData(BaseModel):
    gluten: bool = False
    egg: bool = False
    crustaceans: bool = False
    fish: bool = False
    peanut: bool = False
    soy: bool = False
    milk: bool = False
    tree_nuts: bool = False
    celery: bool = False
    mustard: bool = False

class ExtractResponse(BaseModel):
    success: bool
    allergens: AllergenData
    nutrients: NutritionData
    llm_used: str
    extracted_text: Optional[str] = None
    error: Optional[str] = None
    processing_time: Optional[float] = None


class HealthCheck(BaseModel):
    status: str = "healthy"
    version: str = "1.0.0"