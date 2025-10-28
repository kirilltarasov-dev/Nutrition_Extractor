import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css';
import enTranslations from './locales/en';
import huTranslations from './locales/hu';

// Get base URL
const getApiUrl = () => {
  // Use environment variable if set, otherwise fallback
  return process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';
};

const API_URL = getApiUrl();

function App() {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [apiKey, setApiKey] = useState('');
  const [language, setLanguage] = useState('en');
  const [validationError, setValidationError] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [history, setHistory] = useState([]);
  const [showHistory, setShowHistory] = useState(false);

  const fileInputRef = useRef(null);

  const translations = language === 'en' ? enTranslations : huTranslations;

  // Load API key and history from localStorage
  useEffect(() => {
    const savedKey = localStorage.getItem('gemini_api_key');
    if (savedKey) {
      setApiKey(savedKey);
    }
    
    const savedHistory = localStorage.getItem('nutrition_history');
    if (savedHistory) {
      try {
        const parsedHistory = JSON.parse(savedHistory);
        setHistory(parsedHistory);
      } catch (e) {
        console.error('Error loading history:', e);
      }
    }
  }, []);

  // Save API key to localStorage
  const handleApiKeyChange = (value) => {
    setApiKey(value);
    localStorage.setItem('gemini_api_key', value);
  };

  const validateFile = (file) => {
    setValidationError(null);
    
    // Check file type
    if (file.type !== 'application/pdf') {
      setValidationError(language === 'en' ? 'Only PDF files are allowed' : 'Csak PDF fájlok megengedettek');
      return false;
    }
    
    // Check file size (max 10MB)
    const maxSize = 10 * 1024 * 1024; // 10MB
    if (file.size > maxSize) {
      setValidationError(language === 'en' ? 'File size must be less than 10MB' : 'A fájl mérete nem lehet nagyobb 10MB-nál');
      return false;
    }
    
    if (file.size === 0) {
      setValidationError(language === 'en' ? 'File is empty' : 'A fájl üres');
      return false;
    }
    
    return true;
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      const selectedFiles = Array.from(e.target.files);
      
      // Check if adding more files would exceed the limit
      if (files.length + selectedFiles.length > 3) {
        setValidationError(language === 'en' ? 'Maximum 3 files allowed' : 'Maximum 3 fájl engedélyezett');
        return;
      }
      
      // Validate all selected files
      const validFiles = selectedFiles.filter(validateFile);
      
      if (validFiles.length > 0) {
        setFiles(prevFiles => [...prevFiles, ...validFiles]);
        setError(null);
        setValidationError(null);
      }
      
      // Reset input to allow selecting the same file again
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };


  const handleCopyJSON = () => {
    if (results) {
      const jsonString = JSON.stringify(results, null, 2);
      navigator.clipboard.writeText(jsonString).then(() => {
        alert(language === 'en' ? 'Results copied to clipboard!' : 'Eredmények vágólapra másolva!');
      });
    }
  };

  const handleDownloadJSON = () => {
    if (results) {
      const jsonString = JSON.stringify(results, null, 2);
      const blob = new Blob([jsonString], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `nutrition-data-${Date.now()}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }
  };

  const handlePrintPDF = () => {
    if (!results) return;
    
    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
      <!DOCTYPE html>
      <html>
        <head>
          <title>Nutrition Report</title>
          <style>
            body {
              font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
              padding: 40px;
              color: #333;
            }
            .header {
              text-align: center;
              margin-bottom: 40px;
              border-bottom: 3px solid #667eea;
              padding-bottom: 20px;
            }
            .header h1 {
              color: #667eea;
              margin: 0;
              font-size: 28px;
            }
            .header .subtitle {
              color: #666;
              margin-top: 10px;
            }
            .meta {
              text-align: center;
              color: #888;
              margin-bottom: 30px;
              font-size: 12px;
            }
            .section {
              margin-bottom: 40px;
              page-break-inside: avoid;
            }
            .section h2 {
              color: #333;
              border-bottom: 2px solid #667eea;
              padding-bottom: 10px;
              margin-bottom: 20px;
              font-size: 20px;
            }
            .grid {
              display: grid;
              grid-template-columns: repeat(3, 1fr);
              gap: 15px;
            }
            .item {
              padding: 15px;
              border: 1px solid #e0e0e0;
              border-radius: 8px;
              background: #f8f9fa;
            }
            .item.present {
              background: #fff3cd;
              border-left: 4px solid #ffc107;
            }
            .item.absent {
              background: #d4edda;
              border-left: 4px solid #28a745;
            }
            .label {
              display: block;
              font-weight: 600;
              margin-bottom: 5px;
              color: #555;
              font-size: 13px;
              text-transform: capitalize;
            }
            .value {
              display: block;
              font-size: 18px;
              color: #667eea;
              font-weight: 700;
            }
            .allergen-value {
              font-size: 14px;
              font-weight: 700;
            }
            @media print {
              body { padding: 20px; }
              .header { border-bottom: 2px solid #667eea; }
            }
          </style>
        </head>
        <body>
          <div class="header">
            <h1>${translations.title}</h1>
            <div class="subtitle">Nutrition & Allergen Analysis Report</div>
          </div>
          
          <div class="meta">
            Generated: ${new Date().toLocaleString()}<br>
            Processing Time: ${results.processing_time?.toFixed(2)}s | Powered by: Google Gemini
          </div>
          
          <div class="section">
            <h2>Nutritional Values</h2>
            <div class="grid">
              ${Object.entries(results.nutrients || {}).map(([key, value]) => `
                <div class="item">
                  <span class="label">${key.replace('_', ' ')}</span>
                  <span class="value">${value}</span>
                </div>
              `).join('')}
            </div>
          </div>
          
          <div class="section">
            <h2>Allergens</h2>
            <div class="grid">
              ${Object.entries(results.allergens || {}).map(([key, value]) => `
                <div class="item ${value ? 'present' : 'absent'}">
                  <span class="label">${key.replace('_', ' ')}</span>
                  <span class="allergen-value">${value ? 'Present' : 'Not Present'}</span>
                </div>
              `).join('')}
            </div>
          </div>
          
          <div class="meta" style="margin-top: 60px; border-top: 1px solid #e0e0e0; padding-top: 20px;">
            This report was generated by Nutrition & Allergen Extractor<br>
            For more information, visit the application
          </div>
        </body>
      </html>
    `);
    
    printWindow.document.close();
    
    // Wait for content to load, then print
    setTimeout(() => {
      printWindow.print();
    }, 500);
  };


  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (files.length === 0) {
      setError(language === 'en' ? 'Please select at least one file' : 'Kérjük, válasszon legalább egy fájlt');
      return;
    }

    if (!apiKey) {
      setError(language === 'en' ? 'Please enter your Gemini API key' : 'Kérjük, adja meg a Gemini API kulcsot');
      return;
    }

    if (validationError) {
      return;
    }

    setLoading(true);
    setError(null);
    setUploadProgress(0);

    try {
      const allResults = [];
      
      for (let i = 0; i < files.length; i++) {
        const file = files[i];
        setUploadProgress((i / files.length) * 100);
        
        const formData = new FormData();
        formData.append('file', file);
        formData.append('gemini_api_key', apiKey);

        const response = await axios.post(`${API_URL}/extract`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          timeout: 120000,
        });

        allResults.push({
          fileName: file.name,
          data: response.data
        });
      }

      setUploadProgress(100);
      
      // Save to history (most recent extraction)
      if (allResults.length > 0) {
        const latestResult = allResults[allResults.length - 1];
        const historyEntry = {
          id: Date.now(),
          timestamp: new Date().toISOString(),
          fileName: latestResult.fileName,
          data: latestResult.data
        };
        const updatedHistory = [historyEntry, ...history].slice(0, 10);
        setHistory(updatedHistory);
        localStorage.setItem('nutrition_history', JSON.stringify(updatedHistory));
        
        // Display the last result
        setResults(latestResult.data);
      }
      
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    } finally {
      setTimeout(() => {
        setLoading(false);
        setUploadProgress(0);
      }, 500);
    }
  };

  const capitalizeLabel = (key) => {
    return key.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
  };

  return (
    <div className="App">
      <header className="App-header">
          <div className="header-content">
            <h1>{translations.title}</h1>
            <p>{translations.subtitle}</p>
            <div className="header-description">
              <span className="feature-badge">⚡ Async Processing</span>
              <span className="feature-description">
                Powered by async backend architecture for ultra-fast data extraction and processing
              </span>
            </div>
          <div className="language-switcher">
            <button 
              className={language === 'en' ? 'active' : ''} 
              onClick={() => setLanguage('en')}
              type="button"
            >
              EN
            </button>
            <button 
              className={language === 'hu' ? 'active' : ''} 
              onClick={() => setLanguage('hu')}
              type="button"
            >
              HU
            </button>
          </div>
        </div>
      </header>

      <main className="App-main">
        <form onSubmit={handleSubmit} className="upload-form">
          <div className="form-group">
            <label htmlFor="api-key">{translations.apiKeyLabel}</label>
            <input
              id="api-key"
              type="password"
              value={apiKey}
              onChange={(e) => handleApiKeyChange(e.target.value)}
              placeholder={translations.apiKeyPlaceholder}
              disabled={loading}
            />
            <small>{translations.apiKeyHint} <a href="https://ai.google.dev/" target="_blank" rel="noopener noreferrer">Google AI Studio</a></small>
          </div>

          <div className="form-group">
            <label htmlFor="file-input">{translations.fileLabel} ({files.length}/3)</label>
            <input
              ref={fileInputRef}
              id="file-input"
              type="file"
              accept=".pdf"
              multiple
              onChange={handleFileChange}
              disabled={loading || files.length >= 3}
            />
            
            {files.length > 0 && (
              <div className="files-list">
                {files.map((file, index) => (
                  <div key={index} className="file-info-row">
                    <span className="file-icon-large">📄</span>
                    <div className="file-details">
                      <span className="file-name">{file.name}</span>
                      <span className="file-size">{(file.size / 1024).toFixed(2)} KB</span>
                    </div>
                    <button
                      type="button"
                      onClick={() => setFiles(files.filter((_, i) => i !== index))}
                      className="file-remove-btn"
                    >
                      ✕
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>

          <button type="submit" disabled={loading || files.length === 0 || !apiKey || validationError}>
            {loading ? translations.processing : translations.extractButton}
          </button>
        </form>

        {history.length > 0 && (
          <div className="history-section">
            <button 
              type="button" 
              className="history-toggle-btn"
              onClick={() => setShowHistory(!showHistory)}
            >
              {showHistory ? (language === 'en' ? '▼ Hide History' : '▼ Előzmények elrejtése') : (language === 'en' ? '▶ Show History' : '▶ Előzmények megtekintése')} ({history.length})
            </button>
            
            {showHistory && (
              <div className="history-container">
                {history.map((entry) => (
                  <div key={entry.id} className="history-item">
                    <div className="history-item-header">
                      <span className="history-filename">{entry.fileName}</span>
                      <span className="history-date">
                        {new Date(entry.timestamp).toLocaleString(language === 'en' ? 'en-US' : 'hu-HU')}
                      </span>
                    </div>
                    <button
                      type="button"
                      className="history-view-btn"
                      onClick={() => setResults(entry.data)}
                    >
                      {language === 'en' ? 'View' : 'Megtekintés'}
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {validationError && (
          <div className="error-message validation-error">
            {validationError}
          </div>
        )}

        {loading && (
          <div className="progress-container">
            <div className="progress-bar">
              <div className="progress-bar-fill" style={{ width: `${uploadProgress}%` }}></div>
            </div>
            <p className="progress-text">{uploadProgress}% {language === 'en' ? 'Processing...' : 'Feldolgozás...'}</p>
          </div>
        )}

        {error && (
          <div className="error-message">
            {translations.error}: {error}
          </div>
        )}

        {results && (
          <div className="results">
            <div className="results-header">
              <h2>{translations.extractedData}</h2>
              <div className="results-actions">
                <div className="export-buttons">
                  <button className="export-btn" onClick={handleCopyJSON}>
                    {language === 'en' ? 'Copy JSON' : 'JSON másolása'}
                  </button>
                  <button className="export-btn" onClick={handleDownloadJSON}>
                    {language === 'en' ? 'Download JSON' : 'JSON letöltése'}
                  </button>
                  <button className="export-btn" onClick={handlePrintPDF}>
                    {language === 'en' ? 'Print PDF' : 'PDF nyomtatása'}
                  </button>
                </div>
              </div>
            </div>
            
            {results.success ? (
              <>
                <div className="results-section">
                  <h3>{translations.nutritionalValues}</h3>
                  <div className="nutrients-grid">
                    {Object.entries(results.nutrients || {}).map(([key, value]) => (
                      <div key={key} className="nutrient-item">
                        <span className="nutrient-label">{capitalizeLabel(key)}:</span>
                        <span className="nutrient-value">{value}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="results-section">
                  <h3>{translations.allergens}</h3>
                  <div className="allergens-grid">
                    {Object.entries(results.allergens || {}).map(([key, value]) => (
                      <div key={key} className={`allergen-item ${value ? 'present' : 'absent'}`}>
                        <span className="allergen-label">{capitalizeLabel(key)}:</span>
                        <span className="allergen-value">{value ? translations.present : translations.notPresent}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="results-meta">
                  <p>{translations.poweredBy}: <strong>Google Gemini</strong></p>
                  <p>{translations.processingTime}: <strong>{results.processing_time?.toFixed(2)}s</strong></p>
                </div>
              </>
            ) : (
              <div className="error-message">
                {translations.extractFailed}: {results.error}
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
