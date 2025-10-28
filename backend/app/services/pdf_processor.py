
## 3. Сервис обработки PDF (`app/services/pdf_processor.py`)

import asyncio
import base64
import PyPDF2
import pdf2image
import pytesseract
from PIL import Image, ImageEnhance
import io
import logging

class PDFProcessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # OCR settings for better quality - more comprehensive character set
        self.ocr_config = '--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÁÉÍÓÚÖÜŐŰáéíóúöüőű.,:;()[]{}%+-/gkjml '
    
    async def extract_text_from_pdf(self, pdf_data: bytes) -> str:
        """
        Asynchronously extracts text from PDF (text or scanned) with improved processing
        """
        try:
            self.logger.info("Starting PDF text extraction...")
            
            # Check if data looks like a PDF
            if not pdf_data.startswith(b'%PDF'):
                self.logger.warning("Data doesn't appear to be a PDF file")
                raise Exception("Not a valid PDF file")
            
            # Attempt to extract text directly from PDF
            text = await self._extract_direct_text(pdf_data)
            
            # Check quality of extracted text
            if self._is_text_quality_good(text):
                self.logger.info(f"Direct text extraction successful: {len(text)} characters")
                return self._clean_text(text)
            
            self.logger.info("Direct extraction insufficient, trying OCR...")
            
            # If text is insufficient or quality is poor, try OCR
            ocr_text = await self._extract_text_with_ocr(pdf_data)
            
            # Combine results if possible
            if text and ocr_text:
                combined_text = f"{text}\n{ocr_text}"
                self.logger.info(f"Combined text extraction: {len(combined_text)} characters")
                return self._clean_text(combined_text)
            
            return self._clean_text(ocr_text) if ocr_text else ""
            
        except Exception as e:
            self.logger.error(f"Error extracting text from PDF: {e}")
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    async def _extract_direct_text(self, pdf_data: bytes) -> str:
        """Extracts text from text-based PDF"""
        loop = asyncio.get_event_loop()
        
        def extract_text():
            text = ""
            try:
                with io.BytesIO(pdf_data) as pdf_file:
                    pdf_reader = PyPDF2.PdfReader(pdf_file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
            except Exception as e:
                print(f"Direct text extraction failed: {e}")
            return text
        
        return await loop.run_in_executor(None, extract_text)
    
    def _is_text_quality_good(self, text: str) -> bool:
        """Validates extracted text quality"""
        if not text or len(text.strip()) < 50:
            return False
        
        # Check for food product keywords
        food_keywords = ['energia', 'zsír', 'szénhidrát', 'fehérje', 'nátrium', 
                        'energy', 'fat', 'carbohydrate', 'protein', 'sodium']
        
        text_lower = text.lower()
        keyword_count = sum(1 for keyword in food_keywords if keyword in text_lower)
        
        # Also check for numbers (nutritional values)
        import re
        numbers = re.findall(r'\d+(?:,\d+)?', text)
        
        return keyword_count >= 2 and len(numbers) >= 3
    
    def _clean_text(self, text: str) -> str:
        """Cleans and normalizes text"""
        if not text:
            return ""
        
        import re
        # Normalize whitespace: multiple spaces/newlines to single space
        # BUT preserve structure - replace multiple spaces with single space
        text = re.sub(r'[^\S\n]+', ' ', text)  # Multiple spaces → single space
        text = re.sub(r'\n{3,}', '\n\n', text)  # Multiple newlines → max 2

        # Remove extra spaces and line breaks
        lines = text.split('\n')
        cleaned_lines = []

        for line in lines:
            # Remove extra spaces
            line = ' '.join(line.split())
            
            # Skip empty lines
            if line.strip():
                cleaned_lines.append(line)

        # Join lines
        cleaned_text = '\n'.join(cleaned_lines)
        
        # Fix common OCR errors for Hungarian language
        ocr_fixes = {
            '2sir': 'Zsír',
            'amelyb6l': 'amelyből',
            'amelybol': 'amelyből',
            'telitett': 'telített',
            'zsirsavak': 'zsírsavak',
            'Szénhidrat': 'Szénhidrát',
            'Fehérje': 'Fehérje',
            'Natrium': 'Nátrium',
            'tapérték': 'tápérték',
            'Atlagos': 'Átlagos',
            'energia': 'Energia',
            'zsir': 'Zsír',
            'szénhidrat': 'Szénhidrát',
            'feherje': 'Fehérje',
            'natrium': 'Nátrium'
        }
        
        for wrong, correct in ocr_fixes.items():
            cleaned_text = cleaned_text.replace(wrong, correct)
        
        return cleaned_text
    
    async def _extract_text_with_ocr(self, pdf_data: bytes) -> str:
        """Extracts text from scanned PDF using improved OCR"""
        loop = asyncio.get_event_loop()
        
        def perform_ocr():
            text = ""
            try:
                self.logger.info("Starting OCR processing...")
                
                # Convert PDF to images with high resolution
                images = pdf2image.convert_from_bytes(
                    pdf_data, 
                    dpi=300,  # High resolution for better OCR
                    first_page=None,
                    last_page=None,
                    fmt='jpeg',
                    jpegopt={'quality': 95, 'optimize': True}
                )
                
                self.logger.info(f"Converted PDF to {len(images)} images")
                
                for i, image in enumerate(images):
                    self.logger.info(f"Processing page {i + 1}/{len(images)}")
                    
                    # Enhance image for better OCR
                    enhanced_image = self._enhance_image_for_ocr(image)
                    
                    # Extract text using Tesseract
                    page_text = self._extract_text_from_image(enhanced_image)
                    
                    if page_text:
                        # Clean and improve extracted text
                        cleaned_text = self._clean_ocr_text(page_text)
                        text += cleaned_text + "\n"
                        self.logger.info(f"Page {i + 1}: extracted {len(cleaned_text)} characters")
                    else:
                        self.logger.warning(f"Page {i + 1}: no text extracted")
                    
            except Exception as e:
                self.logger.error(f"OCR extraction failed: {e}")
            
            self.logger.info(f"OCR completed: {len(text)} total characters")
            return text
        
        return await loop.run_in_executor(None, perform_ocr)
    
    def _enhance_image_for_ocr(self, image: Image.Image) -> Image.Image:
        """Enhances image for better OCR"""
        try:
            # Increase resolution
            width, height = image.size
            if width < 2000 or height < 2000:
                scale_factor = max(2000 / width, 2000 / height)
                new_size = (int(width * scale_factor), int(height * scale_factor))
                image = image.resize(new_size, Image.LANCZOS)
            
            # Convert to grayscale
            if image.mode != 'L':
                image = image.convert('L')
            
            # Increase contrast
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)
            
            # Increase sharpness
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(2.0)
            
            return image
            
        except Exception as e:
            self.logger.error(f"Image enhancement failed: {e}")
            return image
    
    def _extract_text_from_image(self, image: Image.Image) -> str:
        """Extracts text from image using Tesseract"""
        try:
            # Try different languages and settings
            languages_to_try = ['hun+eng', 'hun', 'eng']
            
            for lang in languages_to_try:
                try:
                    text = pytesseract.image_to_string(
                        image, 
                        lang=lang,
                        config=self.ocr_config
                    )
                    if text and len(text.strip()) > 10:
                        self.logger.info(f"OCR successful with language: {lang}")
                        return text
                except Exception as e:
                    self.logger.debug(f"OCR failed with language {lang}: {e}")
                    continue
            
            # If all languages failed, try without language specification
            text = pytesseract.image_to_string(image, config=self.ocr_config)
            return text
            
        except Exception as e:
            self.logger.error(f"Tesseract extraction failed: {e}")
            return ""
    
    async def process_base64_pdf(self, base64_string: str) -> bytes:
        """Converts base64 string to bytes"""
        try:
            if ',' in base64_string:
                base64_string = base64_string.split(',')[1]
            
            pdf_data = base64.b64decode(base64_string)
            return pdf_data
        except Exception as e:
            raise Exception(f"Error decoding base64 PDF: {str(e)}")    
    def _clean_ocr_text(self, text: str) -> str:
        """Cleans and improves text extracted using OCR"""
        if not text:
            return ""
        
        # Remove extra spaces and line breaks
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Remove extra spaces
            line = ' '.join(line.split())
            
            # Skip empty lines
            if line.strip():
                cleaned_lines.append(line)
        
        # Join lines
        cleaned_text = '\n'.join(cleaned_lines)
        
        # Fix common OCR errors for Hungarian language
        ocr_fixes = {
            '2sir': 'Zsír',
            'amelyb6l': 'amelyből',
            'amelybol': 'amelyből',
            'telitett': 'telített',
            'zsirsavak': 'zsírsavak',
            'Szénhidrat': 'Szénhidrát',
            'Fehérje': 'Fehérje',
            'Natrium': 'Nátrium',
            'tapérték': 'tápérték',
            'Atlagos': 'Átlagos',
            'energia': 'Energia',
            'zsir': 'Zsír',
            'szénhidrat': 'Szénhidrát',
            'feherje': 'Fehérje',
            'natrium': 'Nátrium',
            'cukor': 'cukor',
            'amelyből cukor': 'amelyből cukor'
        }
        
        for wrong, correct in ocr_fixes.items():
            cleaned_text = cleaned_text.replace(wrong, correct)
        
        return cleaned_text
