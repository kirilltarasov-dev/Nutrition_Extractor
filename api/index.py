"""
Vercel serverless handler for FastAPI backend
"""
import sys
import os

# Add backend directory to path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, backend_path)

# Import the FastAPI app
from app.main import app

# Export for Vercel - the app itself is the handler
# Vercel's @vercel/python wrapper handles ASGI apps directly
# The handler variable is what Vercel looks for
handler = app
