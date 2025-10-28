import logging
import sys
from app.core.config import settings

def setup_logging():
    """Configures logging for the application"""
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, settings.LOG_LEVEL))
    console_handler.setFormatter(formatter)
    
    # Add handler to root logger
    root_logger.addHandler(console_handler)
    
    # Configure logging for our modules
    modules_to_log = [
        'app.services.nutrition_extractor',
        'app.services.pdf_processor', 
        'app.services.llm_service',
        'app.api.endpoints'
    ]
    
    for module in modules_to_log:
        logger = logging.getLogger(module)
        logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # Reduce logging level for external libraries
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('httpcore').setLevel(logging.WARNING)
    logging.getLogger('openai').setLevel(logging.WARNING)
    logging.getLogger('PIL').setLevel(logging.WARNING)
    
    logging.info("Logging configured successfully")
