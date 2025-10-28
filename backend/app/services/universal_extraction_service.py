import json
import aiohttp
import re
import logging
from typing import Dict, Tuple

class UniversalExtractionService:
    """
    Universal extraction service that handles all PDF formats from the assignment
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def create_comprehensive_prompt(self, text: str) -> str:
        """Create comprehensive prompt for LLM extraction with better context understanding"""
        return f"""Extract allergens and nutritional values from the following text. Return ONLY valid JSON.

ALLERGEN EXTRACTION:
- Use true/false boolean values
- Mark TRUE for: "+", "I", "X", "Igen", "tartalmaz", "contains", "may contain"
- Mark FALSE for: "-", "N", "Nem", "mentes", "free from", "allergen-free"

ALLERGEN PATTERNS:
- +/I/X/Igen/tartalmaz = TRUE
- -/N/Nem/mentes = FALSE

NUTRITION EXTRACTION:
- Extract ALL nutrients: Energy, Fat, Carbohydrate, Sugar, Protein, Sodium
- NEVER return "N/A" unless truly not found (99% of products have these)
- Look for values in ANY format: "6,9 g", "6.9 g", "6,9", "0,9 g", "0.9 g"
- FAT: Find "Zsír", "Fat", "lipides", "grasas" - extract value like "6,9 g" or "0,9 g"
- CARBOHYDRATE: Find "Szénhidrát", "Carbohydrate" - extract value
- SUGAR: Look for "amelyből cukrok", "cukor", "sugar" - ALWAYS extract if present
- PROTEIN: Look for "Fehérje", "Protein" - extract value
- 
- Ignore only sub-lines like "- ebből telített zsírsavak"

REQUIRED ALLERGENS TO EXTRACT:
- Gluten (wheat, barley, rye, oats, glutén, búza, gluténtartalmú)
- Egg (eggs, egg products, tojás)
- Crustaceans (shellfish, shrimp, crab, lobster, rák, rákfélék)
- Fish (any fish species, hal)
- Peanut (peanuts, groundnuts, mogyoró, földimogyoró)
- Soy (soybeans, soy products, szója, szójabab)
- Milk (dairy, lactose, milk products, tej, laktóz)
- Tree nuts (almonds, walnuts, hazelnuts, etc., dió, diófélék, csonthéjasok)
- Celery (celery root, celery leaves, zeller)
- Mustard (mustard seeds, mustard powder, mustár)

TEXT TO ANALYZE:
{text}

