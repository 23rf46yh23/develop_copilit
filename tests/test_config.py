"""
Tests for configuration module
"""

import pytest
from src.config import Config, DevelopmentConfig, ProductionConfig, TestingConfig, get_config


class TestConfig:
    """Tests for configuration classes"""
    
    def test_base_config(self):
        """Test base configuration"""
        assert hasattr(Config, "FLASK_ENV")
        assert hasattr(Config, "HOST")
        assert hasattr(Config, "PORT")
        assert hasattr(Config, "API_VERSION")
    
    def test_development_config(self):
        """Test development configuration"""
        assert DevelopmentConfig.DEBUG is True
    
    def test_production_config(self):
        """Test production configuration"""
        assert ProductionConfig.DEBUG is False
        assert ProductionConfig.FLASK_ENV == "production"
    
    def test_testing_config(self):
        """Test testing configuration"""
        assert TestingConfig.TESTING is True
        assert TestingConfig.DEBUG is True
    
    def test_get_config_development(self):
        """Test getting development config"""
        config = get_config("development")
        assert config == DevelopmentConfig
    
    def test_get_config_production(self):
        """Test getting production config"""
        config = get_config("production")
        assert config == ProductionConfig
    
    def test_get_config_testing(self):
        """Test getting testing config"""
        config = get_config("testing")
        assert config == TestingConfig
    
    def test_config_as_dict(self):
        """Test configuration as dictionary"""
        config_dict = Config.as_dict()
        assert isinstance(config_dict, dict)
        assert "FLASK_ENV" in config_dict
        assert "HOST" in config_dict
