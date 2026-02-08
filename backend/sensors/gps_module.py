"""
GPS Module Handler
For location tracking using serial GPS module
"""
from typing import Dict, Any, Optional
import time
import random
from sensors.base_sensor import BaseSensor
from utils import log, config

# Try to import GPS libraries
try:
    import serial
    import pynmea2
    HAS_GPS = True
except ImportError:
    HAS_GPS = False
    log.warning("GPS libraries not available - GPS will run in simulation mode")


class GPSModule(BaseSensor):
    """GPS module for location tracking"""
    
    def __init__(self, port: str = None, baudrate: int = None, enabled: bool = None):
        """
        Initialize GPS module
        
        Args:
            port: Serial port (e.g., /dev/ttyUSB0)
            baudrate: Baud rate for serial communication
            enabled: Override config setting
        """
        if enabled is None:
            enabled = config.ENABLE_GPS
        
        super().__init__("GPS", enabled)
        
        self.port = port or config.GPS_PORT
        self.baudrate = baudrate or config.GPS_BAUDRATE
        self.serial = None
        self.is_simulated = not HAS_GPS
        
        if self.enabled and HAS_GPS:
            self._init_gps()
    
    def _init_gps(self):
        """Initialize serial connection to GPS"""
        try:
            self.serial = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=1
            )
            log.info(f"GPS module initialized on {self.port} at {self.baudrate} baud")
        except Exception as e:
            log.error(f"Failed to initialize GPS: {e}")
            self.enabled = False
            self.is_simulated = True
    
    def read(self) -> Optional[Dict[str, Any]]:
        """
        Read GPS location data
        
        Returns:
            Dictionary with latitude, longitude, altitude, speed, etc.
        """
        if not self.is_ready():
            return None
        
        try:
            if self.is_simulated:
                # Simulate GPS data (Riyadh, Saudi Arabia coordinates)
                latitude = 24.7136 + random.uniform(-0.1, 0.1)
                longitude = 46.6753 + random.uniform(-0.1, 0.1)
                altitude = random.uniform(600, 650)
                speed = random.uniform(0, 20)
                satellites = random.randint(6, 12)
                fix_quality = 1  # GPS fix
            else:
                # Read from actual GPS
                gps_data = self._read_gps_sentence()
                if not gps_data:
                    return None
                
                latitude = gps_data.get("latitude")
                longitude = gps_data.get("longitude")
                altitude = gps_data.get("altitude", 0)
                speed = gps_data.get("speed", 0)
                satellites = gps_data.get("satellites", 0)
                fix_quality = gps_data.get("fix_quality", 0)
            
            reading = {
                "latitude": round(latitude, 6),
                "longitude": round(longitude, 6),
                "altitude": round(altitude, 1),
                "speed": round(speed, 1),
                "satellites": satellites,
                "fix_quality": fix_quality,
                "timestamp": time.time()
            }
            
            self._update_reading(reading)
            log.debug(f"GPS reading: {latitude:.6f}, {longitude:.6f}")
            
            return reading
            
        except Exception as e:
            log.error(f"Failed to read GPS: {e}")
            return None
    
    def _read_gps_sentence(self) -> Optional[Dict[str, Any]]:
        """Read and parse NMEA sentence from GPS"""
        try:
            # Read lines until we get a valid GGA or RMC sentence
            for _ in range(10):
                line = self.serial.readline().decode('ascii', errors='ignore')
                
                if line.startswith('$GPGGA') or line.startswith('$GNGGA'):
                    msg = pynmea2.parse(line)
                    return {
                        "latitude": msg.latitude,
                        "longitude": msg.longitude,
                        "altitude": msg.altitude,
                        "satellites": msg.num_sats,
                        "fix_quality": msg.gps_qual
                    }
                elif line.startswith('$GPRMC') or line.startswith('$GNRMC'):
                    msg = pynmea2.parse(line)
                    return {
                        "latitude": msg.latitude,
                        "longitude": msg.longitude,
                        "speed": msg.spd_over_grnd if hasattr(msg, 'spd_over_grnd') else 0,
                        "fix_quality": 1 if msg.status == 'A' else 0
                    }
            
            return None
            
        except Exception as e:
            log.error(f"Failed to parse GPS sentence: {e}")
            return None
    
    def get_location_string(self) -> str:
        """Get human-readable location string"""
        reading = self.get_last_reading()
        if not reading or not reading.get("value"):
            return "Location unavailable"
        
        data = reading["value"]
        lat = data.get("latitude", 0)
        lon = data.get("longitude", 0)
        
        # Format as degrees
        lat_dir = "N" if lat >= 0 else "S"
        lon_dir = "E" if lon >= 0 else "W"
        
        return f"{abs(lat):.6f}°{lat_dir}, {abs(lon):.6f}°{lon_dir}"
    
    def get_google_maps_url(self) -> Optional[str]:
        """Get Google Maps URL for current location"""
        reading = self.get_last_reading()
        if not reading or not reading.get("value"):
            return None
        
        data = reading["value"]
        lat = data.get("latitude")
        lon = data.get("longitude")
        
        if lat and lon:
            return f"https://www.google.com/maps?q={lat},{lon}"
        
        return None
    
    def calibrate(self) -> bool:
        """GPS doesn't require calibration"""
        log.info("GPS module ready (no calibration needed)")
        return True
    
    def has_fix(self) -> bool:
        """Check if GPS has valid fix"""
        reading = self.get_last_reading()
        if not reading or not reading.get("value"):
            return False
        
        return reading["value"].get("fix_quality", 0) > 0
    
    def __del__(self):
        """Cleanup serial connection on deletion"""
        if self.serial and not self.is_simulated:
            try:
                self.serial.close()
            except:
                pass
