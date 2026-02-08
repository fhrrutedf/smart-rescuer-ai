"""
Configuration management for Smart Rescuer
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    """Application configuration"""
    
    # App Settings
    APP_NAME = os.getenv("APP_NAME", "Smart Rescuer")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    ENV = os.getenv("ENV", "development")
    
    # API Settings
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/smart_rescuer.db")
    
    # AI Models
    AI_MODEL_PATH = Path(os.getenv("AI_MODEL_PATH", BASE_DIR / "ai_engine" / "models"))
    INJURY_MODEL_NAME = os.getenv("INJURY_MODEL_NAME", "injury_detector.tflite")
    SEVERITY_MODEL_NAME = os.getenv("SEVERITY_MODEL_NAME", "severity_scorer.onnx")
    CHATBOT_MODEL_NAME = os.getenv("CHATBOT_MODEL_NAME", "medalpaca")
    
    # Sensors
    ENABLE_ECG_SENSOR = os.getenv("ENABLE_ECG_SENSOR", "False").lower() == "true"
    ENABLE_SPO2_SENSOR = os.getenv("ENABLE_SPO2_SENSOR", "False").lower() == "true"
    ENABLE_TEMP_SENSOR = os.getenv("ENABLE_TEMP_SENSOR", "False").lower() == "true"
    ENABLE_GPS = os.getenv("ENABLE_GPS", "False").lower() == "true"
    
    # GPS Settings
    GPS_PORT = os.getenv("GPS_PORT", "/dev/ttyUSB0")
    GPS_BAUDRATE = int(os.getenv("GPS_BAUDRATE", "9600"))
    
    # Emergency Services
    EMS_API_ENDPOINT = os.getenv("EMS_API_ENDPOINT", "")
    EMS_API_KEY = os.getenv("EMS_API_KEY", "")
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = Path(os.getenv("LOG_FILE", BASE_DIR / "logs" / "smart_rescuer.log"))
    
    # Frontend
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
    
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")
    
    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they don't exist"""
        cls.AI_MODEL_PATH.mkdir(parents=True, exist_ok=True)
        cls.LOG_FILE.parent.mkdir(parents=True, exist_ok=True)


# Create config instance
config = Config()
config.ensure_directories()
