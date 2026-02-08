"""
FastAPI application - Main entry point
"""
from typing import Optional
import time
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil

import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from api.models import (
    EmergencyAssessmentRequest,
    EmergencyAssessmentResponse,
    ChatMessage,
    ChatResponse,
    SystemStatus
)
from core import DataFusionEngine, ReportGenerator, EmergencyDispatcher
from core.pdf_report_generator import PDFReportGenerator
from ai_engine import MedicalChatbot
from utils import log, config
from utils.json_helpers import convert_numpy_types


# Initialize FastAPI app
app = FastAPI(
    title="Smart Rescuer API",
    description="Emergency medical response system with offline AI",
    version=config.APP_VERSION
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
data_fusion = DataFusionEngine()
report_generator = ReportGenerator()
pdf_generator = PDFReportGenerator()
dispatcher = EmergencyDispatcher()
chatbot = MedicalChatbot()

# Upload directory
UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "Smart Rescuer API",
        "version": config.APP_VERSION,
        "status": "running",
        "endpoints": {
            "emergency": "/api/emergency/assess",
            "chat": "/api/chat",
            "status": "/api/status",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for Docker"""
    try:
        # Simple check if AI engine is loaded (optional, keep it fast)
        ai_status = "active" if config.ENABLE_AI else "disabled"
        return {
            "status": "healthy",
            "ai_engine": ai_status,
            "version": config.APP_VERSION
        }
    except Exception as e:
        log.error(f"Health check failed: {e}")
        return JSONResponse(status_code=500, content={"status": "unhealthy", "error": str(e)})



@app.get("/api/status", response_model=SystemStatus)
async def get_status():
    """Get system status"""
    try:
        sensor_status = data_fusion.get_sensor_status()
        
        return SystemStatus(
            sensors=sensor_status,
            version=config.APP_VERSION,
            debug_mode=config.DEBUG
        )
    except Exception as e:
        log.error(f"Failed to get status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/emergency/assess")
async def assess_emergency(
    patient_conscious: bool = Form(True),
    image: Optional[UploadFile] = File(None)
):
    """
    Perform emergency assessment
    
    - **patient_conscious**: Whether patient is conscious
    - **image**: Optional image file of injuries
    """
    try:
        log.info("Emergency assessment requested")
        
        # Handle image upload
        image_path = None
        if image:
            image_path = UPLOAD_DIR / f"injury_{int(time.time())}.jpg"
            with open(image_path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
            log.info(f"Image uploaded: {image_path}")
        
        # Perform assessment
        assessment = data_fusion.perform_emergency_assessment(
            image_path=str(image_path) if image_path else None,
            patient_conscious=patient_conscious
        )
        
        # Generate report
        report = report_generator.generate_ems_report(assessment)
        
        # Dispatch to EMS if critical
        if assessment.get("requires_ems"):
            dispatch_result = dispatcher.dispatch_report(report)
            log.info(f"EMS dispatch result: {dispatch_result['status']}")
        
        # Convert numpy types to native Python types
        assessment = convert_numpy_types(assessment)
        report = convert_numpy_types(report)
        
        # Return assessment
        return JSONResponse(content={
            "assessment": assessment,
            "report": report,
            "text_summary": report_generator.generate_text_summary(assessment),
            "patient_image_path": str(image_path) if image_path else None
        })
        
    except Exception as e:
        log.error(f"Emergency assessment failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """
    Chat with medical AI assistant
    
    - **message**: User's message/symptoms
    - **reset_history**: Reset conversation history
    """
    try:
        response = chatbot.chat(
            user_message=message.message,
            reset_history=message.reset_history
        )
        
        return ChatResponse(**response)
        
    except Exception as e:
        log.error(f"Chat failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/sensors/calibrate")
async def calibrate_sensors():
    """Calibrate all sensors"""
    try:
        results = data_fusion.calibrate_all_sensors()
        return {"calibration_results": results}
    except Exception as e:
        log.error(f"Calibration failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/sensors/vitals")
async def get_vital_signs():
    """Get current vital signs reading"""
    try:
        vital_signs = data_fusion._collect_vital_signs()
        return {"vital_signs": vital_signs}
    except Exception as e:
        log.error(f"Failed to read vital signs: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/live/stream")
async def live_stream_vitals():
    """
    Live stream endpoint - Real-time vital signs with instant analysis
    Returns current sensor readings + instant health assessment
    """
    try:
        from ai_engine.severity_scorer import SeverityScorer
        
        # Collect real-time vital signs
        vital_signs = data_fusion._collect_vital_signs()
        
        # Get GPS location
        location = data_fusion.gps_module.read()
        
        # Calculate instant severity score
        scorer = SeverityScorer()
        severity = scorer.calculate_score(
            vital_signs=vital_signs,
            injuries=[],
            patient_conscious=True
        )
        
        # Instant analysis
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "vital_signs": vital_signs,
            "location": location,
            "severity": severity,
            "instant_alerts": []
        }
        
        # Check for critical conditions
        if vital_signs.get('heart_rate'):
            hr = vital_signs['heart_rate']
            if hr > 120:
                analysis['instant_alerts'].append({
                    "type": "warning",
                    "message": "High heart rate detected",
                    "value": hr
                })
            elif hr < 50:
                analysis['instant_alerts'].append({
                    "type": "critical",
                    "message": "Low heart rate detected",
                    "value": hr
                })
        
        if vital_signs.get('spo2'):
            spo2 = vital_signs['spo2']
            if spo2 < 90:
                analysis['instant_alerts'].append({
                    "type": "critical",
                    "message": "Critical oxygen level",
                    "value": spo2
                })
        
        if vital_signs.get('body_temperature'):
            temp = vital_signs['body_temperature']
            if temp > 38.5:
                analysis['instant_alerts'].append({
                    "type": "warning",
                    "message": "High temperature detected",
                    "value": temp
                })
        
        return analysis
        
    except Exception as e:
        log.error(f"Live stream failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/location")
async def get_location():
    """Get current GPS location"""
    try:
        location = data_fusion.gps_module.read()
        if location:
            location["maps_url"] = data_fusion.gps_module.get_google_maps_url()
        return {"location": location}
    except Exception as e:
        log.error(f"Failed to read location: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/sensors/advanced")
async def read_advanced_sensors():
    """قراءة جميع الحساسات المتقدمة (9 حساسات)"""
    try:
        from sensors.advanced_sensors import advanced_sensors
        
        # قراءة الحساسات
        readings = advanced_sensors.read_all_sensors()
        
        # تحليل الحالة
        health_summary = advanced_sensors.get_health_summary(readings)
        
        return {
            "success": True,
            "sensors": readings,
            "health_summary": health_summary,
            "timestamp": readings['timestamp']
        }
    except Exception as e:
        log.error(f"Failed to read advanced sensors: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/first-aid/instructions")
async def get_first_aid_instructions(
    injuries: Optional[list] = None,
    vital_signs: Optional[dict] = None
):
    """الحصول على إرشادات الإسعافات الأولية"""
    try:
        from core.first_aid import first_aid
        
        instructions = first_aid.get_instructions(
            condition="emergency",
            injuries=injuries,
            vital_signs=vital_signs
        )
        
        return {
            "success": True,
            "first_aid": instructions
        }
    except Exception as e:
        log.error(f"Failed to get first aid instructions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/emergency/complete-assessment")
async def complete_emergency_assessment(
    request: EmergencyAssessmentRequest,
    image: UploadFile = File(None)
):
    """تقييم طوارئ متكامل: رؤية حاسوبية + حساسات + AI تحليل + إرشادات"""
    try:
        from sensors.advanced_sensors import advanced_sensors
        from core.first_aid import first_aid
        from ai_engine.medical_analyzer import medical_ai
        
        # 1. Computer Vision Analysis
        if image:
            temp_file = Path(config.UPLOAD_DIR) / f"temp_{time.time()}.jpg"
            with open(temp_file, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
            
            assessment = data_fusion.assess_emergency(
                patient_conscious=request.patient_conscious,
                image_path=str(temp_file)
            )
            temp_file.unlink(missing_ok=True)
        else:
            assessment = data_fusion.assess_emergency(
                patient_conscious=request.patient_conscious
            )
        
        # 2. Read All Sensors
        sensor_readings = advanced_sensors.read_all_sensors()
        health_summary = advanced_sensors.get_health_summary(sensor_readings)
        
        # 3. AI Medical Analysis (الجديد - تحليل ذكي مو ردود ثابتة)
        ai_analysis = medical_ai.analyze_complete_case(
            vision_data={'injuries': assessment.get('detected_injuries', [])},
            sensor_data=sensor_readings
        )
        
        # 4. Get First Aid Instructions
        instructions = first_aid.get_instructions(
            condition="emergency",
            injuries=assessment.get('detected_injuries', []),
            vital_signs=sensor_readings
        )
        
        # 5. Generate Complete Report
        complete_report = {
            "vision_analysis": {
                "injuries": assessment.get('detected_injuries', []),
                "severity": assessment.get('severity_assessment', {})
            },
            "sensor_readings": sensor_readings,
            "health_summary": health_summary,
            "ai_medical_analysis": ai_analysis,  # التحليل الذكي
            "first_aid_instructions": instructions,
            "overall_severity": ai_analysis['diagnosis']['severity'],
            "critical_alerts": health_summary['critical_alerts'],
            "warnings": health_summary['warnings'],
            "gps_location": sensor_readings['gps']['maps_link'],
            "timestamp": sensor_readings['timestamp']
        }
        
        # 6. Generate EMS Report
        ems_report = report_generator.generate_report(assessment, sensor_readings)
        complete_report['ems_report_path'] = str(ems_report)
        
        log.info(f"Complete AI assessment: {ai_analysis['diagnosis']['severity']}")
        
        return {"success": True, **complete_report}
        
    except Exception as e:
        log.error(f"Complete assessment failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))






@app.post("/api/emergency/download-report")
async def download_pdf_report(data: dict):
    """
    Generate and download PDF report with patient photo and GPS location
    
    - **data**: Contains assessment and patient_image_path
    """
    try:
        from fastapi.responses import FileResponse
        from datetime import datetime
        
        log.info("PDF report generation requested")
        
        # Extract assessment and image path
        assessment = data.get('assessment', {})
        patient_image_path = data.get('patient_image_path')
        
        # Validate assessment data
        if not assessment:
            log.error("No assessment data provided")
            raise HTTPException(status_code=400, detail="Assessment data is required")
        
        # Add GPS location to assessment if available
        if 'location' not in assessment or not assessment['location']:
            try:
                location_data = data_fusion.gps_module.read()
                if location_data:
                    assessment['location'] = location_data
            except Exception as e:
                log.warning(f"Could not get GPS location: {e}")
        
        # Generate PDF with patient photo and location
        pdf_path = pdf_generator.generate_pdf_report(
            assessment=assessment,
            patient_image_path=patient_image_path
        )
        
        if not pdf_path.exists():
            log.error("PDF file was not created")
            raise HTTPException(status_code=500, detail="Failed to generate PDF file")
        
        log.info(f"PDF generated successfully: {pdf_path}")
        
        # Return file for download
        filename = f"medical_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        return FileResponse(
            path=str(pdf_path),
            media_type='application/pdf',
            filename=filename,
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"PDF generation failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF: {str(e)}")
        
    except Exception as e:
        log.error(f"PDF generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=config.DEBUG
    )
