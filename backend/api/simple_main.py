"""
Simplified FastAPI application for testing - No AI dependencies
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Smart Rescuer API - Simple Mode",
    description="Emergency medical response system (testing mode)",
    version="1.0.0"
)

# CORS middleware - Allow all origins for testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "Smart Rescuer API - Simple Mode",
        "version": "1.0.0",
        "status": "running",
        "mode": "simplified_testing",
        "message": "AI features disabled for testing"
    }

@app.get("/api/status")
async def get_status():
    """Get system status"""
    return {
        "status": "online",
        "sensors": {
            "ecg": {"status": "simulated", "enabled": False},
            "spo2": {"status": "simulated", "enabled": False},
            "temperature": {"status": "simulated", "enabled": False},
            "gps": {"status": "simulated", "enabled": False}
        },
        "version": "1.0.0",
        "debug_mode": True
    }

@app.post("/api/emergency/assess")
async def assess_emergency():
    """Simplified emergency assessment"""
    return JSONResponse(content={
        "assessment": {
            "status": "simulated",
            "message": "This is a test response. Full AI features will be enabled after installing all dependencies.",
            "severity": "moderate",
            "detected_injuries": ["Testing mode - No actual analysis"],
            "requires_ems": False
        },
        "report": {
            "summary": "Test mode active"
        },
        "text_summary": "System is running in test mode. Full AI features available after setup completion."
    })

@app.get("/api/sensors/vitals")
async def get_vital_signs():
    """Get simulated vital signs"""
    return {
        "vital_signs": {
            "heart_rate": 75,
            "spo2": 98,
            "temperature": 37.0,
            "status": "simulated"
        }
    }

@app.get("/api/location")
async def get_location():
    """Get simulated GPS location"""
    return {
        "location": {
            "latitude": 0.0,
            "longitude": 0.0,
            "status": "simulated",
            "maps_url": "https://maps.google.com"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("simple_main:app", host="0.0.0.0", port=8000, reload=True)
