"""
Tests for the Flask application
"""

import pytest
import json
from src.app import create_app


@pytest.fixture
def app():
    """Create test application"""
    app = create_app("testing")
    yield app


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


class TestHealthEndpoint:
    """Tests for health check endpoint"""
    
    def test_health_check(self, client):
        """Test health check returns 200"""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data["status"] == "healthy"
        assert "version" in data
        assert data["service"] == "develop_copilit"


class TestAPIInfo:
    """Tests for API info endpoint"""
    
    def test_api_info(self, client):
        """Test API info endpoint"""
        response = client.get("/api/v1/info")
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert "api_version" in data
        assert "features" in data
        assert isinstance(data["features"], list)


class TestCompletionEndpoint:
    """Tests for code completion endpoint"""
    
    def test_complete_with_valid_code(self, client):
        """Test completion with valid code"""
        payload = {
            "code": "def hello",
            "language": "python"
        }
        
        response = client.post(
            "/api/v1/complete",
            data=json.dumps(payload),
            content_type="application/json"
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "completions" in data
        assert "suggestions" in data
        assert isinstance(data["completions"], list)
    
    def test_complete_without_code(self, client):
        """Test completion without code parameter"""
        payload = {}
        
        response = client.post(
            "/api/v1/complete",
            data=json.dumps(payload),
            content_type="application/json"
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
    
    def test_complete_with_javascript(self, client):
        """Test completion with JavaScript"""
        payload = {
            "code": "function test",
            "language": "javascript"
        }
        
        response = client.post(
            "/api/v1/complete",
            data=json.dumps(payload),
            content_type="application/json"
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "completions" in data


class TestAnalysisEndpoint:
    """Tests for code analysis endpoint"""
    
    def test_analyze_valid_code(self, client):
        """Test analysis with valid code"""
        payload = {
            "code": "def hello():\n    print('world')",
            "language": "python"
        }
        
        response = client.post(
            "/api/v1/analyze",
            data=json.dumps(payload),
            content_type="application/json"
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "analysis" in data
        assert "refactoring_suggestions" in data
    
    def test_analyze_without_code(self, client):
        """Test analysis without code parameter"""
        payload = {}
        
        response = client.post(
            "/api/v1/analyze",
            data=json.dumps(payload),
            content_type="application/json"
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data


class TestTemplateEndpoint:
    """Tests for template generation endpoint"""
    
    def test_generate_function_template(self, client):
        """Test function template generation"""
        payload = {
            "type": "function",
            "language": "python",
            "name": "my_func",
            "params": "x, y"
        }
        
        response = client.post(
            "/api/v1/template",
            data=json.dumps(payload),
            content_type="application/json"
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "template" in data
        assert "my_func" in data["template"]
    
    def test_generate_class_template(self, client):
        """Test class template generation"""
        payload = {
            "type": "class",
            "language": "python",
            "name": "MyClass"
        }
        
        response = client.post(
            "/api/v1/template",
            data=json.dumps(payload),
            content_type="application/json"
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "template" in data
        assert "MyClass" in data["template"]
    
    def test_generate_without_type(self, client):
        """Test template generation without type"""
        payload = {}
        
        response = client.post(
            "/api/v1/template",
            data=json.dumps(payload),
            content_type="application/json"
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
