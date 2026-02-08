"""
AI-Powered Medical Analysis Engine
محرك التحليل الطبي بالذكاء الاصطناعي
"""
from typing import Dict, Any, List, Optional
from datetime import datetime


class MedicalAIAnalyzer:
    """محلل طبي ذكي باستخدام AI"""
    
    def analyze_complete_case(
        self,
        vision_data: Dict[str, Any],
        sensor_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """تحليل كامل للحالة باستخدام AI"""
        
        injuries = vision_data.get('injuries', [])
        
        # تحليل الإصابات
        injury_analysis = self._analyze_injuries(injuries, sensor_data)
        
        # تحليل العلامات الحيوية
        vital_analysis = self._analyze_vitals(sensor_data)
        
        # الربط الذكي
        correlation = self._correlate_data(injury_analysis, vital_analysis)
        
        # التشخيص
        diagnosis = self._generate_diagnosis(injury_analysis, vital_analysis, correlation)
        
        # الأولويات
        priorities = self._determine_priorities(diagnosis)
        
        # خطة العلاج
        treatment_plan = self._generate_treatment_plan(diagnosis, priorities)
        
        return {
            'diagnosis': diagnosis,
            'injury_analysis': injury_analysis,
            'vital_analysis': vital_analysis,
            'correlation': correlation,
            'priorities': priorities,
            'treatment_plan': treatment_plan,
            'timestamp': datetime.now().isoformat()
        }
    
    def _analyze_injuries(self, injuries: List[Dict], sensor_data: Dict) -> Dict[str, Any]:
        """تحليل ذكي للإصابات"""
        if not injuries:
            return {'total': 0, 'severity': 'none', 'concerns': []}
        
        concerns = []
        severity_score = 0
        
        for injury in injuries:
            injury_type = injury.get('type', '')
            
            if injury_type == 'bleeding':
                severity_score += 8
                pulse = sensor_data.get('pulse', {}).get('value', 75)
                if pulse > 100:
                    concerns.append("نزيف + تسارع نبض = فقدان دم نشط")
            
            elif injury_type == 'burn':
                severity_score += 7
                temp = sensor_data.get('temperature', {}).get('value', 37)
                if temp > 38:
                    concerns.append("حروق + حمى = احتمال عدوى")
            
            elif injury_type == 'fracture':
                severity_score += 6
                concerns.append("كسر - عدم تحريك المصاب")
        
        avg_severity = severity_score / len(injuries) if injuries else 0
        
        return {
            'total': len(injuries),
            'severity': 'critical' if avg_severity > 7 else 'high',
            'concerns': concerns
        }
    
    def _analyze_vitals(self, sensor_data: Dict) -> Dict[str, Any]:
        """تحليل العلامات الحيوية"""
        concerns = []
        severity = 0
        
        # SpO2
        spo2 = sensor_data.get('spo2', {}).get('value', 98)
        if spo2 < 90:
            concerns.append(f"نقص أكسجين حاد ({spo2}%) - تهديد للحياة")
            severity += 5
        
        # Pulse
        pulse = sensor_data.get('pulse', {}).get('value', 75)
        if pulse > 120:
            concerns.append(f"تسارع نبض ({pulse} bpm) - صدمة محتملة")
            severity += 3
        
        # Temperature
        temp = sensor_data.get('temperature', {}).get('value', 37)
        if temp > 38.5:
            concerns.append(f"حمى ({temp}°C)")
            severity += 2
        
        return {
            'concerns': concerns,
            'severity_score': severity,
            'status': 'critical' if severity >= 5 else 'stable'
        }
    
    def _correlate_data(self, injury_analysis: Dict, vital_analysis: Dict) -> Dict:
        """الربط الذكي بين البيانات"""
        findings = []
        
        if injury_analysis.get('severity') == 'critical' and vital_analysis.get('status') == 'critical':
            findings.append({
                'finding': 'إصابات حرجة + علامات حيوية حرجة',
                'interpretation': 'حالة طوارئ شديدة - تدخل فوري',
                'severity': 'critical'
            })
        
        return {'findings': findings}
    
    def _generate_diagnosis(self, injury_analysis: Dict, vital_analysis: Dict, correlation: Dict) -> Dict:
        """توليد التشخيص"""
        diagnoses = []
        
        if injury_analysis.get('total', 0) > 0:
            diagnoses.append("إصابات متعددة تحتاج تقييم طبي")
        
        if vital_analysis.get('status') == 'critical':
            diagnoses.append("علامات حيوية غير مستقرة")
        
        return {
            'primary': diagnoses,
            'severity': 'critical' if vital_analysis.get('severity_score', 0) >= 5 else 'moderate'
        }
    
    def _determine_priorities(self, diagnosis: Dict) -> List[Dict]:
        """تحديد الأولويات"""
        return [
            {'priority': 1, 'action': 'تأمين مجرى التنفس', 'critical': True},
            {'priority': 2, 'action': 'إيقاف النزيف', 'critical': True},
            {'priority': 3, 'action': 'تثبيت الكسور', 'critical': False}
        ]
    
    def _generate_treatment_plan(self, diagnosis: Dict, priorities: List) -> Dict:
        """خطة العلاج"""
        return {
            'immediate_actions': [p['action'] for p in priorities if p['critical']],
            'monitoring': ['مراقبة العلامات الحيوية كل 5 دقائق'],
            'ems_transport': True
        }


medical_ai = MedicalAIAnalyzer()
