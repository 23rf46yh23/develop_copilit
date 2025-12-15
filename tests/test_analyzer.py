"""
Tests for code analyzer module
"""

import pytest
from src.copilit.analyzer import CodeAnalyzer


class TestCodeAnalyzer:
    """Tests for CodeAnalyzer class"""
    
    @pytest.fixture
    def analyzer(self):
        """Create CodeAnalyzer instance"""
        return CodeAnalyzer()
    
    def test_analyze_python_code(self, analyzer):
        """Test analyzing Python code"""
        code = """
def hello():
    print('world')

class TestClass:
    pass
"""
        analysis = analyzer.analyze_code(code, "python")
        
        assert analysis["language"] == "python"
        assert "hello" in analysis["functions"]
        assert "TestClass" in analysis["classes"]
        assert isinstance(analysis["issues"], list)
    
    def test_analyze_javascript_code(self, analyzer):
        """Test analyzing JavaScript code"""
        code = """
function hello() {
    console.log('world');
}

class TestClass {
}
"""
        analysis = analyzer.analyze_code(code, "javascript")
        
        assert analysis["language"] == "javascript"
        assert "hello" in analysis["functions"]
        assert "TestClass" in analysis["classes"]
    
    def test_check_long_lines(self, analyzer):
        """Test checking for long lines"""
        code = "x = " + "a" * 120  # Create a very long line
        analysis = analyzer.analyze_code(code, "python")
        
        assert len(analysis["issues"]) > 0
        assert any(issue["type"] == "style" for issue in analysis["issues"])
    
    def test_check_todo_comments(self, analyzer):
        """Test checking for TODO comments"""
        code = "# TODO: implement this\npass"
        analysis = analyzer.analyze_code(code, "python")
        
        assert len(analysis["issues"]) > 0
        assert any(issue["type"] == "todo" for issue in analysis["issues"])
    
    def test_get_complexity_simple(self, analyzer):
        """Test complexity calculation for simple code"""
        code = "x = 1\ny = 2"
        complexity = analyzer.get_complexity(code)
        
        assert complexity >= 1
    
    def test_get_complexity_with_conditionals(self, analyzer):
        """Test complexity calculation with conditionals"""
        code = """
if x > 0:
    if y > 0:
        pass
    elif y < 0:
        pass
for i in range(10):
    pass
"""
        complexity = analyzer.get_complexity(code)
        
        assert complexity > 3
    
    def test_suggest_refactoring_high_complexity(self, analyzer):
        """Test refactoring suggestions for high complexity"""
        # Create code with high complexity
        code = "if x: pass\n" * 15
        suggestions = analyzer.suggest_refactoring(code, "python")
        
        assert len(suggestions) > 0
        assert any(s["type"] == "complexity" for s in suggestions)
    
    def test_suggest_refactoring_long_code(self, analyzer):
        """Test refactoring suggestions for long code"""
        code = "\n".join([f"x{i} = {i}" for i in range(60)])
        suggestions = analyzer.suggest_refactoring(code, "python")
        
        assert len(suggestions) > 0
        assert any(s["type"] == "length" for s in suggestions)
