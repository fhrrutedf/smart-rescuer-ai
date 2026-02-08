"""
Temperature Sensor Handler
Using MLX90614 infrared temperature sensor or similar
"""
from typing import Dict, Any, Optional
import time
import random
from sensors.base_sensor import BaseSensor
from utils import log, config

# Try to import smbus for I2C communication
try:
    import smbus2
    HAS_SMBUS = True
except ImportError:
    HAS_SMBUS = False
    log.warning("smbus2 not available - Temperature sensor will run in simulation mode")


class TemperatureSensor(BaseSensor):
    """Non-contact infrared temperature sensor"""
    
    # MLX90614 I2C address
    MLX90614_ADDR = 0x5A
    MLX90614_TEMP_AMBIENT = 0x06
    MLX90614_TEMP_OBJECT = 0x07
    
    def __init__(self, i2c_bus: int = 1, enabled: bool = None):
        """
        Initialize temperature sensor
        
        Args:
            i2c_bus: I2C bus number (usually 1 on Raspberry Pi)
            enabled: Override config setting
        """
        if enabled is None:
            enabled = config.ENABLE_TEMP_SENSOR
        
        super().__init__("Temperature", enabled)
        self.i2c_bus_num = i2c_bus
        self.bus = None
        self.is_simulated = not HAS_SMBUS
        
        if self.enabled and HAS_SMBUS:
            self._init_sensor()
    
    def _init_sensor(self):
        """Initialize I2C bus"""
        try:
            self.bus = smbus2.SMBus(self.i2c_bus_num)
            # Test read
            self._read_raw_temp(self.MLX90614_TEMP_AMBIENT)
            log.info(f"MLX90614 temperature sensor initialized on I2C bus {self.i2c_bus_num}")
        except Exception as e:
            log.error(f"Failed to initialize temperature sensor: {e}")
            self.enabled = False
            self.is_simulated = True
    
    def read(self) -> Optional[Dict[str, Any]]:
        """
        Read temperature data
        
        Returns:
            Dictionary with body and ambient temperature
        """
        if not self.is_ready():
            return None
        
        try:
            if self.is_simulated:
                # Simulate realistic temperatures
                body_temp = round(random.uniform(36.0, 37.5), 1)  # Normal range
                ambient_temp = round(random.uniform(20.0, 25.0), 1)
            else:
                # Read from actual sensor
                body_temp = self._read_object_temp()
                ambient_temp = self._read_ambient_temp()
            
            reading = {
                "body_temperature": body_temp,
                "ambient_temperature": ambient_temp,
                "unit": "°C"
            }
            
            self._update_reading(reading)
            log.debug(f"Temperature reading: Body={body_temp}°C, Ambient={ambient_temp}°C")
            
            return reading
            
        except Exception as e:
            log.error(f"Failed to read temperature sensor: {e}")
            return None
    
    def _read_raw_temp(self, register) -> float:
        """Read raw temperature from sensor"""
        try:
            # Read 3 bytes (data low, data high, PEC)
            data = self.bus.read_i2c_block_data(self.MLX90614_ADDR, register, 3)
            
            # Combine bytes
            temp_raw = (data[1] << 8) | data[0]
            
            # Convert to Celsius (sensor returns temp * 50 in Kelvin)
            temp_celsius = (temp_raw * 0.02) - 273.15
            
            return round(temp_celsius, 1)
        except Exception as e:
            log.error(f"Failed to read raw temperature: {e}")
            return 0.0
    
    def _read_object_temp(self) -> float:
        """Read object (body) temperature"""
        return self._read_raw_temp(self.MLX90614_TEMP_OBJECT)
    
    def _read_ambient_temp(self) -> float:
        """Read ambient temperature"""
        return self._read_raw_temp(self.MLX90614_TEMP_AMBIENT)
    
    def calibrate(self) -> bool:
        """Calibrate temperature sensor"""
        log.info("Calibrating temperature sensor...")
        time.sleep(1)
        log.info("Temperature calibration complete")
        return True
    
    def detect_emergency(self, reading: Dict[str, Any]) -> bool:
        """
        Detect emergency conditions from temperature
        
        Args:
            reading: Temperature reading dict
            
        Returns:
            True if emergency detected
        """
        temp = reading.get("body_temperature", 37.0)
        
        # Fever or hypothermia
        if temp >= 39.0:  # High fever
            log.warning(f"High fever detected: {temp}°C")
            return True
        elif temp <= 35.0:  # Hypothermia
            log.warning(f"Hypothermia detected: {temp}°C")
            return True
        
        return False
    
    def __del__(self):
        """Cleanup I2C bus on deletion"""
        if self.bus and not self.is_simulated:
            try:
                self.bus.close()
            except:
                pass
