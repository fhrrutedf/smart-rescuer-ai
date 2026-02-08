"""
Advanced Sensor Suite - All 9 Sensors
حساسات متقدمة - جميع الـ 9 حساسات
"""
from typing import Dict, Any, Optional
from datetime import datetime
import random
from utils import log


class AdvancedSensorSuite:
    """مجموعة الحساسات المتقدمة الكاملة"""
    
    def __init__(self):
        """Initialize all 9 sensors"""
        self.sensors_enabled = True
        self.simulation_mode = True  # سيتم تبديله عند توصيل الجهاز
        
        log.info("Advanced Sensor Suite initialized with 9 sensors")
    
    def read_all_sensors(self) -> Dict[str, Any]:
        """قراءة جميع الحساسات دفعة واحدة"""
        readings = {}
        
        readings['temperature'] = self._read_temperature()
        readings['spo2'] = self._read_spo2()
        readings['pulse'] = self._read_pulse()
        readings['motion'] = self._read_motion()
        readings['ecg'] = self._read_ecg()
        readings['gsr'] = self._read_gsr()
        readings['blood_pressure'] = self._read_blood_pressure()
        readings['gas'] = self._read_gas()
        readings['co2'] = self._read_co2()
        readings['gps'] = self._read_gps()
        
        readings['timestamp'] = datetime.now().isoformat()
        readings['simulation_mode'] = self.simulation_mode
        
        return readings
    
    def _read_temperature(self) -> Dict[str, Any]:
        """قراءة درجة الحرارة"""
        if self.simulation_mode:
            value = round(random.uniform(36.0, 38.5), 1)
            status = 'normal' if 36.1 <= value <= 37.5 else ('high' if value > 37.5 else 'low')
        else:
            value = 0
            status = 'unknown'
        
        return {
            'value': value,
            'unit': '°C',
            'status': status,
            'normal_range': '36.1-37.5'
        }
    
    def _read_spo2(self) -> Dict[str, Any]:
        """قراءة تشبع الأكسجين"""
        if self.simulation_mode:
            value = round(random.uniform(92.0, 100.0), 1)
            status = 'normal' if value >= 95 else ('low' if value >= 90 else 'critical')
        else:
            value = 0
            status = 'unknown'
        
        return {
            'value': value,
            'unit': '%',
            'status': status,
            'normal_range': '95-100'
        }
    
    def _read_pulse(self) -> Dict[str, Any]:
        """قراءة معدل النبض"""
        if self.simulation_mode:
            value = random.randint(55, 110)
            status = 'normal' if 60 <= value <= 100 else ('high' if value > 100 else 'low')
        else:
            value = 0
            status = 'unknown'
        
        return {
            'value': value,
            'unit': 'bpm',
            'status': status,
            'normal_range': '60-100'
        }
    
    def _read_motion(self) -> Dict[str, Any]:
        """قراءة حساس الحركة"""
        if self.simulation_mode:
            x = round(random.uniform(-1.0, 1.0), 2)
            y = round(random.uniform(-1.0, 1.0), 2)
            z = round(random.uniform(0.9, 1.1), 2)
            magnitude = round((x**2 + y**2 + z**2)**0.5, 2)
            status = 'still' if magnitude < 1.2 else ('moving' if magnitude < 2.0 else 'active')
        else:
            x = y = z = magnitude = 0
            status = 'unknown'
        
        return {
            'x': x,
            'y': y,
            'z': z,
            'magnitude': magnitude,
            'unit': 'g',
            'status': status
        }
    
    def _read_ecg(self) -> Dict[str, Any]:
        """قراءة تخطيط القلب"""
        if self.simulation_mode:
            hr = random.randint(60, 100)
            qrs_duration = round(random.uniform(0.06, 0.10), 3)
            rhythm = 'sinus' if 60 <= hr <= 100 else 'abnormal'
            status = 'normal' if rhythm == 'sinus' else 'abnormal'
        else:
            hr = qrs_duration = 0
            rhythm = 'unknown'
            status = 'unknown'
        
        return {
            'heart_rate': hr,
            'qrs_duration': qrs_duration,
            'rhythm': rhythm,
            'unit': 'mV',
            'status': status
        }
    
    def _read_gsr(self) -> Dict[str, Any]:
        """قراءة الاستجابة الجلدية"""
        if self.simulation_mode:
            value = round(random.uniform(1.0, 10.0), 2)
            status = 'calm' if value < 4 else ('moderate' if value < 7 else 'stressed')
        else:
            value = 0
            status = 'unknown'
        
        return {
            'value': value,
            'unit': 'µS',
            'status': status
        }
    
    def _read_blood_pressure(self) -> Dict[str, Any]:
        """قراءة ضغط الدم"""
        if self.simulation_mode:
            systolic = random.randint(100, 140)
            diastolic = random.randint(60, 90)
            
            if systolic < 120 and diastolic < 80:
                status = 'normal'
            elif systolic < 140 and diastolic < 90:
                status = 'elevated'
            else:
                status = 'high'
        else:
            systolic = diastolic = 0
            status = 'unknown'
        
        return {
            'systolic': systolic,
            'diastolic': diastolic,
            'value': f"{systolic}/{diastolic}",
            'unit': 'mmHg',
            'status': status
        }
    
    def _read_gas(self) -> Dict[str, Any]:
        """قراءة حساس الغاز"""
        if self.simulation_mode:
            value = round(random.uniform(0, 50), 1)
            status = 'safe' if value < 20 else ('warning' if value < 40 else 'danger')
        else:
            value = 0
            status = 'unknown'
        
        return {
            'value': value,
            'unit': 'ppm',
            'status': status
        }
    
    def _read_co2(self) -> Dict[str, Any]:
        """قراءة ثاني أكسيد الكربون"""
        if self.simulation_mode:
            value = random.randint(350, 1200)
            status = 'good' if value < 800 else ('acceptable' if value < 1000 else 'poor')
        else:
            value = 0
            status = 'unknown'
        
        return {
            'value': value,
            'unit': 'ppm',
            'status': status
        }
    
    def _read_gps(self) -> Dict[str, Any]:
        """قراءة تحديد الموقع"""
        if self.simulation_mode:
            latitude = round(33.5138 + random.uniform(-0.01, 0.01), 6)
            longitude = round(36.2765 + random.uniform(-0.01, 0.01), 6)
            accuracy = round(random.uniform(5, 20), 1)
            status = 'acquired'
        else:
            latitude = longitude = accuracy = 0
            status = 'unknown'
        
        return {
            'latitude': latitude,
            'longitude': longitude,
            'accuracy': accuracy,
            'unit': 'degrees',
            'status': status,
            'maps_link': f"https://www.google.com/maps?q={latitude},{longitude}"
        }
    
    def get_health_summary(self, readings: Dict[str, Any]) -> Dict[str, Any]:
        """تحليل شامل للحالة الصحية"""
        
        warnings = []
        critical = []
        
        # Temperature
        if readings['temperature']['status'] != 'normal':
            msg = f"حرارة {readings['temperature']['value']}°C"
            if readings['temperature']['value'] > 39:
                critical.append(msg)
            else:
                warnings.append(msg)
        
        # SpO2
        if readings['spo2']['status'] != 'normal':
            msg = f"أكسجين {readings['spo2']['value']}%"
            if readings['spo2']['status'] == 'critical':
                critical.append(msg)
            else:
                warnings.append(msg)
        
        # Pulse
        if readings['pulse']['status'] != 'normal':
            msg = f"نبض {readings['pulse']['value']} bpm"
            if readings['pulse']['value'] > 120 or readings['pulse']['value'] < 50:
                critical.append(msg)
            else:
                warnings.append(msg)
        
        # Blood Pressure
        if readings['blood_pressure']['status'] == 'high':
            warnings.append(f"ضغط {readings['blood_pressure']['value']}")
        
        # GSR
        if readings['gsr']['status'] == 'stressed':
            warnings.append(f"توتر عالي")
        
        # Gas
        if readings['gas']['status'] != 'safe':
            if readings['gas']['status'] == 'danger':
                critical.append(f"خطر غاز")
            else:
                warnings.append(f"تحذير غاز")
        
        # Overall status
        if len(critical) > 0:
            overall_status = 'critical'
            severity = 'high'
        elif len(warnings) > 2:
            overall_status = 'concerning'
            severity = 'medium'
        elif len(warnings) > 0:
            overall_status = 'attention'
            severity = 'low'
        else:
            overall_status = 'stable'
            severity = 'minimal'
        
        return {
            'overall_status': overall_status,
            'severity': severity,
            'critical_alerts': critical,
            'warnings': warnings,
            'total_issues': len(critical) + len(warnings),
            'gps_location': readings['gps']['maps_link']
        }


# Global instance
advanced_sensors = AdvancedSensorSuite()
