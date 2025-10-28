"""Pytest configuration and fixtures"""
import pytest
from starlette.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Create test client for FastAPI app"""
    import app.main
    return TestClient(app.main.app)


@pytest.fixture
def sample_pdf_data():
    """Sample PDF data for testing"""
    return b"%PDF-1.4\nfake pdf content"


@pytest.fixture
def sample_text():
    """Sample extracted text"""
    return "Sample PDF text with nutrients and allergens"


@pytest.fixture
def sample_allergens():
    """Sample allergen data"""
    from app.models.schemas import AllergenData
    return AllergenData(gluten=True, milk=True)


@pytest.fixture
def sample_nutrients():
    """Sample nutrition data"""
    from app.models.schemas import NutritionData
    return NutritionData(energy="100 kJ", fat="5 g", protein="10 g")


@pytest.fixture
def sample_gemini_key():
    """Sample Gemini API key"""
    return "test_api_key_12345"

