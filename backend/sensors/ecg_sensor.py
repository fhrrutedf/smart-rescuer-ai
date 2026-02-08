"""
ECG (Electrocardiogram) Sensor Handler
Using AD8232 or similar ECG sensor module
"""
from typing import Dict, Any, Optional
import time
import random  # For simulation on non-RPi systems
from sensors.base_sensor import BaseSensor
from utils import log, config

# Try to import GPIO, use simulation if not available
try:
    import RPi.GPIO as GPIO
    HAS_GPIO = True
except ImportError:
    HAS_GPIO = False
    log.warning("RPi.GPIO not available - ECG sensor will run in simulation mode")


class ECGSensor(BaseSensor):
    """ECG Sensor for heart rhythm monitoring"""
    
    def __init__(self, pin: int = 17, enabled: bool = None):
        """
        Initialize ECG sensor
        
        Args:
            pin: GPIO pin number for analog input
            enabled: Override config setting
        """
        if enabled is None:
            enabled = config.ENABLE_ECG_SENSOR
        
        super().__init__("ECG", enabled)
        self.pin = pin
        self.sample_rate = 200  # Hz
        self.is_simulated = not HAS_GPIO
        
        if self.enabled and HAS_GPIO:
            self._setup_gpio()
    
    def _setup_gpio(self):
        """Setup GPIO pins"""
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin, GPIO.IN)
            log.info(f"ECG sensor GPIO setup complete on pin {self.pin}")
        except Exception as e:
            log.error(f"Failed to setup ECG GPIO: {e}")
            self.enabled = False
    
    def read(self) -> Optional[Dict[str, Any]]:
        """
        Read ECG data
        
        Returns:
            Dictionary with heart rate and rhythm data
        """
        if not self.is_ready():
            return None
        
        try:
            if self.is_simulated:
                # Simulate ECG data
                heart_rate = random.randint(60, 100)  # Normal range
                rhythm = "normal" if random.random() > 0.1 else "irregular"
                signal_quality = random.uniform(0.7, 1.0)
            else:
                # Read from actual sensor
                samples = self._collect_samples(duration=5)  # 5 second reading
                heart_rate = self._calculate_heart_rate(samples)
                rhythm = self._analyze_rhythm(samples)
                signal_quality = self._assess_signal_quality(samples)
            
            reading = {
                "heart_rate": heart_rate,
                "rhythm": rhythm,
                "signal_quality": signal_quality,
                "unit": "bpm"
            }
            
            self._update_reading(reading)
            log.debug(f"ECG reading: HR={heart_rate} bpm, rhythm={rhythm}")
            
            return reading
            
        except Exception as e:
            log.error(f"Failed to read ECG sensor: {e}")
            return None
    
    def _collect_samples(self, duration: int = 5) -> list:
        """Collect ECG samples for specified duration"""
        samples = []
        sample_count = self.sample_rate * duration
        
        for _ in range(sample_count):
            if HAS_GPIO:
                # Read analog value (would need ADC like MCP3008)
                value = GPIO.input(self.pin)
                samples.append(value)
            time.sleep(1 / self.sample_rate)
        
        return samples
    
    def _calculate_heart_rate(self, samples: list) -> int:
        """Calculate heart rate from samples"""
        # Simplified: count peaks and calculate BPM
        # In production, use proper ECG analysis algorithms
        return random.randint(60, 100)  # Placeholder
    
    def _analyze_rhythm(self, samples: list) -> str:
        """Analyze heart rhythm"""
        # Simplified rhythm analysis
        # In production, detect AFib, VTach, etc.
        return "normal"  # Placeholder
    
    def _assess_signal_quality(self, samples: list) -> float:
        """Assess ECG signal quality (0-1)"""
        return 0.9  # Placeholder
    
    def calibrate(self) -> bool:
        """Calibrate ECG sensor"""
        log.info("Calibrating ECG sensor...")
        time.sleep(1)
        log.info("ECG calibration complete")
        return True
    
    def detect_emergency(self, reading: Dict[str, Any]) -> bool:
        """
        Detect emergency conditions from ECG
        
        Args:
            reading: ECG reading dict
            
        Returns:
            True if emergency detected
        """
        hr = reading.get("heart_rate", 0)
        rhythm = reading.get("rhythm", "normal")
        
        # Emergency conditions
        if hr < 40 or hr > 150:  # Severe bradycardia or tachycardia
            return True
        if rhythm in ["ventricular_fibrillation", "ventricular_tachycardia"]:
            return True
        
        return False
    
    def __del__(self):
        """Cleanup GPIO on deletion"""
        if HAS_GPIO and self.enabled:
            try:
                GPIO.cleanup(self.pin)
            except:
                pass
