"""
Injury Detection using Computer Vision
Detects physical injuries from camera images
"""
from typing import Dict, Any, Optional, List
import cv2
import numpy as np
from pathlib import Path
from utils import log, config

# Optimize TensorFlow before importing
try:
    from utils import tf_optimizer
except ImportError:
    pass  # If optimizer not available, continue without it

# Try to import TensorFlow Lite
try:
    import tflite_runtime.interpreter as tflite
    HAS_TFLITE = True
except ImportError:
    try:
        import tensorflow.lite as tflite
        HAS_TFLITE = True
    except ImportError:
        HAS_TFLITE = False
        log.warning("TFLite not available - Injury detection will use rule-based fallback")


class InjuryDetector:
    """Computer Vision-based injury detection"""
    
    # Injury classes that the model can detect
    INJURY_CLASSES = [
        "no_injury",
        "bleeding",
        "bruise",
        "burn",
        "cut",
        "fracture",
        "swelling"
    ]
    
    def __init__(self, model_path: Optional[Path] = None):
        """
        Initialize injury detector
        
        Args:
            model_path: Path to TFLite model file
        """
        self.model_path = model_path or (config.AI_MODEL_PATH / config.INJURY_MODEL_NAME)
        self.interpreter = None
        self.input_details = None
        self.output_details = None
        self.is_model_loaded = False
        
        if HAS_TFLITE and self.model_path.exists():
            self._load_model()
        else:
            log.warning(f"Model not found at {self.model_path}, using rule-based detection")
    
    def _load_model(self):
        """Load TFLite model"""
        try:
            self.interpreter = tflite.Interpreter(model_path=str(self.model_path))
            self.interpreter.allocate_tensors()
            
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            
            self.is_model_loaded = True
            log.info(f"Injury detection model loaded from {self.model_path}")
        except Exception as e:
            log.error(f"Failed to load injury detection model: {e}")
            self.is_model_loaded = False
    
    def detect_from_image(self, image_path: str) -> List[Dict[str, Any]]:
        """
        Detect injuries from image file
        
        Args:
            image_path: Path to image file
            
        Returns:
            List of detected injuries with confidence scores
        """
        try:
            image = cv2.imread(image_path)
            if image is None:
                log.error(f"Failed to load image: {image_path}")
                return []
            
            return self.detect(image)
        except Exception as e:
            log.error(f"Error detecting injuries from image: {e}")
            return []
    
    def detect(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """
        Detect injuries from image array
        
        Args:
            image: OpenCV image (BGR format)
            
        Returns:
            List of detected injuries with confidence scores
        """
        import time
        start_time = time.time()
        
        if self.is_model_loaded:
            log.info("Using AI model for injury detection...")
            result = self._detect_with_model(image)
            log.info(f"AI model detection took {time.time() - start_time:.2f}s")
            return result
        else:
            log.info("Using rule-based detection (AI model not available)...")
            result = self._detect_rule_based(image)
            log.info(f"Rule-based detection took {time.time() - start_time:.2f}s")
            return result
    
    def _detect_with_model(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """Detect injuries using AI model"""
        try:
            # Preprocess image
            input_shape = self.input_details[0]['shape']
            height, width = input_shape[1], input_shape[2]
            
            # Resize and normalize
            processed = cv2.resize(image, (width, height))
            processed = cv2.cvtColor(processed, cv2.COLOR_BGR2RGB)
            processed = processed.astype(np.float32) / 255.0
            processed = np.expand_dims(processed, axis=0)
            
            # Run inference
            self.interpreter.set_tensor(self.input_details[0]['index'], processed)
            self.interpreter.invoke()
            
            # Get output
            output = self.interpreter.get_tensor(self.output_details[0]['index'])
            predictions = output[0]
            
            # Parse results
            injuries = []
            for idx, confidence in enumerate(predictions):
                if confidence > 0.3 and idx > 0:  # Skip "no_injury" class
                    injuries.append({
                        "type": self.INJURY_CLASSES[idx],
                        "confidence": float(confidence),
                        "severity": self._estimate_severity(self.INJURY_CLASSES[idx], confidence)
                    })
            
            # Sort by confidence
            injuries.sort(key=lambda x: x['confidence'], reverse=True)
            
            log.info(f"Detected {len(injuries)} injuries using AI model")
            return injuries
            
        except Exception as e:
            log.error(f"Model inference failed: {e}")
            return self._detect_rule_based(image)
    
    def _detect_rule_based(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """
        Fallback rule-based detection using color and texture analysis
        This is a simplified approach for demonstration
        """
        try:
            injuries = []
            
            # Convert to different color spaces
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # Detect red regions (potential bleeding/wounds)
            lower_red1 = np.array([0, 50, 50])
            upper_red1 = np.array([10, 255, 255])
            lower_red2 = np.array([170, 50, 50])
            upper_red2 = np.array([180, 255, 255])
            
            mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
            mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
            red_mask = cv2.bitwise_or(mask1, mask2)
            
            red_percentage = (cv2.countNonZero(red_mask) / (image.shape[0] * image.shape[1])) * 100
            
            if red_percentage > 5:
                injuries.append({
                    "type": "bleeding",
                    "confidence": min(red_percentage / 20, 0.9),
                    "severity": "high" if red_percentage > 15 else "medium"
                })
            
            # Detect dark regions (potential bruising)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            dark_mask = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)[1]
            dark_percentage = (cv2.countNonZero(dark_mask) / (image.shape[0] * image.shape[1])) * 100
            
            if dark_percentage > 10:
                injuries.append({
                    "type": "bruise",
                    "confidence": 0.6,
                    "severity": "medium"
                })
            
            log.info(f"Detected {len(injuries)} injuries using rule-based method")
            return injuries
            
        except Exception as e:
            log.error(f"Rule-based detection failed: {e}")
            return []
    
    def _estimate_severity(self, injury_type: str, confidence: float) -> str:
        """Estimate injury severity"""
        severity_map = {
            "bleeding": "high",
            "fracture": "high",
            "burn": "high",
            "cut": "medium",
            "swelling": "medium",
            "bruise": "low"
        }
        
        base_severity = severity_map.get(injury_type, "medium")
        
        # Adjust based on confidence
        if confidence > 0.8:
            return "high"
        elif confidence < 0.5:
            return "low"
        
        return base_severity
    
    def get_injury_summary(self, injuries: List[Dict[str, Any]]) -> str:
        """Create human-readable injury summary"""
        if not injuries:
            return "No visible injuries detected"
        
        summary_parts = []
        for injury in injuries:
            injury_type = injury['type'].replace('_', ' ').title()
            confidence = injury['confidence'] * 100
            summary_parts.append(f"{injury_type} ({confidence:.0f}%)")
        
        return ", ".join(summary_parts)
