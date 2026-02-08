"""
Base sensor class for all medical sensors
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime
from utils import log


class BaseSensor(ABC):
    """Abstract base class for all sensors"""
    
    def __init__(self, name: str, enabled: bool = True):
        self.name = name
        self.enabled = enabled
        self.last_reading = None
        self.last_reading_time = None
        log.info(f"Initialized {name} sensor (enabled={enabled})")
    
    @abstractmethod
    def read(self) -> Optional[Dict[str, Any]]:
        """Read data from the sensor"""
        pass
    
    @abstractmethod
    def calibrate(self) -> bool:
        """Calibrate the sensor"""
        pass
    
    def is_ready(self) -> bool:
        """Check if sensor is ready to read"""
        return self.enabled
    
    def get_last_reading(self) -> Optional[Dict[str, Any]]:
        """Get the last reading"""
        return {
            "value": self.last_reading,
            "timestamp": self.last_reading_time,
            "sensor": self.name
        } if self.last_reading is not None else None
    
    def _update_reading(self, value: Any):
        """Update the last reading"""
        self.last_reading = value
        self.last_reading_time = datetime.now()
