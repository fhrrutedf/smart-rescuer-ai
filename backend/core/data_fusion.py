"""
Data Fusion Engine
Combines sensor data, AI analysis, and generates comprehensive assessment
"""
from typing import Dict, Any, Optional
from datetime import datetime
import cv2
import numpy as np
from sensors import ECGSensor, SpO2Sensor, TemperatureSensor, GPSModule
from ai_engine import InjuryDetector, SeverityScorer
from utils import log


class DataFusionEngine:
    """Main engine for combining all data sources"""
    
    def __init__(self):
        """Initialize data fusion engine"""
        # Initialize sensors
        self.ecg_sensor = ECGSensor()
        self.spo2_sensor = SpO2Sensor()
        self.temp_sensor = TemperatureSensor()
        self.gps_module = GPSModule()
        
        # Initialize AI components
        self.injury_detector = InjuryDetector()
        self.severity_scorer = SeverityScorer()
        
        log.info("Data Fusion Engine initialized")
    
    def perform_emergency_assessment(
        self,
        image_path: Optional[str] = None,
        patient_conscious: bool = True
    ) -> Dict[str, Any]:
        """
        Perform complete emergency assessment
        
        Args:
            image_path: Path to injury image (optional)
            patient_conscious: Whether patient is conscious
            
        Returns:
            Complete assessment report
        """
        import time
        start_time = time.time()
        log.info("Starting emergency assessment...")
        assessment_time = datetime.now()
        
        try:
            # Step 1: Collect vital signs
            step_start = time.time()
            log.info("Collecting vital signs...")
            vital_signs = self._collect_vital_signs()
            log.info(f"✓ Vital signs collected in {time.time() - step_start:.2f}s")
            
            # Step 2: Detect injuries (if image provided)
            injuries = []
            if image_path:
                step_start = time.time()
                log.info("Analyzing injuries from image...")
                injuries = self.injury_detector.detect_from_image(image_path)
                log.info(f"✓ Injury detection completed in {time.time() - step_start:.2f}s")
            
            # Step 3: Get location
            step_start = time.time()
            log.info("Getting GPS location...")
            location = self.gps_module.read()
            log.info(f"✓ GPS location obtained in {time.time() - step_start:.2f}s")
            
            # Step 4: Calculate severity score
            step_start = time.time()
            log.info("Calculating severity score...")
            severity_result = self.severity_scorer.calculate_score(
                injuries=injuries,
                vital_signs=vital_signs,
                patient_conscious=patient_conscious
            )
            log.info(f"✓ Severity score calculated in {time.time() - step_start:.2f}s")
            
            # Step 5: Build comprehensive assessment
            assessment = {
                "timestamp": assessment_time.isoformat(),
                "vital_signs": vital_signs,
                "injuries": injuries,
                "injury_summary": self.injury_detector.get_injury_summary(injuries),
                "location": location,
                "severity": severity_result,
                "patient_conscious": patient_conscious,
                "requires_ems": severity_result.get("requires_immediate_attention", False)
            }
            
            total_time = time.time() - start_time
            log.info(f"✅ Assessment complete in {total_time:.2f}s - Severity: {severity_result['severity_level']}")
            
            return assessment
            
        except Exception as e:
            log.error(f"Emergency assessment failed: {e}")
            return {
                "timestamp": assessment_time.isoformat(),
                "error": str(e),
                "status": "failed"
            }
    
    def _collect_vital_signs(self) -> Dict[str, Any]:
        """Collect data from all vital sign sensors"""
        vital_signs = {}
        
        try:
            # ECG
            ecg_data = self.ecg_sensor.read()
            if ecg_data:
                vital_signs.update({
                    "heart_rate": ecg_data.get("heart_rate"),
                    "rhythm": ecg_data.get("rhythm")
                })
            
            # SpO2
            spo2_data = self.spo2_sensor.read()
            if spo2_data:
                vital_signs["spo2"] = spo2_data.get("spo2")
                # Use SpO2 heart rate if ECG not available
                if "heart_rate" not in vital_signs:
                    vital_signs["heart_rate"] = spo2_data.get("heart_rate")
            
            # Temperature
            temp_data = self.temp_sensor.read()
            if temp_data:
                vital_signs["body_temperature"] = temp_data.get("body_temperature")
                vital_signs["ambient_temperature"] = temp_data.get("ambient_temperature")
            
        except Exception as e:
            log.error(f"Error collecting vital signs: {e}")
        
        return vital_signs
    
    def calibrate_all_sensors(self) -> Dict[str, bool]:
        """Calibrate all sensors"""
        log.info("Calibrating all sensors...")
        
        results = {
            "ecg": self.ecg_sensor.calibrate(),
            "spo2": self.spo2_sensor.calibrate(),
            "temperature": self.temp_sensor.calibrate(),
            "gps": self.gps_module.calibrate()
        }
        
        log.info(f"Calibration results: {results}")
        return results
    
    def get_sensor_status(self) -> Dict[str, Any]:
        """Get status of all sensors"""
        return {
            "ecg": {
                "enabled": self.ecg_sensor.enabled,
                "ready": self.ecg_sensor.is_ready(),
                "simulated": getattr(self.ecg_sensor, 'is_simulated', False)
            },
            "spo2": {
                "enabled": self.spo2_sensor.enabled,
                "ready": self.spo2_sensor.is_ready(),
                "simulated": getattr(self.spo2_sensor, 'is_simulated', False)
            },
            "temperature": {
                "enabled": self.temp_sensor.enabled,
                "ready": self.temp_sensor.is_ready(),
                "simulated": getattr(self.temp_sensor, 'is_simulated', False)
            },
            "gps": {
                "enabled": self.gps_module.enabled,
                "ready": self.gps_module.is_ready(),
                "has_fix": self.gps_module.has_fix(),
                "simulated": getattr(self.gps_module, 'is_simulated', False)
            }
        }
