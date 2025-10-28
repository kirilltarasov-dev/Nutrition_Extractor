# Nutrition & Allergen Extractor - User Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Using the Application](#using-the-application)
4. [Understanding the Results](#understanding-the-results)
5. [Troubleshooting](#troubleshooting)
6. [Frequently Asked Questions](#frequently-asked-questions)

---

## Introduction

The Nutrition & Allergen Extractor is an AI-powered tool that automatically extracts allergen information and nutritional values from food specification PDF documents. It's designed to save time and reduce errors in handling product specifications.

### What It Does

- Extracts 10 major allergens from PDF documents
- Extracts 6 key nutritional values (energy, fat, carbohydrates, sugar, protein, sodium)
- Supports both real PDFs and scanned documents (with OCR)
- Works in English and Hungarian
- Provides results in under 5 seconds typically
- Supports uploading up to 3 PDF files simultaneously
- Provides history of previous extractions
- Export results to JSON or PDF format
- Fast async processing with real-time progress updates

### Supported Languages

- 🇺🇸 English
- 🇭🇺 Hungarian

---

## Getting Started

### Prerequisites

Before using the application, you need:

1. **A Google Gemini API Key** (free tier available)
   - Visit [Google AI Studio](https://ai.google.dev/) to get your API key
   - Sign in with your Google account
   - Click "Get API Key" to generate one

2. **PDF file(s)** containing nutrition information
   - Must be a product specification document
   - Can be a real PDF or a scanned image-based PDF
   - Maximum file size per file: 10MB
   - You can upload up to 3 files simultaneously

### System Requirements

- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection for API access

### First Time Setup

1. Open the application in your browser
2. Click the language switcher to choose your preferred language (EN/HU)
3. Enter your Gemini API key in the provided field
   - Your API key will be saved in your browser
   - You won't need to enter it again unless you clear your browser data

---

## Using the Application

### Step-by-Step Process

#### 1. Enter Your API Key

- Click on the API key input field
- Paste your Google Gemini API key
- The key is automatically saved to your browser's local storage
- Click the link to get your API key if you don't have one yet

#### 2. Upload PDF File(s)

**Uploading Files:**
- Click the upload button to select PDF files
- You can select up to 3 files at once
- Selected files will appear in a list below
- Remove any file by clicking the ✕ button
- The counter shows how many files you have (e.g., "2/3")

**File Requirements:**
- Format: PDF only
- Maximum size per file: 10MB
- Must contain nutrition information
- You can upload multiple files for batch processing

#### 3. Extract Data

- Click the "Extract Data" button
- Watch the progress bar (typically 2-5 seconds)
- Wait for results to appear

#### 4. View and Export Results

Once extraction is complete:

- **View Results**: Scroll down to see extracted data from the last processed file
- **Copy JSON**: Click "Copy JSON" to copy results to clipboard
- **Download JSON**: Click "Download JSON" to save as JSON file
- **Print PDF**: Click "Print PDF" to generate a printable PDF report
- **View History**: Click "▶ Show History" to access previous extractions

#### 5. Access Your History

- Click "▶ Show History" to view your extraction history
- See up to 10 previous extractions
- Click "View" on any history item to reload that result
- History is automatically saved in your browser

---

## Understanding the Results

### Extracted Data Structure

The application extracts two types of data:

#### Allergens (10 Major Allergens)

| Allergen | Description |
|----------|-------------|
| **Gluten** | Wheat, barley, rye, oats |
| **Egg** | Eggs and egg products |
| **Crustaceans** | Shrimp, lobster, crab |
| **Fish** | All fish species |
| **Peanut** | Peanuts and peanut products |
| **Soy** | Soybeans and soy products |
| **Milk** | Milk and dairy products |
| **Tree Nuts** | Almonds, walnuts, hazelnuts, etc. |
| **Celery** | Celery and celery products |
| **Mustard** | Mustard seeds and mustard products |

**Display Format:**
- - **Green indicator** = Allergen is present
- ⚪ **Gray indicator** = Allergen is not present

#### Nutritional Values (6 Core Nutrients)

| Nutrient | Description |
|----------|-------------|
| **Energy** | Energy value in kJ or kcal |
| **Fat** | Total fat content in grams |
| **Carbohydrate** | Total carbohydrates in grams |
| **Sugar** | Sugar content in grams |
| **Protein** | Protein content in grams |
| **Sodium** | Sodium content in grams |

**Display Format:**
- Shows the value extracted from the PDF (e.g., "1173 kJ", "18.9 g")
- May display "N/A" if information is not found or unclear

### Result Metadata

Each extraction also includes:

- **Processing Time**: How long the extraction took (in seconds)
- **LLM Used**: Which AI model was used (typically "gemini")
- **Success Status**: Whether extraction completed successfully

### Export Options

The application now offers three ways to save and use your results:

**1. Copy JSON** - Copy results to your clipboard for quick access

**2. Download JSON** - Download results as a JSON file for data integration

**3. Print PDF** - Generate a formatted PDF report ready for printing

**JSON Format:**
The exported JSON contains:
```json
{
  "success": true,
  "allergens": {
    "gluten": false,
    "egg": true,
    ...
  },
  "nutrients": {
    "energy": "1173 kJ",
    "fat": "18.9 g",
    ...
  },
  "llm_used": "gemini",
  "processing_time": 2.45
}
```

---

## Troubleshooting

### Common Issues and Solutions

#### 1. "Gemini API key required" Error

**Problem:** You haven't entered an API key or it's invalid.

**Solution:**
- Make sure you've entered your Gemini API key
- Check if the key is correct (no extra spaces)
- Get a new API key from [Google AI Studio](https://ai.google.dev/)
- Make sure your API key has not expired

#### 2. "Only PDF files are allowed" Error

**Problem:** You're trying to upload a non-PDF file.

**Solution:**
- Only upload PDF files (`.pdf` extension)
- Convert other file types to PDF first
- Make sure the file extension is correct

#### 3. "File too large" Error

**Problem:** Your PDF exceeds the 10MB limit.

**Solution:**
- Compress your PDF using online tools
- Reduce the resolution of scanned images
- Split large PDFs into smaller files

#### 4. "Empty file" Error

**Problem:** The uploaded file is empty or corrupted.

**Solution:**
- Re-download the original PDF
- Check if the file opens in a PDF viewer
- Try a different PDF file

#### 5. All Allergens Show as "Present"

**Problem:** Incorrect extraction results.

**Causes:**
- PDF format is unusual or unclear
- Text is not properly structured
- OCR failed for scanned documents

**Solutions:**
- Try with a different PDF format
- Ensure the document is clear and readable
- Check if nutrition table is clearly visible
- Use a real PDF instead of a scanned one

#### 6. Nutrients Show "N/A"

**Problem:** Nutritional values couldn't be extracted.

**Causes:**
- Nutritional information is in an unusual format
- OCR errors in scanned documents
- Table structure is not recognized

**Solutions:**
- Ensure nutrition table is clearly visible
- Try higher quality scanned documents
- Use original PDF instead of scanned version
- Check if nutrient names are clear

#### 7. Processing Takes Too Long

**Problem:** Extraction is taking more than 30 seconds.

**Causes:**
- Large or complex PDF files
- Slow internet connection
- API service issues

**Solutions:**
- Wait for processing to complete (timeout is 2 minutes)
- Check your internet connection
- Try with a smaller PDF file
- Refresh the page and try again

#### 8. "Backend connection refused" Error

**Problem:** Cannot connect to the backend server.

**Solution:**
- Make sure the backend is running
- Check if you're using the correct URL
- Contact your administrator if this is a hosted instance

#### 9. Results Look Incorrect

**Problem:** Extracted values don't match the PDF.

**Causes:**
- AI misinterpretation
- Unclear document format

**Solutions:**
- Verify original document
- Check PDF quality
- Try manual verification for critical data
- Provide feedback to improve accuracy

---

## Frequently Asked Questions

### General Questions

**Q: Is my API key secure?**  
A: Yes! Your API key is stored locally in your browser and never sent to our servers. Only Google receives your API key for processing.

**Q: Can I use this offline?**  
A: No, the application requires internet connection to access the Google Gemini API.

**Q: Is there a limit on how many PDFs I can process?**  
A: The limit depends on your Google Gemini API quota. Free tier includes generous usage limits.

**Q: Do you store my PDFs?**  
A: No! PDFs are processed in memory and never stored on any server. Everything is processed and discarded immediately.

**Q: Is this service free?**  
A: The application is free to use, but Google Gemini API has usage limits. Check Google AI Studio for current pricing.

**Q: Which browsers are supported?**  
A: All modern browsers including Chrome, Firefox, Safari, and Edge.

### Data Accuracy Questions

**Q: How accurate is the extraction?**  
A: Accuracy depends on PDF quality and format. Typically 90-95% for well-structured documents. Always verify critical data.

**Q: Can I trust the extracted allergen information?**  
A: While the AI is highly accurate, always verify allergen information for safety-critical applications. This tool is a time-saver, not a replacement for human review for critical safety data.

**Q: What happens if the PDF has multiple languages?**  
A: The system supports multiple languages including English, Hungarian, French, and Spanish. It will automatically detect and extract data.

**Q: Can it read handwriting in PDFs?**  
A: No, the system is designed for printed or typed text. Handwritten text may not be accurately extracted.

### Technical Questions

**Q: What file formats are supported?**  
A: Only PDF files are currently supported (`.pdf` extension).

**Q: What's the maximum file size?**  
A: 10MB is the current maximum file size.

**Q: How long does processing take?**  
A: Typically 2-5 seconds for real PDFs, 5-10 seconds for scanned documents.

**Q: What happens if I upload a scanned document?**  
A: The system uses OCR (Optical Character Recognition) to extract text from images. This takes slightly longer but works well for clear scanned documents.

**Q: Can I process multiple PDFs at once?**  
A: Currently, you can process one PDF at a time. For multiple files, process them one by one.

**Q: Where can I find the API documentation?**  
A: API documentation is available at `/docs` endpoint when the backend is running (e.g., `http://localhost:8000/docs`).

### Export and Integration Questions

**Q: Can I export results to Excel?**  
A: Currently, only JSON export is available. You can convert JSON to Excel using online tools or Excel's data import feature.

**Q: Can I integrate this into my own application?**  
A: Yes! Use the API endpoints. Documentation is in the Developer Guide.

**Q: Can I run this on my own server?**  
A: Yes, see the deployment documentation for self-hosting instructions.

---

## Tips for Best Results

### PDF Quality Tips

1. **Use original PDFs when possible** - Not scanned copies
2. **Ensure clear nutrition tables** - Well-formatted tables extract better
3. **Good scan quality** - If using scanned PDFs, use at least 300 DPI
4. **Avoid handwritten notes** - Printed text extracts more accurately
5. **Proper orientation** - Make sure the PDF is not rotated or upside-down

### Data Extraction Tips

1. **Verify critical data** - Always double-check allergen information for safety
2. **Check units** - Make sure units (g, kg, ml) are correctly extracted
3. **Review N/A values** - If many values are N/A, the document format might not be supported
4. **Export results** - Save your results using the export feature

### Performance Tips

1. **Optimize PDFs** - Smaller files process faster
2. **Good internet** - Faster connection means faster processing
3. **Clear browser cache** - If having issues, clear cache and try again
4. **Update browser** - Use the latest browser version for best performance

---

## Support and Feedback

### Getting Help

If you encounter issues not covered in this guide:

1. Check the troubleshooting section above
2. Review the error message for specific details
3. Contact your administrator (for hosted instances)
4. Visit the project repository for updates

### Reporting Issues

When reporting issues, please provide:

- Description of the problem
- Error message (if any)
- PDF type (real or scanned)
- File size
- Steps to reproduce
- Browser and operating system

### Feature Requests

Have ideas for improvements? We'd love to hear them!

- Faster processing
- Additional export formats
- Support for more languages
- Batch processing
- Other suggestions

---

## Privacy and Security

### Data Privacy

- **No data storage** - Your PDFs are never stored
- **Local processing** - Data stays in your browser until upload
- **Immediate deletion** - Data is deleted after processing
- **No tracking** - No analytics or tracking

### API Key Security

- Store securely - Don't share your API key
- Rotate regularly - Update your key periodically
- Browser storage - Keys are stored locally
- HTTPS recommended - Use secure connection when available

### Best Practices

- Don't upload sensitive documents if concerned about privacy
- Use secure network connections (HTTPS)
- Keep your API key private
- Log out when finished on shared computers

---

## Updates and Version Information

**Current Version:** 1.0.0  
**Last Updated:** October 2025

### What's New

- AI-powered extraction with Google Gemini
- Support for scanned documents (OCR)
- Multi-language support (EN, HU)
- Real-time progress tracking
- JSON export functionality
- Modern, responsive interface

### Future Features

Planned for upcoming versions:

- Support for more export formats (CSV, Excel)
- Batch processing multiple PDFs
- Additional language support
- Result history and caching
- Enhanced OCR accuracy
- Custom allergen lists

---

## Contact

For questions, issues, or feedback:

- **GitHub Issues:** Report bugs or request features
- **Documentation:** Check online docs for detailed information
- **Email Support:** Contact your administrator

---

## Acknowledgments

This application uses:

- **Google Gemini** - For AI-powered text extraction
- **FastAPI** - For the robust backend framework
- **React** - For the modern user interface
- **Open Source Community** - For excellent tools and libraries

Thank you for using Nutrition & Allergen Extractor!