Return ONLY this JSON format:
{{
  "allergens": {{
    "gluten": true/false,
    "egg": true/false,
    "crustaceans": true/false,
    "fish": true/false,
    "peanut": true/false,
    "soy": true/false,
    "milk": true/false,
    "tree_nuts": true/false,
    "celery": true/false,
    "mustard": true/false
  }},
  "nutrients": {{
    "energy": "value unit" or "N/A",
    "fat": "value unit" or "N/A",
    "carbohydrate": "value unit" or "N/A",
    "sugar": "value unit" or "N/A",
    "protein": "value unit" or "N/A",
    "sodium": "value unit" or "N/A"
  }}
}}"""

    async def extract_with_gemini(self, text: str, api_key: str) -> Tuple[Dict, Dict]:
        """Extract with Gemini"""
        try:
            self.logger.info("Using Gemini for extraction...")
            prompt = self.create_comprehensive_prompt(text)
            
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
                
                payload = {
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"temperature": 0.1, "maxOutputTokens": 1000}
                }
                
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        result_text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                        self.logger.info(f" Gemini raw response: {result_text}")
                        
                        # Clean JSON response (remove markdown formatting)
                        if result_text.startswith('```json'):
                            result_text = result_text[7:]  # Remove ```json
                        if result_text.endswith('```'):
                            result_text = result_text[:-3]  # Remove ```
                        result_text = result_text.strip()
                        
                        # Try to parse JSON
                        try:
                            result = json.loads(result_text)
                            
                            # Check if allergens is a list (incorrect LLM response) and convert to dict
                            allergens_raw = result.get("allergens", {})
                            nutrients_raw = result.get("nutrients", {})
                            
                            if isinstance(allergens_raw, list):
                                self.logger.warning("LLM returned allergens as list, converting to empty dict")
                                allergens = {}
                            else:
                                allergens = allergens_raw
                            
                            if isinstance(nutrients_raw, list):
                                self.logger.warning("LLM returned nutrients as list, converting to empty dict")
                                nutrients = {}
                            else:
                                nutrients = nutrients_raw
                            
                            # Log LLM results
                            true_allergens = sum(1 for v in allergens.values() if v is True)
                            self.logger.info(f" Gemini returned {true_allergens} true allergens: {[k for k, v in allergens.items() if v]}")
                            self.logger.info(" Gemini JSON parsed successfully")
                            return allergens, nutrients
                        except json.JSONDecodeError:
                            self.logger.warning(" Gemini response is not valid JSON, using fallback")
                            return self.advanced_fallback(result_text)
                    else:
                        self.logger.error(f" Gemini API error: {response.status}")
                        return {}, {}
                        
        except Exception as e:
            self.logger.error(f"Gemini failed: {e}")
            return {}, {}
    
    def advanced_fallback(self, text: str) -> Tuple[Dict, Dict]:
        """Advanced fallback with comprehensive patterns for all document types"""
        self.logger.info("Using advanced fallback...")
        self.logger.debug(f"Text length: {len(text)}, first 200 chars: {text[:200]}")
        
        # Comprehensive patterns for all document formats
        patterns = {
            "energy": [
                # IMPORTANT: Both units formats FIRST
                # Format with colon: "Energy/Energia: 1173 kJ/282kcal"
                r"energy/energia:\s*(\d+(?:,\d+)?)\s*kj/(\d+(?:,\d+)?)kcal",
                r"energia/energy:\s*(\d+(?:,\d+)?)\s*kj/(\d+(?:,\d+)?)kcal",
                # Format: "Energy/Energia 1173 kJ/282kcal" or "Energia/Energy 1173 kJ/282kcal"
                r"energy/energia\s*(\d+(?:,\d+)?)\s*kj/(\d+(?:,\d+)?)kcal",
                r"energia/energy\s*(\d+(?:,\d+)?)\s*kj/(\d+(?:,\d+)?)kcal",
                # Format with label "value": "Energia/Energy value 224 kJ / 53 kcal"
                r"energia/energy\s+value\s+(\d+(?:,\d+)?)\s*kj\s*/\s*(\d+(?:,\d+)?)\s*kcal",
                # Format with multiple spaces: "Energia/Energy value  224 kJ / 53 kcal"
                r"energia/energy\s+value\s{2,}(\d+(?:,\d+)?)\s*kj\s*/\s*(\d+(?:,\d+)?)\s*kcal",
                # Format: "Energia 1173 kJ/282kcal"
                r"(?:energia|energy)\s+(\d+(?:,\d+)?)\s*kj/(\d+(?:,\d+)?)kcal",
                # Format: "Energia: 224 kJ / 53 kcal"
                r"(?:energia|energy)[:\s]*(\d+(?:,\d+)?)\s*kj\s*/\s*(\d+(?:,\d+)?)\s*kcal",
                r"(\d+(?:,\d+)?)\s*kj\s*/\s*(\d+(?:,\d+)?)\s*kcal",
                r"(\d+(?:,\d+)?)\s*kj/(\d+(?:,\d+)?)\s*kcal",  # Without space
                r"(\d+(?:,\d+)?)\s*kj\s*\((\d+(?:,\d+)?)\s*kcal\)",  # Parentheses
                
                # Standard formats with labels (single unit)
                r"(?:energia|energy|énergie|calories|calorías)[:\s]*(\d+(?:,\d+)?)\s*(?:kj|kcal)(?!\s*/)",
                r"(?:energia|energy|énergie|calories|calorías)\s*\[(?:kj|kcal)\]\s*:\s*(\d+(?:,\d+)?)\s*(?:kj|kcal)",
                
                # Direct energy values (more specific)
                r"(\d+(?:,\d+)?)\s*kj(?!\s*/)",  # kJ only
                r"(\d+(?:,\d+)?)\s*kcal(?!\s*/)",  # kcal only
                
                # Hungarian kcal formats
                r"energia\s*:\s*(\d+(?:,\d+)?)\s*kcal",
                r"energia\s+(\d+(?:,\d+)?)\s*kcal",
                r"energia\s+(\d+(?:,\d+)?)\s*kj",
                
                # Hungarian specific formats
                r"energia\s*\[kj\]\s*:\s*(\d+(?:,\d+)?)\s*kj",
                r"energia\s*\[kcal\]\s*:\s*(\d+(?:,\d+)?)\s*kcal",
                r"energia\s*:\s*(\d+(?:,\d+)?)\s*(?:kj|kcal)",
                
                # French formats
                r"énergie\s*:\s*(\d+(?:,\d+)?)\s*(?:kj|kcal)",
                r"calories\s*:\s*(\d+(?:,\d+)?)\s*kcal",
                
                # Table formats
                r"energia\s*\(kj\)\s*:\s*(\d+(?:,\d+)?)",
                r"energia\s*\(kcal\)\s*:\s*(\d+(?:,\d+)?)",
                
                # Hungarian table format: "Energia  kJ  1553 I N X"
                r"energia\s+\s*kj\s+(\d+)(?:\s+[INX])?",
                r"energia\s+\s*kcal\s+(\d+)(?:\s+[INX])?",
                
                # OCR error patterns
                r"energia\s*:\s*(\d+(?:[.,]\d+)?)\s*(?:kj|kcal)",
                r"energy\s*:\s*(\d+(?:[.,]\d+)?)\s*(?:kj|kcal)"
            ],
            "fat": [
                # Standard formats with labels
                r"(?:zsír|fat|lipides|gras|grasas)[:\s]+(\d+(?:[,.]\d+)?)\s*g(?!\s*/)",
                r"(?:zsírtartalom|fat content|contenu en lipides|contenido en grasas)[:\s]+(\d+(?:[,.]\d+)?)\s*g(?!\s*/)",
                # Hungarian without colon
                r"zsír\s+(\d+(?:[,.]\d+)?)\s*g",
                r"fat\s+(\d+(?:[,.]\d+)?)\s*g",
                
                # Hungarian table format: "Zsír  g  36 N"
                r"zsír\s+\s*g\s+(\d+(?:,\d+)?)(?:\s+[INX])?",
                # Hungarian table format: "Zsír  g  36 N" (alternative)
                r"zsír\s+\s*g\s+(\d+)(?:\s+[INX])?",
                # Hungarian table format with comma: "Zsír  g  36,5 N"
                r"zsír\s+\s*g\s+(\d+,\d+)(?:\s+[INX])?",
                r"zsír\s*\[\s*g\s*\]\s*(\d+(?:,\d+)?)\s*[INX]",
                r"zsír\s*\[\s*g\s*\]\s*(\d+(?:,\d+)?)\s*[NX]",
                r"zsír\s*\[g\]\s*:\s*(\d+(?:,\d+)?)\s*g",
                r"zsír\s*:\s*(\d+(?:,\d+)?)\s*g",
                r"zsír\s*g\s*:\s*(\d+(?:,\d+)?)\s*g",
                r"zsírtartalom\s*:\s*(\d+(?:,\d+)?)\s*g",
                
                # Direct values without labels (for table formats) - REMOVED TOO BROAD
                # r"(\d{1,2},\d{2})\s*g\s*$",
                # r"^(\d{1,2},\d{2})\s*g",
                # r"^\s*(\d{1,2},\d{2})\s*$",
                # r"(\d{1,3},\d{1,2})\s*g",
                # r"(\d+,\d+)\s*g"
                
                # English formats
                r"fat/.*?(\d+(?:,\d+)?)\s*g",
                r"fat\s*:\s*(\d+(?:,\d+)?)\s*g",
                r"total fat\s*:\s*(\d+(?:,\d+)?)\s*g",
                
                # French formats
                r"lipides\s*:\s*(\d+(?:,\d+)?)\s*g",
                r"matières grasses\s*:\s*(\d+(?:,\d+)?)\s*g",
                
                # Spanish formats
                r"grasas\s*:\s*(\d+(?:,\d+)?)\s*g",
                r"lípidos\s*:\s*(\d+(?:,\d+)?)\s*g",
                
                # Table formats
                r"zsír\s*\(g\)\s*:\s*(\d+(?:,\d+)?)",
                r"fat\s*\(g\)\s*:\s*(\d+(?:,\d+)?)",
                
                # OCR error patterns
                r"zsir\s*:\s*(\d+(?:[.,]\d+)?)\s*g",
                r"fat\s*:\s*(\d+(?:[.,]\d+)?)\s*g"
            ],
            "protein": [
                # Standard formats with labels
                r"(?:fehérje|protein|protéines|proteínas|proteine)[:\s]+(\d+(?:,\d+)?)\s*g(?!\s*/)",
                # Hungarian without colon
                r"fehérje\s+(\d+(?:,\d+)?)\s*g",
                r"protein\s+(\d+(?:,\d+)?)\s*g",
                
                # Hungarian table format: "Fehérje  g 21,6" or "Fehérje  g 12 N" - capture ONLY the number
                r"fehérje\s+\s*g\s+(\d+(?:,\d+)?)(?!\s*[gG])",
                r"Fehérje\s+\s*g\s+(\d+(?:,\d+)?)(?!\s*[gG])",
                r"fehérje\s*\[\s*g\s*\]\s+(\d+(?:,\d+)?)(?=\s*[INX]|\s|$)",
                r"fehérje\s*\[\s*g\s*\]\s+(\d+(?:,\d+)?)(?=\s*[NX]|\s|$)",
                r"fehérje\s*\[g\]\s*:\s*(\d+(?:,\d+)?)\s*g",
                r"fehérje\s*:\s*(\d+(?:,\d+)?)\s*g",
                r"fehérje\s*g\s*:\s*(\d+(?:,\d+)?)\s*g",
                r"fehérjetartalom\s*:\s*(\d+(?:,\d+)?)\s*g",
                
                # English formats
                r"protein/.*?(\d+(?:,\d+)?)\s*g",
                r"protein\s*:\s*(\d+(?:,\d+)?)\s*g",
                r"total protein\s*:\s*(\d+(?:,\d+)?)\s*g",
                
                # French formats
                r"protéines\s*:\s*(\d+(?:,\d+)?)\s*g",
                r"protéine\s*:\s*(\d+(?:,\d+)?)\s*g",
                
                # Spanish formats
                r"proteínas\s*:\s*(\d+(?:,\d+)?)\s*g",
                r"proteína\s*:\s*(\d+(?:,\d+)?)\s*g",
                
                # Table formats
                r"fehérje\s*\(g\)\s*:\s*(\d+(?:,\d+)?)",
                r"protein\s*\(g\)\s*:\s*(\d+(?:,\d+)?)",
                
                # OCR error patterns
                r"feherje\s*:\s*(\d+(?:[.,]\d+)?)\s*g",
                r"protein\s*:\s*(\d+(?:[.,]\d+)?)\s*g",
                # OCR patterns for yogurt document
                r"Fehérje\s*(\d+(?:[.,]\d+)?)\s*g",
                r"fehérje\s*(\d+(?:[.,]\d+)?)\s*g",
                # Direct values for table formats - REMOVED TOO BROAD
                # r"^\s*(\d{1,2},\d{1})\s*g",
                # r"(\d+,\d+)\s*g"
            ],
            "carbohydrate": [
                # Standard formats with labels
                r"(?:szénhidrát|carbohydrate|carbohydrates|glucides|hidratos de carbono)[:\s]+(\d+(?:,\d+)?)\s*g(?!\s*/)",
                # Hungarian without colon
                r"szénhidrát\s+(\d+(?:,\d+)?)\s*g",
                r"carbohydrate\s+(\d+(?:,\d+)?)\s*g",
                # Add pattern for decimal in Hungarian
                r"szénhidrát\s*:\s*(\d+(?:[.,]\d+)?)\s*g",
                
                # Hungarian table format: "Szénhidrát  g  1 N"
                r"szénhidrát\s+\s*g\s+(\d+)(?:\s+[INX])?",
                r"szénhidrát\s*\[\s*g\s*\]\s*(\d+(?:,\d+)?)\s*[INX]",
                r"szénhidrát\s*\[\s*g\s*\]\s*(\d+(?:,\d+)?)\s*[NX]",
                r"szénhidrát\s*\[g\]\s*:\s*(\d+(?:,\d+)?)\s*g",
                r"szénhidrát\s*:\s*(\d+(?:,\d+)?)\s*g",
                r"szénhidrát\s*g\s*:\s*(\d+(?:,\d+)?)\s*g",
                r"szénhidráttartalom\s*:\s*(\d+(?:,\d+)?)\s*g",
                
                # English formats
                r"carbohydrate/.*?(\d+(?:,\d+)?)\s*g",
                r"carbohydrate\s*:\s*(\d+(?:,\d+)?)\s*g",
                r"total carbohydrate\s*:\s*(\d+(?:,\d+)?)\s*g",
                r"carbohydrates\s*:\s*(\d+(?:,\d+)?)\s*g",
                
                # French formats
                r"glucides\s*:\s*(\d+(?:,\d+)?)\s*g",
                r"hydrates de carbone\s*:\s*(\d+(?:,\d+)?)\s*g",
                
                # Spanish formats
                r"hidratos de carbono\s*:\s*(\d+(?:,\d+)?)\s*g",
                r"carbohidratos\s*:\s*(\d+(?:,\d+)?)\s*g",
                
                # Table formats
                r"szénhidrát\s*\(g\)\s*:\s*(\d+(?:,\d+)?)",
                r"carbohydrate\s*\(g\)\s*:\s*(\d+(?:,\d+)?)",
                
                # OCR error patterns
                r"szénhidrat\s*:\s*(\d+(?:[.,]\d+)?)\s*g",
                r"carbohydrate\s*:\s*(\d+(?:[.,]\d+)?)\s*g",
                # Direct values for table formats - REMOVED TOO BROAD
                # r"^\s*(\d{1,3},\d{1,2})\s*g",
                # r"(\d+,\d+)\s*g"
            ],
            "sugar": [
                # Standard formats with labels
                r"(?:cukor|sugar|sugars|sucres|azúcares)[:\s]+(\d+(?:,\d+)?)\s*g(?!\s*/)",
                # Hungarian without colon
                r"cukor\s+(\d+(?:,\d+)?)\s*g",
                r"sugar\s+(\d+(?:,\d+)?)\s*g",
                
                # Hungarian table format: "cukor  g  0,5 N"
                r"cukor\s+\s*g\s+(\d+,\d+)(?:\s+[INX])?",
                # "amelyből cukor: X.X g" or "-of which sugars/ X.X g amelyből cukrok"
                r"amelyből cukor\s*[:\s]+\s*(\d+(?:,\d+)?)\s*g",
                r"amelyből cukrok\s*[:\s]+\s*(\d+(?:,\d+)?)\s*g",
                r"-of which sugars/\s*(\d+(?:,\d+)?)\s*g",
                r"-of which sugar/\s*(\d+(?:,\d+)?)\s*g",
                # Format: "amelyből cukrok  2,4 g" (with spaces, no colon)
                r"amelyből cukrok\s+(\d+(?:,\d+)?)\s*g",
                r"amelyből cukor\s+(\d+(?:,\d+)?)\s*g",
                r"sugars?\s*:\s*(\d+(?:,\d+)?)\s*g(?!\s*/)",
                r"sugar\s*:\s*(\d+(?:,\d+)?)\s*g(?!\s*/)",
                r"cukrok\s*\[\s*g\s*\]\s*(\d+(?:,\d+)?)\s*[INX]",
                r"cukor\s*\[\s*g\s*\]\s*(\d+(?:,\d+)?)\s*[INX]",
                r"cukor\s*:\s*(\d+(?:,\d+)?)\s*g",
                r"cukrok\s*:\s*(\d+(?:,\d+)?)\s*g",
                r"cukor\s*g\s*:\s*(\d+(?:,\d+)?)\s*g",
                r"cukrok\s*g\s*:\s*(\d+(?:,\d+)?)\s*g",
                r"cukortartalom\s*:\s*(\d+(?:,\d+)?)\s*g",
                
                # English formats
                r"sugars/\s*(\d+(?:,\d+)?)\s*g",
                r"sugar/.*?(\d+(?:,\d+)?)\s*g",
                r"sugar\s*:\s*(\d+(?:,\d+)?)\s*g",
                r"sugars\s*:\s*(\d+(?:,\d+)?)\s*g",
                r"of which sugars\s*:\s*(\d+(?:,\d+)?)\s*g",
                
                # French formats
                r"sucres\s*:\s*(\d+(?:,\d+)?)\s*g",
                r"dont sucres\s*:\s*(\d+(?:,\d+)?)\s*g",
                
                # Spanish formats
                r"azúcares\s*:\s*(\d+(?:,\d+)?)\s*g",
                r"de los cuales azúcares\s*:\s*(\d+(?:,\d+)?)\s*g",
                
                # Table formats
                r"cukor\s*\(g\)\s*:\s*(\d+(?:,\d+)?)",
                r"sugar\s*\(g\)\s*:\s*(\d+(?:,\d+)?)",
                
                # OCR error patterns
                r"cukor\s*:\s*(\d+(?:[.,]\d+)?)\s*g",
                r"sugar\s*:\s*(\d+(?:[.,]\d+)?)\s*g",
                # OCR patterns for yogurt document
                r"amelyből cukrok\s*[:\s]+\s*(\d+(?:[.,]\d+)?)\s*g",
                r"amelyből cukrok\s+(\d+(?:[.,]\d+)?)\s*g",
                r"cukrok\s+(\d+(?:[.,]\d+)?)\s*g",
                # Handle variations: "amelyből cukrok: 2,4" without "g"
                r"amelyből cukrok\s*[:\s]+\s*(\d+(?:[.,]\d+)?)",
                r"ebből cukor\s*[:\s]+\s*(\d+(?:[.,]\d+)?)\s*g"
            ],
            "sodium": [
                # Standard formats with labels
                r"(?:só|salt|sodium|sel|nátrium|sal)[:\s]+(\d+(?:,\d+)?)\s*g(?!\s*/)",
                # Handle "-" or "not specified" cases
                r"(?:só|salt|sodium)[:\s]+[-\u2013]",
                # Hungarian without colon
                r"só\s+(\d+(?:,\d+)?)\s*g",
                r"salt\s+(\d+(?:,\d+)?)\s*g",
                
                # Hungarian table format: "Só  g  1,9 N"
                r"só\s+\s*g\s+(\d+,\d+)(?:\s+[INX])?",
                r"só\s*\[\s*g\s*\]\s*(\d+(?:,\d+)?)\s*[INX]",
                r"só\s*\[\s*g\s*\]\s*(\d+(?:,\d+)?)\s*[NX]",
                r"só\s*\[g\]\s*:\s*(\d+(?:,\d+)?)\s*g",
                r"só\s*:\s*(\d+(?:,\d+)?)\s*g",
                r"só\s*g\s*:\s*(\d+(?:,\d+)?)\s*g",
                r"nátrium\s*:\s*(\d+(?:,\d+)?)\s*g",
                r"sótartalom\s*:\s*(\d+(?:,\d+)?)\s*g",
                
                # English formats
                r"salt/.*?(\d+(?:[.,]\d+)?)\s*g",
                r"salt\s*:\s*(\d+(?:[.,]\d+)?)\s*g",
                r"sodium\s*:\s*(\d+(?:[.,]\d+)?)\s*g",
                r"sodium\s*:\s*(\d+(?:[.,]\d+)?)\s*mg",
                
                # French formats
                r"sel\s*:\s*(\d+(?:,\d+)?)\s*g",
                r"sodium\s*:\s*(\d+(?:,\d+)?)\s*g",
                
                # Spanish formats
                r"sal\s*:\s*(\d+(?:,\d+)?)\s*g",
                r"sodio\s*:\s*(\d+(?:,\d+)?)\s*g",
                
                # Table formats
                r"só\s*\(g\)\s*:\s*(\d+(?:,\d+)?)",
                r"salt\s*\(g\)\s*:\s*(\d+(?:,\d+)?)",
                
                # OCR error patterns
                r"so\s*:\s*(\d+(?:[.,]\d+)?)\s*g",
                r"salt\s*:\s*(\d+(?:[.,]\d+)?)\s*g",
                # Direct values for table formats - REMOVED TOO BROAD
                # r"^\s*(\d{1},\d{3})\s*g",
                # r"^\s*(\d{1},\d{2})\s*g",
                # r"(\d+,\d{3})\s*g"
            ]
        }
        
        # Initialize nutrients with default values
        nutrients = {
            "energy": "N/A",
            "fat": "N/A",
            "carbohydrate": "N/A",
            "sugar": "N/A",
            "protein": "N/A",
            "sodium": "N/A"
        }
        
        for nutrient, pattern_list in patterns.items():
            value = None
            match_text = None
            for pattern in pattern_list:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    match_text = match.group(0)
                    # Handle different group numbers
                    if len(match.groups()) > 1:
                        # For energy with both kJ and kcal, prefer kJ
                        value = match.group(1) if match.group(1) else match.group(2)
                    else:
                        value = match.group(1)
                    self.logger.debug(f"Matched {nutrient} with pattern: {match.group(0)} -> {value}")
                    break
            
            if value:
                # Validate value ranges to avoid incorrect extractions
                try:
                    # Handle both comma and dot as decimal separators
                    num_value = float(value.replace(',', '.'))
                    
                        # Reasonable ranges for nutrients per 100g
                    max_values = {
                        "energy": 5000,  # kJ (increased for high-energy foods)
                        "fat": 100,      # g (increased for high-fat foods)
                        "protein": 100,  # g (increased for high-protein foods)
                        "carbohydrate": 100,  # g
                        "sugar": 100,    # g
                        "sodium": 10     # g (increased for processed foods)
                    }
                    
                    # Also check for suspiciously low values (likely wrong extraction)
                    min_values = {
                        "energy": 50,    # kJ (minimum reasonable energy)
                        "fat": 0.01,     # g (minimum fat - allow very low fat products)
                        "protein": 0.01,  # g (minimum protein)
                        "carbohydrate": 0.01,  # g (minimum carbohydrate)
                        "sugar": 0.01,   # g (minimum sugar)
                        "sodium": 0.001  # g (minimum sodium)
                    }
                    
                    # Skip validation for energy - we'll handle it specially
                    if nutrient != "energy":
                        if num_value > max_values.get(nutrient, 1000):
                            self.logger.warning(f"Suspicious high value for {nutrient}: {value}")
                            nutrients[nutrient] = "N/A"
                            continue
                    
                    if num_value < min_values.get(nutrient, 0):
                        self.logger.warning(f"Suspicious low value for {nutrient}: {value}")
                        # Don't reject, just warn - might be correct for very low values
                        
                except ValueError:
                    self.logger.warning(f"Invalid number format for {nutrient}: {value}")
                    nutrients[nutrient] = "N/A"
                    continue
                
                if nutrient == "energy":
                    # Check if we matched both kJ and kcal (pattern with 2 groups)
                    if match and len(match.groups()) >= 2:
                        # Both units found - save as combined format
                        kj_val = match.group(1)
                        kcal_val = match.group(2)
                        nutrients["energy"] = f"{kj_val} kJ / {kcal_val} kcal"
                    else:
                        # Single unit - infer from text
                        unit = "kJ"
                        if match_text:
                            lt = match_text.lower()
                            # Check for kcal pattern (must be explicit)
                            if "kcal" in lt and "kj" not in lt:
                                unit = "kcal"
                            elif "kj" in lt:
                                unit = "kJ"
                        
                        nutrients["energy"] = f"{value} {unit}"
                else:
                    # Handle sodium in mg → convert to g
                    if nutrient == "sodium" and match_text and "mg" in match_text.lower():
                        grams = num_value / 1000.0
                        nutrients[nutrient] = f"{grams:.3f} g"
                    else:
                        nutrients[nutrient] = f"{value} g"
        
        self.logger.info(f"Extracted nutrients: {nutrients}")
        
        # Improved allergen detection with context
        # BE CONSERVATIVE: Default all allergens to False unless explicitly found
        allergens = {
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
        
        # CONSERVATIVE APPROACH: Only look for numbered allergen table format
        
        # CONSERVATIVE APPROACH: Only look for numbered allergen table format
        # Format: "06 + Gluten", "03 - Eggs", etc.
        
        # Basic fallback: parse numbered format "06 + Gluten", "03 - Eggs"
        allergen_keywords = {
            "gluten": ["gluten", "glutén"],
            "milk": ["milk", "tej", "tejfehérje", "laktóz"],
            "egg": ["egg", "tojás"],
            "crustaceans": ["crustacean", "rák", "rákfélék"],
            "fish": ["fish", "hal"],
            "peanut": ["peanut", "földimogyoró"],
            "soy": ["soy", "szója"],
            "tree_nuts": ["almond", "walnut", "dió", "diófélék"],
            "celery": ["celery", "zeller"],
            "mustard": ["mustard", "mustár"]
        }
        
        for allergen, keywords_list in allergen_keywords.items():
            for keyword in keywords_list:
                # Check for "+" indicator
                plus_pattern = rf"\d+\s*\+\s+.*?{keyword}"
                if re.search(plus_pattern, text, re.IGNORECASE):
                    allergens[allergen] = True
                    self.logger.info(f"Found {allergen} with +")
                    break
                # Check for "-" indicator
                minus_pattern = rf"\d+\s*\-\s+.*?{keyword}"
                if re.search(minus_pattern, text, re.IGNORECASE):
                    allergens[allergen] = False
                    self.logger.info(f"Found {allergen} with -")
                    break
        
        return allergens, nutrients
    
    def clean_text(self, text: str) -> str:
        """Advanced text cleaning with OCR error correction"""
        # Remove extra spaces and normalize
        text = re.sub(r'\s+', ' ', text)
        
        # Fix common OCR errors
        ocr_fixes = {
            's6': 'só', 'S6': 'Só',
            'cukrok': 'cukor', 'Cukrok': 'Cukor',
            'Zsir': 'Zsír', 'Feherje': 'Fehérje',
            '1Z73': '1173', '1Z74': '1174', '1Z75': '1175',
            'amelyből cukrok': 'amelyből cukor',
            'telített zsírsavak': 'telített zsír',
            'zsirtartalom': 'zsír tartalom',
            # Fix OCR errors from yogurt document
            'Jellemz6érték': 'Jellemzőérték',
            'amelyb6élcukrok': 'amelyből cukrok',
            'amelybőltelítettzsírsavak': 'amelyből telített zsírsavak',
            'Fehérje 3,2 2/100g': 'Fehérje 3,2 g/100g',
            'amelyb6élcukrok 2,4 2/100g': 'amelyből cukrok 2,4 g/100g',
            'Gluténttartalmaz6gabonafélék': 'Glutént tartalmazó gabonafélék',
            'Rakfélék': 'Rákfélék',
            'Szdjabab': 'Szójabab',
            'Féldimogyoré': 'Földimogyoró',
            'Csonthéjasok': 'Csonthéjasok',
            'Mustarésabbolkésziilttermékek': 'Mustár és abból készült termékek'
        }
        
        for wrong, correct in ocr_fixes.items():
            text = text.replace(wrong, correct)
        
        # Normalize parentheses and brackets
        text = re.sub(r'[\[\]]', '(', text)
        text = re.sub(r'[()]', ' ', text)
        
        # Remove extra punctuation but keep important ones (+ and - for allergens)
        text = re.sub(r'[^\w\s,.:+-]', ' ', text)
        
        # Fix common OCR number errors
        text = re.sub(r'(\d+)[Oo](\d+)', r'\1.0\2', text)  # 15O2 -> 15.02
        text = re.sub(r'(\d+)[lI](\d+)', r'\1.1\2', text)  # 15l2 -> 15.12
        # Normalize decimal separator: dot -> comma for numeric decimals (e.g., 1.58 -> 1,58)
        text = re.sub(r'(?<=\d)\.(?=\d)', ',', text)
        
        return text.strip()
