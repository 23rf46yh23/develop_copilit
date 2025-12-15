"""
Code analysis module
"""

import re
from typing import List, Dict, Any


class CodeAnalyzer:
    """
    Analyzes code for patterns, issues, and suggestions
    """
    
    def __init__(self):
        self.patterns = {
            "python": {
                "function_def": r"def\s+(\w+)\s*\(",
                "class_def": r"class\s+(\w+)[\s\(:]",
                "import": r"(?:from\s+[\w\.]+\s+)?import\s+([\w\s,]+)",
            },
            "javascript": {
                "function_def": r"function\s+(\w+)\s*\(",
                "class_def": r"class\s+(\w+)\s*\{",
                "import": r"import\s+.*?\s+from\s+['\"](.+?)['\"]",
            }
        }
    
    def analyze_code(self, code: str, language: str = "python") -> Dict[str, Any]:
        """
        Analyze code and return insights
        
        Args:
            code: Code to analyze
            language: Programming language
            
        Returns:
            Dictionary containing analysis results
        """
        analysis = {
            "language": language,
            "lines": len(code.split("\n")),
            "functions": [],
            "classes": [],
            "imports": [],
            "issues": [],
        }
        
        patterns = self.patterns.get(language, self.patterns["python"])
        
        # Find functions
        for match in re.finditer(patterns["function_def"], code):
            analysis["functions"].append(match.group(1))
        
        # Find classes
        for match in re.finditer(patterns["class_def"], code):
            analysis["classes"].append(match.group(1))
        
        # Find imports
        for match in re.finditer(patterns["import"], code):
            analysis["imports"].append(match.group(1).strip())
        
        # Check for common issues
        analysis["issues"] = self._check_issues(code, language)
        
        return analysis
    
    def _check_issues(self, code: str, language: str) -> List[Dict[str, str]]:
        """
        Check for common code issues
        
        Args:
            code: Code to check
            language: Programming language
            
        Returns:
            List of issues found
        """
        issues = []
        
        lines = code.split("\n")
        
        for i, line in enumerate(lines, 1):
            # Check line length
            if len(line) > 100:
                issues.append({
                    "line": i,
                    "type": "style",
                    "message": "Line exceeds 100 characters"
                })
            
            # Check for TODO comments
            if "TODO" in line or "FIXME" in line:
                issues.append({
                    "line": i,
                    "type": "todo",
                    "message": "TODO/FIXME found"
                })
        
        return issues
    
    def get_complexity(self, code: str) -> int:
        """
        Calculate cyclomatic complexity (simplified)
        
        Args:
            code: Code to analyze
            
        Returns:
            Complexity score
        """
        complexity = 1  # Base complexity
        
        # Count decision points
        decision_keywords = ["if", "elif", "else", "for", "while", "try", "except", "and", "or"]
        
        for keyword in decision_keywords:
            complexity += code.count(keyword)
        
        return complexity
    
    def suggest_refactoring(self, code: str, language: str = "python") -> List[Dict[str, str]]:
        """
        Suggest refactoring opportunities
        
        Args:
            code: Code to analyze
            language: Programming language
            
        Returns:
            List of refactoring suggestions
        """
        suggestions = []
        
        # Check complexity
        complexity = self.get_complexity(code)
        if complexity > 10:
            suggestions.append({
                "type": "complexity",
                "message": f"High complexity ({complexity}). Consider breaking into smaller functions."
            })
        
        # Check for long functions
        lines = code.split("\n")
        if len(lines) > 50:
            suggestions.append({
                "type": "length",
                "message": "Function/file is long. Consider splitting into smaller units."
            })
        
        return suggestions
