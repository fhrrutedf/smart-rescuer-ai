"""
Emergency Report Generator
Creates structured reports for EMS
"""
from typing import Dict, Any
from datetime import datetime
from pathlib import Path
import json
from utils import log
from utils.json_helpers import NumpyEncoder



class ReportGenerator:
    """Generate emergency reports"""
    
    def __init__(self, reports_dir: str = "./reports"):
        """
        Initialize report generator
        
        Args:
            reports_dir: Directory to save reports
        """
        self.reports_dir = Path(reports_dir)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        log.info(f"Report generator initialized (dir: {self.reports_dir})")
    
    def generate_ems_report(self, assessment: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate EMS-formatted report
        
        Args:
            assessment: Assessment data from DataFusionEngine
            
        Returns:
            EMS report dictionary
        """
        try:
            timestamp = assessment.get("timestamp", datetime.now().isoformat())
            vital_signs = assessment.get("vital_signs", {})
            severity = assessment.get("severity", {})
            location = assessment.get("location", {})
            injuries = assessment.get("injuries", [])
            
            # Build EMS report
            report = {
                "report_id": self._generate_report_id(),
                "timestamp": timestamp,
                "priority": self._map_severity_to_priority(severity.get("severity_level")),
                
                # Patient Status
                "patient": {
                    "conscious": assessment.get("patient_conscious", True),
                    "vital_signs": {
                        "heart_rate": vital_signs.get("heart_rate"),
                        "spo2": vital_signs.get("spo2"),
                        "temperature": vital_signs.get("body_temperature"),
                        "ecg_rhythm": vital_signs.get("rhythm")
                    }
                },
                
                # Injuries
                "injuries": {
                    "summary": assessment.get("injury_summary", "No visible injuries"),
                    "details": injuries,
                    "count": len(injuries)
                },
                
                # Severity Assessment
                "severity": {
                    "score": severity.get("total_score"),
                    "level": severity.get("severity_level"),
                    "critical_factors": severity.get("critical_factors", []),
                    "immediate_attention_required": severity.get("requires_immediate_attention", False)
                },
                
                # Location
                "location": {
                    "latitude": location.get("latitude") if location else None,
                    "longitude": location.get("longitude") if location else None,
                    "google_maps_url": self._build_maps_url(location) if location else None,
                    "gps_accuracy": location.get("fix_quality") if location else 0
                },
                
                # Recommended Actions
                "recommendations": self._generate_recommendations(assessment)
            }
            
            # Save report
            report_file = self._save_report(report)
            report["report_file"] = str(report_file)
            
            log.info(f"EMS report generated: {report['report_id']}")
            
            return report
            
        except Exception as e:
            log.error(f"Failed to generate EMS report: {e}")
            return {"error": str(e)}
    
    def generate_text_summary(self, assessment: Dict[str, Any]) -> str:
        """Generate human-readable text summary"""
        try:
            severity = assessment.get("severity", {})
            vital_signs = assessment.get("vital_signs", {})
            location = assessment.get("location", {})
            
            lines = [
                "=" * 50,
                "تقرير حالة الطوارئ - المنقذ الذكي",
                "SMART RESCUER EMERGENCY REPORT",
                "=" * 50,
                f"الوقت: {assessment.get('timestamp', 'N/A')}",
                f"مستوى الخطورة: {severity.get('severity_level', 'N/A').upper()}",
                f"الدرجة: {severity.get('total_score', 0)}/10",
                "",
                "العلامات الحيوية:",
                f"  معدل القلب: {vital_signs.get('heart_rate', 'N/A')} bpm",
                f"  الأكسجين: {vital_signs.get('spo2', 'N/A')}%",
                f"  الحرارة: {vital_signs.get('body_temperature', 'N/A')}°C",
                "",
                f"الإصابات: {assessment.get('injury_summary', 'لا توجد إصابات ظاهرة')}",
                ""
            ]
            
            if location:
                lat = location.get('latitude', 0)
                lon = location.get('longitude', 0)
                lines.extend([
                    "الموقع:",
                    f"  {lat:.6f}, {lon:.6f}",
                    f"  Google Maps: https://www.google.com/maps?q={lat},{lon}",
                    ""
                ])
            
            critical_factors = severity.get('critical_factors', [])
            if critical_factors:
                lines.append("العوامل الحرجة:")
                for factor in critical_factors:
                    lines.append(f"  ⚠️ {factor}")
                lines.append("")
            
            lines.append("=" * 50)
            
            return "\n".join(lines)
            
        except Exception as e:
            log.error(f"Failed to generate text summary: {e}")
            return "Error generating summary"
    
    def _generate_report_id(self) -> str:
        """Generate unique report ID"""
        return f"SR-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    
    def _map_severity_to_priority(self, severity_level: str) -> str:
        """Map severity level to EMS priority"""
        priority_map = {
            "critical": "P1 - IMMEDIATE",
            "severe": "P2 - URGENT",
            "moderate": "P3 - DELAYED",
            "mild": "P4 - MINOR",
            "minimal": "P5 - NON-URGENT"
        }
        return priority_map.get(severity_level, "P3 - DELAYED")
    
    def _build_maps_url(self, location: Dict[str, Any]) -> str:
        """Build Google Maps URL from location"""
        lat = location.get("latitude")
        lon = location.get("longitude")
        if lat and lon:
            return f"https://www.google.com/maps?q={lat},{lon}"
        return ""
    
    def _generate_recommendations(self, assessment: Dict[str, Any]) -> list:
        """Generate action recommendations based on assessment"""
        recommendations = []
        severity = assessment.get("severity", {})
        vital_signs = assessment.get("vital_signs", {})
        
        # Severity-based recommendations
        if severity.get("requires_immediate_attention"):
            recommendations.append("اتصل بالطوارئ 997 فوراً")
            recommendations.append("لا تحرك المصاب إلا إذا كان في خطر مباشر")
        
        # Vital signs-based recommendations
        spo2 = vital_signs.get("spo2", 100)
        if spo2 < 90:
            recommendations.append("أعط الأكسجين إن توفر")
        
        hr = vital_signs.get("heart_rate", 75)
        if hr < 50:
            recommendations.append("راقب معدل القلب البطيء")
        elif hr > 120:
            recommendations.append("حاول تهدئة المريض")
        
        # Injuries-based recommendations
        injuries = assessment.get("injuries", [])
        for injury in injuries:
            if injury['type'] == 'bleeding':
                recommendations.append("اضغط على الجرح لوقف النزيف")
            elif injury['type'] == 'fracture':
                recommendations.append("ثبّت العضو المكسور دون تحريكه")
        
        return recommendations if recommendations else ["انتظر وصول الإسعاف"]
    
    def _save_report(self, report: Dict[str, Any]) -> Path:
        """Save report to file"""
        try:
            report_id = report.get("report_id", "unknown")
            report_file = self.reports_dir / f"{report_id}.json"
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2, cls=NumpyEncoder)
            
            log.info(f"Report saved: {report_file}")
            return report_file
            
        except Exception as e:
            log.error(f"Failed to save report: {e}")
            return Path("error.json")
