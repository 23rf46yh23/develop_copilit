"""
Main Flask application
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import logging

from src.config import get_config
from src.copilit import CodeCompleter, CodeAnalyzer


def create_app(config_name: str = None) -> Flask:
    """
    Create and configure the Flask application
    
    Args:
        config_name: Configuration name (development, production, testing)
        
    Returns:
        Configured Flask application
    """
    app = Flask(__name__)
    
    # Load configuration
    config = get_config(config_name)
    app.config.from_object(config)
    
    # Enable CORS
    CORS(app)
    
    # Setup logging
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Initialize components
    completer = CodeCompleter()
    analyzer = CodeAnalyzer()
    
    # Health check endpoint
    @app.route("/health", methods=["GET"])
    def health_check():
        """Health check endpoint"""
        return jsonify({
            "status": "healthy",
            "version": "0.1.0",
            "service": "develop_copilit"
        })
    
    # API version endpoint
    @app.route(f"/api/{config.API_VERSION}/info", methods=["GET"])
    def api_info():
        """API information endpoint"""
        return jsonify({
            "api_version": config.API_VERSION,
            "features": [
                "code_completion",
                "code_analysis",
                "template_generation"
            ]
        })
    
    # Code completion endpoint
    @app.route(f"/api/{config.API_VERSION}/complete", methods=["POST"])
    def complete():
        """
        Code completion endpoint
        
        Request body:
            {
                "code": "def hello",
                "language": "python",
                "cursor_position": 10
            }
        """
        try:
            data = request.get_json()
            
            if not data or "code" not in data:
                return jsonify({"error": "Missing 'code' in request"}), 400
            
            code = data["code"]
            language = data.get("language", "python")
            cursor_position = data.get("cursor_position")
            
            completions = completer.get_completions(code, language, cursor_position)
            suggestions = completer.suggest_next_line(code, language)
            
            return jsonify({
                "completions": completions,
                "suggestions": suggestions
            })
        
        except Exception as e:
            app.logger.error(f"Error in complete endpoint: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500
    
    # Code analysis endpoint
    @app.route(f"/api/{config.API_VERSION}/analyze", methods=["POST"])
    def analyze():
        """
        Code analysis endpoint
        
        Request body:
            {
                "code": "def hello():\\n    print('world')",
                "language": "python"
            }
        """
        try:
            data = request.get_json()
            
            if not data or "code" not in data:
                return jsonify({"error": "Missing 'code' in request"}), 400
            
            code = data["code"]
            language = data.get("language", "python")
            
            analysis = analyzer.analyze_code(code, language)
            refactoring = analyzer.suggest_refactoring(code, language)
            
            return jsonify({
                "analysis": analysis,
                "refactoring_suggestions": refactoring
            })
        
        except Exception as e:
            app.logger.error(f"Error in analyze endpoint: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500
    
    # Template generation endpoint
    @app.route(f"/api/{config.API_VERSION}/template", methods=["POST"])
    def generate_template():
        """
        Template generation endpoint
        
        Request body:
            {
                "type": "function",
                "language": "python",
                "name": "my_function",
                "params": "x, y"
            }
        """
        try:
            data = request.get_json()
            
            if not data or "type" not in data:
                return jsonify({"error": "Missing 'type' in request"}), 400
            
            template_type = data["type"]
            language = data.get("language", "python")
            kwargs = {k: v for k, v in data.items() if k not in ["type", "language"]}
            
            template = completer.get_template(template_type, language, **kwargs)
            
            return jsonify({
                "template": template
            })
        
        except Exception as e:
            app.logger.error(f"Error in template endpoint: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500
    
    return app


def main():
    """Main entry point"""
    app = create_app()
    config = get_config()
    
    app.logger.info(f"Starting Develop Copilit on {config.HOST}:{config.PORT}")
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)


if __name__ == "__main__":
    main()
