"""
Severity Scoring using Data Fusion
Combines visual and vital signs data to calculate severity score
"""
from typing import Dict, Any, List, Optional
import numpy as np
from utils import log


class SeverityScorer:
    """Calculate severity score by fusing multiple data sources"""
    
    # Severity levels
    SEVERITY_LEVELS = {
        "critical": (8, 10),
        "severe": (6, 7.9),
        "moderate": (4, 5.9),
        "mild": (2, 3.9),
        "minimal": (0, 1.9)
    }
    
    def __init__(self):
        """Initialize severity scorer"""
        log.info("Severity scorer initialized")
    
    def calculate_score(
        self,
        injuries: List[Dict[str, Any]],
        vital_signs: Dict[str, Any],
        patient_conscious: bool = True
    ) -> Dict[str, Any]:
        """
        Calculate overall severity score
        
        Args:
            injuries: List of detected injuries
            vital_signs: Dictionary with ECG, SpO2, temp data
            patient_conscious: Whether patient is conscious
            
        Returns:
            Dictionary with severity score and breakdown
        """
        try:
            # Calculate individual component scores
            injury_score = self._score_injuries(injuries)
            vital_score = self._score_vital_signs(vital_signs)
            consciousness_score = 0 if patient_conscious else 3
            
            # Weighted combination
            weights = {
                "injury": 0.4,
                "vitals": 0.5,
                "consciousness": 0.1
            }
            
            total_score = (
                injury_score * weights["injury"] +
                vital_score * weights["vitals"] +
                consciousness_score * weights["consciousness"]
            )
            
            # Ensure score is in range [0, 10]
            total_score = np.clip(total_score, 0, 10)
            
            # Determine severity level
            severity_level = self._get_severity_level(total_score)
            
            # Identify critical factors
            critical_factors = self._identify_critical_factors(
                injuries, vital_signs, patient_conscious
            )
            
            result = {
                "total_score": float(round(total_score, 2)),
                "severity_level": severity_level,
                "breakdown": {
                    "injury_score": float(round(injury_score, 2)),
                    "vital_signs_score": float(round(vital_score, 2)),
                    "consciousness_score": int(consciousness_score)
                },
                "critical_factors": critical_factors,
                "requires_immediate_attention": bool(total_score >= 6)
            }
            
            log.info(f"Calculated severity score: {total_score:.2f} ({severity_level})")
            
            return result
            
        except Exception as e:
            log.error(f"Failed to calculate severity score: {e}")
            return {
                "total_score": 5.0,
                "severity_level": "moderate",
                "error": str(e)
            }
    
    def _score_injuries(self, injuries: List[Dict[str, Any]]) -> float:
        """
        Score injuries based on type and severity
        
        Returns:
            Score from 0-10
        """
        if not injuries:
            return 0.0
        
        # Injury type severity weights
        injury_weights = {
            "bleeding": 8,
            "fracture": 7,
            "burn": 7,
            "cut": 5,
            "swelling": 3,
            "bruise": 2
        }
        
        max_score = 0
        for injury in injuries:
            injury_type = injury.get("type", "unknown")
            confidence = injury.get("confidence", 0)
            base_weight = injury_weights.get(injury_type, 5)
            
            # Adjust by confidence
            score = base_weight * confidence
            max_score = max(max_score, score)
        
        return min(max_score, 10)
    
    def _score_vital_signs(self, vital_signs: Dict[str, Any]) -> float:
        """
        Score vital signs abnormality
        
        Returns:
            Score from 0-10
        """
        scores = []
        
        # Heart rate scoring
        if "heart_rate" in vital_signs:
            hr = vital_signs["heart_rate"]
            hr_score = self._score_heart_rate(hr)
            scores.append(hr_score)
        
        # SpO2 scoring
        if "spo2" in vital_signs:
            spo2 = vital_signs["spo2"]
            spo2_score = self._score_spo2(spo2)
            scores.append(spo2_score)
        
        # Temperature scoring
        if "body_temperature" in vital_signs:
            temp = vital_signs["body_temperature"]
            temp_score = self._score_temperature(temp)
            scores.append(temp_score)
        
        # ECG rhythm scoring
        if "rhythm" in vital_signs:
            rhythm = vital_signs["rhythm"]
            rhythm_score = self._score_rhythm(rhythm)
            scores.append(rhythm_score)
        
        # Return maximum score (worst case)
        return max(scores) if scores else 0.0
    
    def _score_heart_rate(self, hr: int) -> float:
        """Score heart rate (0-10, higher is worse)"""
        if 60 <= hr <= 100:
            return 0  # Normal
        elif 50 <= hr < 60 or 100 < hr <= 120:
            return 3  # Mild abnormality
        elif 40 <= hr < 50 or 120 < hr <= 150:
            return 6  # Moderate abnormality
        else:
            return 9  # Severe abnormality
    
    def _score_spo2(self, spo2: float) -> float:
        """Score SpO2 (0-10, higher is worse)"""
        if spo2 >= 95:
            return 0  # Normal
        elif 90 <= spo2 < 95:
            return 4  # Mild hypoxemia
        elif 85 <= spo2 < 90:
            return 7  # Moderate hypoxemia
        else:
            return 10  # Severe hypoxemia
    
    def _score_temperature(self, temp: float) -> float:
        """Score body temperature (0-10, higher is worse)"""
        if 36.5 <= temp <= 37.5:
            return 0  # Normal
        elif 37.5 < temp <= 38.5 or 35.5 <= temp < 36.5:
            return 2  # Mild abnormality
        elif 38.5 < temp <= 39.5 or 34.5 <= temp < 35.5:
            return 5  # Moderate abnormality
        else:
            return 8  # Severe abnormality
    
    def _score_rhythm(self, rhythm: str) -> float:
        """Score ECG rhythm (0-10, higher is worse)"""
        rhythm_scores = {
            "normal": 0,
            "sinus_tachycardia": 2,
            "sinus_bradycardia": 2,
            "irregular": 4,
            "atrial_fibrillation": 6,
            "ventricular_tachycardia": 9,
            "ventricular_fibrillation": 10
        }
        return rhythm_scores.get(rhythm, 3)
    
    def _get_severity_level(self, score: float) -> str:
        """Convert numeric score to severity level"""
        for level, (min_score, max_score) in self.SEVERITY_LEVELS.items():
            if min_score <= score <= max_score:
                return level
        return "moderate"
    
    def _identify_critical_factors(
        self,
        injuries: List[Dict[str, Any]],
        vital_signs: Dict[str, Any],
        conscious: bool
    ) -> List[str]:
        """Identify critical factors requiring immediate attention"""
        factors = []
        
        # Check injuries
        for injury in injuries:
            if injury.get("severity") == "high":
                factors.append(f"Severe {injury['type']}")
        
        # Check vital signs
        hr = vital_signs.get("heart_rate", 75)
        if hr < 50 or hr > 120:
            factors.append(f"Abnormal heart rate: {hr} bpm")
        
        spo2 = vital_signs.get("spo2", 98)
        if spo2 < 90:
            factors.append(f"Low oxygen: {spo2}%")
        
        temp = vital_signs.get("body_temperature", 37)
        if temp > 39 or temp < 35:
            factors.append(f"Abnormal temperature: {temp}°C")
        
        if not conscious:
            factors.append("Patient unconscious")
        
        return factors
