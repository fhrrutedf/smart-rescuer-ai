"""
Pydantic models for API requests/responses
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class VitalSigns(BaseModel):
    """Vital signs data"""
    heart_rate: Optional[int] = Field(None, description="Heart rate in BPM")
    spo2: Optional[float] = Field(None, description="Blood oxygen saturation %")
    body_temperature: Optional[float] = Field(None, description="Body temperature in Celsius")
    rhythm: Optional[str] = Field(None, description="ECG rhythm")


class Location(BaseModel):
    """GPS location data"""
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    altitude: Optional[float] = None
    accuracy: Optional[int] = None


class Injury(BaseModel):
    """Detected injury"""
    type: str
    confidence: float
    severity: str


class SeverityScore(BaseModel):
    """Severity assessment"""
    total_score: float
    severity_level: str
    requires_immediate_attention: bool
    critical_factors: List[str] = []


class EmergencyAssessmentRequest(BaseModel):
    """Request for emergency assessment"""
    patient_conscious: bool = True
    image_path: Optional[str] = None


class EmergencyAssessmentResponse(BaseModel):
    """Emergency assessment result"""
    timestamp: str
    vital_signs: VitalSigns
    injuries: List[Injury]
    injury_summary: str
    location: Optional[Location]
    severity: SeverityScore
    patient_conscious: bool
    requires_ems: bool


class ChatMessage(BaseModel):
    """Chat message"""
    message: str
    reset_history: bool = False


class ChatResponse(BaseModel):
    """Chatbot response"""
    message: str
    is_emergency: bool
    model: Optional[str] = None


class SensorStatus(BaseModel):
    """Sensor status"""
    enabled: bool
    ready: bool
    simulated: bool = False
    has_fix: Optional[bool] = None


class SystemStatus(BaseModel):
    """Overall system status"""
    sensors: Dict[str, SensorStatus]
    version: str
    debug_mode: bool
