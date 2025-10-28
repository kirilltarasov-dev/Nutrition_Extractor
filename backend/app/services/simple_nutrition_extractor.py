"""Simple nutrition extractor - works with any PDF"""
import time
import logging
from typing import Dict
from app.models.schemas import AllergenData, NutritionData
from app.services.pdf_processor import PDFProcessor
from app.services.universal_extraction_service import UniversalExtractionService

class SimpleNutritionExtractor:
    """Extracts allergens and nutrients from PDF documents"""
    
    def __init__(self):
        self.pdf_processor = PDFProcessor()
        self.extraction_service = UniversalExtractionService()
        self.logger = logging.getLogger(__name__)
    
    async def extract_from_pdf(self, pdf_data: bytes, gemini_key: str) -> Dict:
        """Extract allergens and nutrients from PDF bytes"""
        start_time = time.time()
        
        try:
            # Extract text from PDF (with OCR support)
            text = await self.pdf_processor.extract_text_from_pdf(pdf_data)
            self.logger.info(f"Extracted text: {len(text)} chars")
            self.logger.info(f"First 500 chars of extracted text: {text[:500]}")
            
            # Clean text
            clean_text = self.extraction_service.clean_text(text)
            self.logger.info(f"Cleaned text: {len(clean_text)} chars")
            self.logger.info(f"First 500 chars of cleaned text: {clean_text[:500]}")
            
            # Try LLM first for both allergens and nutrients
            allergens, nutrients = {}, {}
            llm_used = False
            try:
                llm_allergens, llm_nutrients = await self._try_gemini(clean_text, gemini_key)
                
                self.logger.info(f"LLM returned: allergens={llm_allergens}, nutrients={llm_nutrients}")
                
                # Validate LLM results
                if llm_allergens:
                    # Check for true values (handle both bool True and string "true")
                    def is_true_value(v):
                        return v is True or (isinstance(v, str) and v.lower() in ('true', 'yes', '1', 'igen', 'contains'))
                    
                    true_count = sum(1 for v in llm_allergens.values() if is_true_value(v))
                    true_list = [k for k, v in llm_allergens.items() if is_true_value(v)]
                    self.logger.warning(f"LLM returned {true_count}/10 allergens as TRUE: {true_list}")
                    
                    # Check if nutrients are all N/A (LLM didn't extract anything useful)
                    nutrients_all_na = all(v == "N/A" or v is None or v == "" for v in llm_nutrients.values()) if llm_nutrients else True
                    
                    # If LLM returns all false and all N/A, it failed to parse - use fallback
                    if true_count == 0 and nutrients_all_na:
                        self.logger.error("LLM returned ALL FALSE allergies AND ALL N/A nutrients - parsing failed, using fallback")
                        llm_allergens = None
                        llm_nutrients = None
                    # If too many allergens are true (>5), also use fallback (checking for false positives when ALL are true)
                    elif true_count > 5:
                        self.logger.warning(f"SUSPICIOUS! LLM says {true_count} allergens present (likely false positive), using regex fallback instead")
                        llm_allergens = None
                        llm_nutrients = None
                    # If all nutrients are N/A, use fallback
                    elif nutrients_all_na:
                        self.logger.warning("LLM returned all nutrients as N/A, using regex fallback instead")
                        llm_allergens = None
                        llm_nutrients = None
                
                if llm_allergens and llm_nutrients:
                    allergens = llm_allergens
                    nutrients = llm_nutrients
                    llm_used = True
                    self.logger.info("Using LLM results for both allergens and nutrients")
                    
                    # Post-process: Try to extract missing values from fallback
                    missing_items = []
                    for key in ["protein", "sodium", "sugar"]:
                        if nutrients.get(key) == "N/A":
                            missing_items.append(key)
                    
                    if missing_items:
                        self.logger.warning(f"LLM returned N/A for {missing_items}, trying to extract from fallback patterns")
                        try:
                            # Run fallback just for missing items
                            _, fallback_nutrients = self.extraction_service.advanced_fallback(clean_text)
                            for key in missing_items:
                                if fallback_nutrients.get(key) != "N/A":
                                    nutrients[key] = fallback_nutrients[key]
                                    self.logger.warning(f"Found {key} value from fallback: {nutrients[key]}")
                        except Exception as e:
                            self.logger.debug(f"Fallback check failed: {e}")
                else:
                    # LLM returned empty or suspicious results, use fallback
                    self.logger.info("LLM returned empty or suspicious results, using fallback")
                    allergens, nutrients = self.extraction_service.advanced_fallback(clean_text)
            except Exception as e:
                self.logger.info(f"LLM failed: {e}, using fallback")
                allergens, nutrients = self.extraction_service.advanced_fallback(clean_text)
            
            # Validate results
            final_allergens = self._validate_allergens(allergens)
            final_nutrients = self._validate_nutrients(nutrients)
            
            processing_time = time.time() - start_time
            
            return {
                "success": True,
                "allergens": AllergenData(**final_allergens).model_dump(),
                "nutrients": NutritionData(**final_nutrients).model_dump(),
                "llm_used": "gemini" if llm_used else "regex_fallback",
                "extracted_text": clean_text,
                "processing_time": processing_time
            }
            
        except Exception as e:
            self.logger.error(f"Extraction error: {e}")
            return self._create_error_response(f"Extraction failed: {str(e)}")
    
    async def _try_gemini(self, text: str, gemini_key: str):
        """Try to use Gemini for nutrient extraction only"""
        try:
            return await self.extraction_service.extract_with_gemini(text, gemini_key)
        except Exception as e:
            self.logger.info(f"Gemini extraction failed: {e}")
            return {}, {}
    
    def _validate_allergens(self, allergens: Dict) -> Dict:
        """Validate allergen values"""
        # Initialize default allergens
        validated = {
            "gluten": False,
            "egg": False,
            "crustaceans": False,
            "fish": False,
            "peanut": False,
            "soy": False,
            "milk": False,
            "tree_nuts": False,
            "celery": False,
            "mustard": False
        }
        
        # Update with validated values
        for allergen in validated.keys():
            value = allergens.get(allergen)
            if isinstance(value, bool):
                validated[allergen] = value
        
        return validated
    
    def _validate_nutrients(self, nutrients: Dict) -> Dict:
        """Validate nutrient values"""
        validated = {
            "energy": "N/A",
            "fat": "N/A",
            "carbohydrate": "N/A",
            "sugar": "N/A",
            "protein": "N/A",
            "sodium": "N/A"
        }
        
        for nutrient in validated.keys():
            value = nutrients.get(nutrient)
            if value and value != "N/A":
                validated[nutrient] = value
        
        return validated
    
    def _create_error_response(self, error_msg: str) -> Dict:
        """Create error response"""
        return {
            "success": False,
            "error": error_msg,
            "allergens": AllergenData().model_dump(),
            "nutrients": NutritionData().model_dump(),
            "llm_used": "gemini",
            "extracted_text": "",
            "processing_time": 0
        }
