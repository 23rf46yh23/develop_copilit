"""
Code completion module
"""

from typing import List, Dict, Any


class CodeCompleter:
    """
    Provides code completion suggestions based on context
    """
    
    def __init__(self):
        self.completion_templates = {
            "python": {
                "function": "def {name}({params}):\n    pass",
                "class": "class {name}:\n    def __init__(self):\n        pass",
                "if": "if {condition}:\n    pass",
                "for": "for {var} in {iterable}:\n    pass",
            },
            "javascript": {
                "function": "function {name}({params}) {{\n    // TODO\n}}",
                "class": "class {name} {{\n    constructor() {{\n        // TODO\n    }}\n}}",
                "if": "if ({condition}) {{\n    // TODO\n}}",
                "for": "for (let {var} of {iterable}) {{\n    // TODO\n}}",
            }
        }
    
    def get_completions(self, code: str, language: str = "python", cursor_position: int = None) -> List[Dict[str, Any]]:
        """
        Get code completion suggestions
        
        Args:
            code: The current code context
            language: Programming language (default: python)
            cursor_position: Current cursor position
            
        Returns:
            List of completion suggestions
        """
        completions = []
        
        # Simple keyword-based completions
        keywords = {
            "python": ["def", "class", "if", "for", "while", "import", "from", "return", "try", "except"],
            "javascript": ["function", "class", "if", "for", "while", "const", "let", "return", "try", "catch"]
        }
        
        lang_keywords = keywords.get(language, keywords["python"])
        
        for keyword in lang_keywords:
            completions.append({
                "text": keyword,
                "type": "keyword",
                "description": f"{language} keyword"
            })
        
        return completions
    
    def get_template(self, template_type: str, language: str = "python", **kwargs) -> str:
        """
        Get code template
        
        Args:
            template_type: Type of template (function, class, etc.)
            language: Programming language
            **kwargs: Template variables
            
        Returns:
            Formatted template string
        """
        templates = self.completion_templates.get(language, {})
        template = templates.get(template_type, "")
        
        try:
            return template.format(**kwargs)
        except KeyError:
            return template
    
    def suggest_next_line(self, code: str, language: str = "python") -> List[str]:
        """
        Suggest next line of code based on context
        
        Args:
            code: Current code
            language: Programming language
            
        Returns:
            List of suggested next lines
        """
        suggestions = []
        
        lines = code.strip().split("\n")
        if not lines:
            return suggestions
        
        last_line = lines[-1].strip()
        
        # Simple heuristics for suggestions
        if last_line.endswith(":"):
            suggestions.append("    pass")
        elif "import" in last_line and language == "python":
            suggestions.append("import os")
            suggestions.append("import sys")
        elif "function" in last_line or "def" in last_line:
            suggestions.append("    return None")
        
        return suggestions
