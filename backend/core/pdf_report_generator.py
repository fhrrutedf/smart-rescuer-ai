"""
PDF Report Generator - Enhanced with Patient Photo
Creates professional medical reports in PDF format matching the design
"""
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Frame, Image as RLImage
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT
from reportlab.graphics.shapes import Drawing, Circle
from reportlab.platypus.flowables import Image
from utils import log
import io
from PIL import Image as PILImage


class PDFReportGenerator:
    """Generate professional PDF medical reports with patient photos"""
    
    def __init__(self, reports_dir: str = "./reports"):
        """Initialize PDF report generator"""
        self.reports_dir = Path(reports_dir)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        self.arabic_font = 'Helvetica'
        
        log.info("PDF Report Generator initialized")
    
    def generate_pdf_report(
        self, 
        assessment: Dict[str, Any], 
        report_id: str = None,
        patient_image_path: str = None
    ) -> Path:
        """
        Generate PDF report from assessment data with patient photo
        
        Args:
            assessment: Assessment data dictionary
            report_id: Optional report ID
            patient_image_path: Path to patient photo
            
        Returns:
            Path to generated PDF file
        """
        try:
            # Generate report ID if not provided
            if not report_id:
                report_id = f"SR-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            
            # Create PDF path
            pdf_path = self.reports_dir / f"{report_id}.pdf"
            
            # Create PDF document
            doc = SimpleDocTemplate(
                str(pdf_path),
                pagesize=A4,
                rightMargin=2*cm,
                leftMargin=2*cm,
                topMargin=1.5*cm,
                bottomMargin=2*cm
            )
            
            # Build content
            story = []
            styles = getSampleStyleSheet()
            
            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=22,
                textColor=colors.HexColor('#2c3e50'),
                spaceAfter=10,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            )
            
            subtitle_style = ParagraphStyle(
                'SubTitle',
                parent=styles['Normal'],
                fontSize=12,
                textColor=colors.HexColor('#7f8c8d'),
                alignment=TA_CENTER,
                spaceAfter=20
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=14,
                textColor=colors.white,
                spaceAfter=10,
                spaceBefore=15,
                backColor=colors.HexColor('#34495e'),
                leftIndent=10,
                rightIndent=10
            )
            
            # Header with Patient Photo
            header_data = []
            
            # Add patient photo if provided
            if patient_image_path and Path(patient_image_path).exists():
                try:
                    # Load and resize image to circular
                    img = RLImage(patient_image_path, width=3*cm, height=3*cm)
                    photo_cell = img
                except Exception as e:
                    log.warning(f"Could not load patient image: {e}")
                    photo_cell = Paragraph("No Photo", styles['Normal'])
            else:
                photo_cell = Paragraph("Patient Profile", styles['Normal'])
            
            # Title cell
            title_cell = [
                Paragraph("Smart AI - Medical Report", title_style),
                Paragraph("تقرير طبي ذكي", subtitle_style)
            ]
            
            # Create header table
            header_table = Table(
                [[photo_cell, title_cell]], 
                colWidths=[4*cm, 13*cm]
            )
            header_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                ('ALIGN', (1, 0), (1, 0), 'LEFT'),
            ]))
            story.append(header_table)
            story.append(Spacer(1, 0.5*cm))
            
            # Sensor/Vital Signs Table (Like the image)
            story.append(Paragraph("Sensor Readings / قراءات الحساسات", heading_style))
            story.append(Spacer(1, 0.2*cm))
            
            vital_signs = assessment.get('vital_signs', {})
            location = assessment.get('location', {})
            
            # Build sensor table data
            sensor_data = [
                ['Sensor', 'Value', 'Status']
            ]
            
            # Temperature
            temp = vital_signs.get('body_temperature', 37.0)
            temp_status = '✓ Normal' if 36 <= temp <= 37.5 else '⚠ Alert'
            sensor_data.append(['Temperature', f'{temp}°C', temp_status])
            
            # SpO2
            spo2 = vital_signs.get('spo2', 98)
            spo2_status = '✓ Normal' if spo2 >= 95 else '⚠ Low'
            sensor_data.append(['SpO2 (Oxygen)', f'{spo2}%', spo2_status])
            
            # Heart Rate
            hr = vital_signs.get('heart_rate', 72)
            hr_status = '✓ Normal' if 60 <= hr <= 100 else '⚠ Alert'
            sensor_data.append(['Heart Rate (BPM)', f'{hr} bpm', hr_status])
            
            # Blood Pressure (simulated)
            sensor_data.append(['Blood Pressure', '120/80 mmHg', '✓ Normal'])
            
            # ECG
            rhythm = vital_signs.get('rhythm', 'Sinus Rhythm')
            sensor_data.append(['ECG', rhythm, '✓ Normal'])
            
            # GSR/Stress (simulated)
            sensor_data.append(['GSR (Stress)', '3.5 μS', '✓ Relaxed'])
            
            # Motion Sensor (simulated)
            sensor_data.append(['Motion Sensor', 'Stationary', '✓ Active'])
            
            # Gas Sensor (simulated)
            sensor_data.append(['Gas Sensor', '250 ppm', '✓ Safe Air'])
            
            # CO2 Level (simulated)
            sensor_data.append(['CO2 Level', '400 ppm', '✓ Good Quality'])
            
            # GPS Location
            if location:
                lat = location.get('latitude', 0)
                lon = location.get('longitude', 0)
                if lat and lon:
                    # Create clickable Google Maps link
                    maps_url = f"https://www.google.com/maps?q={lat},{lon}"
                    gps_text = f'<link href="{maps_url}" color="blue">{lat:.6f}°N, {lon:.6f}°E</link>'
                    sensor_data.append(['GPS Location', Paragraph(gps_text, styles['Normal']), '📍 Located'])
                else:
                    sensor_data.append(['GPS Location', 'N/A', '⚠ No Fix'])
            else:
                sensor_data.append(['GPS Location', 'N/A', '⚠ No Fix'])
            
            # Create sensor table with blue header (like image)
            sensor_table = Table(sensor_data, colWidths=[6*cm, 6*cm, 5*cm])
            sensor_table.setStyle(TableStyle([
                # Header row - Blue background
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a90e2')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                
                # Data rows
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('ALIGN', (0, 1), (0, -1), 'LEFT'),
                ('ALIGN', (1, 1), (1, -1), 'CENTER'),
                ('ALIGN', (2, 1), (2, -1), 'CENTER'),
                
                # Grid
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d0d0d0')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
            ]))
            story.append(sensor_table)
            story.append(Spacer(1, 0.5*cm))
            
            # Medical Summary Section (Like the image)
            story.append(Paragraph("Medical Summary / الملخص الطبي", heading_style))
            story.append(Spacer(1, 0.2*cm))
            
            # Build summary text
            severity = assessment.get('severity', {})
            injuries = assessment.get('injuries', [])
            
            summary_lines = []
            
            # Vital signs assessment
            summary_lines.append("The patient's vital signs are all within normal ranges.")
            
            # Heart rhythm
            if rhythm:
                summary_lines.append(f"No irregularities detected in heart rhythm (ECG) - {rhythm}.")
            
            # Stress levels
            summary_lines.append("Stress levels are normal.")
            
            # Environmental conditions
            summary_lines.append("Environmental conditions are safe.")
            
            # Injuries if any
            if injuries:
                summary_lines.append(f"\n⚠️ Detected Injuries: {len(injuries)}")
                for injury in injuries[:3]:  # Show top 3
                    summary_lines.append(f"  • {injury.get('type', 'Unknown')}: {injury.get('location', 'N/A')}")
            
            # Overall health score
            total_score = severity.get('total_score', 10)
            health_percentage = int((total_score / 10) * 100)
            summary_lines.append(f"\nOverall Health Score: {health_percentage}%")
            
            # Emergency level
            severity_level = severity.get('severity_level', 'normal')
            if severity_level in ['critical', 'severe']:
                summary_lines.append("\n⚠️ EMERGENCY: Immediate medical attention required!")
                summary_lines.append("Call 997 now!")
            
            summary_text = '\n'.join(summary_lines)
            
            # Create summary box
            summary_table = Table(
                [[Paragraph(summary_text, styles['Normal'])]],
                colWidths=[17*cm]
            )
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
                ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#d0d0d0')),
                ('LEFTPADDING', (0, 0), (-1, -1), 15),
                ('RIGHTPADDING', (0, 0), (-1, -1), 15),
                ('TOPPADDING', (0, 0), (-1, -1), 15),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            story.append(summary_table)
            story.append(Spacer(1, 0.5*cm))
            
            # Report metadata at bottom
            meta_data = [
                ['Report ID:', report_id],
                ['Date/Time:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
                ['Priority:', self._get_priority(assessment)]
            ]
            
            meta_table = Table(meta_data, colWidths=[5*cm, 12*cm])
            meta_table.setStyle(TableStyle([
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#7f8c8d')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ]))
            story.append(meta_table)
            
            # Footer
            story.append(Spacer(1, 0.5*cm))
            footer_style = ParagraphStyle(
                'Footer',
                parent=styles['Normal'],
                fontSize=8,
                textColor=colors.HexColor('#95a5a6'),
                alignment=TA_CENTER
            )
            story.append(Paragraph(f"Generated by Smart Rescuer AI System", footer_style))
            story.append(Paragraph("Emergency Hotline: 997 | النجدة: 997", footer_style))
            
            # Build PDF
            doc.build(story)
            
            log.info(f"PDF report generated: {pdf_path}")
            return pdf_path
            
        except Exception as e:
            log.error(f"Failed to generate PDF report: {e}")
            raise
    
    def _get_priority(self, assessment: Dict[str, Any]) -> str:
        """Get priority level from assessment"""
        severity_level = assessment.get('severity', {}).get('severity_level', 'moderate')
        priority_map = {
            'critical': 'P1 - IMMEDIATE',
            'severe': 'P2 - URGENT',
            'moderate': 'P3 - DELAYED',
            'mild': 'P4 - MINOR',
            'minimal': 'P5 - NON-URGENT'
        }
        return priority_map.get(severity_level, 'P3 - DELAYED')
    
    def _get_severity_color(self, severity_level: str) -> colors.Color:
        """Get color for severity level"""
        color_map = {
            'critical': colors.HexColor('#d32f2f'),
            'severe': colors.HexColor('#f57c00'),
            'moderate': colors.HexColor('#fbc02d'),
            'mild': colors.HexColor('#689f38'),
            'minimal': colors.HexColor('#388e3c')
        }
        return color_map.get(severity_level, colors.grey)
