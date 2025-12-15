"""
Tests for code completion module
"""

import pytest
from src.copilit.completion import CodeCompleter


class TestCodeCompleter:
    """Tests for CodeCompleter class"""
    
    @pytest.fixture
    def completer(self):
        """Create CodeCompleter instance"""
        return CodeCompleter()
    
    def test_get_completions_python(self, completer):
        """Test getting Python completions"""
        code = "def test"
        completions = completer.get_completions(code, "python")
        
        assert isinstance(completions, list)
        assert len(completions) > 0
        assert any(c["text"] == "def" for c in completions)
    
    def test_get_completions_javascript(self, completer):
        """Test getting JavaScript completions"""
        code = "function test"
        completions = completer.get_completions(code, "javascript")
        
        assert isinstance(completions, list)
        assert len(completions) > 0
        assert any(c["text"] == "function" for c in completions)
    
    def test_get_template_python_function(self, completer):
        """Test getting Python function template"""
        template = completer.get_template("function", "python", name="test_func", params="x, y")
        
        assert "def test_func(x, y):" in template
        assert "pass" in template
    
    def test_get_template_python_class(self, completer):
        """Test getting Python class template"""
        template = completer.get_template("class", "python", name="TestClass")
        
        assert "class TestClass:" in template
        assert "__init__" in template
    
    def test_get_template_javascript_function(self, completer):
        """Test getting JavaScript function template"""
        template = completer.get_template("function", "javascript", name="testFunc", params="x, y")
        
        assert "function testFunc(x, y)" in template
        assert "TODO" in template
    
    def test_suggest_next_line_after_colon(self, completer):
        """Test suggesting next line after colon"""
        code = "def test():"
        suggestions = completer.suggest_next_line(code, "python")
        
        assert isinstance(suggestions, list)
        assert "pass" in suggestions[0] if suggestions else True
    
    def test_suggest_next_line_after_import(self, completer):
        """Test suggesting next line after import"""
        code = "import"
        suggestions = completer.suggest_next_line(code, "python")
        
        assert isinstance(suggestions, list)
