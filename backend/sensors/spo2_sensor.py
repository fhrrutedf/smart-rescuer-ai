"""
SpO2 (Blood Oxygen Saturation) and Heart Rate Sensor
Using MAX30100 or MAX30102 pulse oximeter sensor
"""
from typing import Dict, Any, Optional
import time
import random
from sensors.base_sensor import BaseSensor
from utils import log, config

# Try to import MAX30102 library
try:
    from max30102 import MAX30102
    HAS_MAX30102 = True
except ImportError:
    HAS_MAX30102 = False
    log.warning("MAX30102 library not available - SpO2 sensor will run in simulation mode")


class SpO2Sensor(BaseSensor):
    """SpO2 and Heart Rate Sensor"""
    
    def __init__(self, enabled: bool = None):
        """
        Initialize SpO2 sensor
        
        Args:
            enabled: Override config setting
        """
        if enabled is None:
            enabled = config.ENABLE_SPO2_SENSOR
        
        super().__init__("SpO2", enabled)
        self.is_simulated = not HAS_MAX30102
        self.sensor = None
        
        if self.enabled and HAS_MAX30102:
            self._init_sensor()
    
    def _init_sensor(self):
        """Initialize MAX30102 sensor"""
        try:
            self.sensor = MAX30102()
            self.sensor.setup()
            log.info("MAX30102 sensor initialized successfully")
        except Exception as e:
            log.error(f"Failed to initialize MAX30102: {e}")
            self.enabled = False
            self.is_simulated = True
    
    def read(self) -> Optional[Dict[str, Any]]:
        """
        Read SpO2 and heart rate data
        
        Returns:
            Dictionary with SpO2, heart rate, and confidence
        """
        if not self.is_ready():
            return None
        
        try:
            if self.is_simulated:
                # Simulate realistic readings
                spo2 = random.randint(95, 100)  # Normal range
                heart_rate = random.randint(60, 100)
                confidence = random.uniform(0.8, 1.0)
            else:
                # Read from actual sensor
                red, ir = self.sensor.read_sequential()
                spo2, heart_rate = self._calculate_spo2_hr(red, ir)
                confidence = self._calculate_confidence(red, ir)
            
            reading = {
                "spo2": spo2,
                "heart_rate": heart_rate,
                "confidence": confidence,
                "unit": "%"
            }
            
            self._update_reading(reading)
            log.debug(f"SpO2 reading: {spo2}%, HR={heart_rate} bpm")
            
            return reading
            
        except Exception as e:
            log.error(f"Failed to read SpO2 sensor: {e}")
            return None
    
    def _calculate_spo2_hr(self, red_data, ir_data) -> tuple:
        """
        Calculate SpO2 and heart rate from raw sensor data
        
        Args:
            red_data: Red LED sensor data
            ir_data: Infrared LED sensor data
            
        Returns:
            Tuple of (spo2, heart_rate)
        """
        # Simplified calculation - in production use proper algorithms
        # like the one from Maxim Integrated
        spo2 = 97  # Placeholder
        heart_rate = 75  # Placeholder
        return spo2, heart_rate
    
    def _calculate_confidence(self, red_data, ir_data) -> float:
        """Calculate reading confidence based on signal quality"""
        return 0.9  # Placeholder
    
    def calibrate(self) -> bool:
        """Calibrate SpO2 sensor"""
        log.info("Calibrating SpO2 sensor...")
        
        if not self.is_simulated and self.sensor:
            try:
                # Perform calibration
                self.sensor.shutdown()
                time.sleep(0.5)
                self.sensor.setup()
                log.info("SpO2 calibration complete")
                return True
            except Exception as e:
                log.error(f"SpO2 calibration failed: {e}")
                return False
        else:
            time.sleep(1)
            log.info("SpO2 calibration complete (simulated)")
            return True
    
    def detect_emergency(self, reading: Dict[str, Any]) -> bool:
        """
        Detect emergency conditions from SpO2 reading
        
        Args:
            reading: SpO2 reading dict
            
        Returns:
            True if emergency detected
        """
        spo2 = reading.get("spo2", 100)
        confidence = reading.get("confidence", 0)
        
        # Low confidence readings should be rechecked
        if confidence < 0.7:
            return False
        
        # Critical hypoxemia
        if spo2 < 90:
            log.warning(f"Critical SpO2 detected: {spo2}%")
            return True
        
        return False
    
    def __del__(self):
        """Cleanup sensor on deletion"""
        if self.sensor and not self.is_simulated:
            try:
                self.sensor.shutdown()
            except:
                pass
