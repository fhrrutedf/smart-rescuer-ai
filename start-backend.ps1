# تشغيل Smart Rescuer - Backend Server

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Smart Rescuer - Backend Server" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Change to backend directory
Set-Location -Path "$PSScriptRoot\backend"

# Check if virtual environment exists
if (-Not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "Virtual environment not found. Creating..." -ForegroundColor Yellow
    python -m venv venv
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
.\venv\Scripts\Activate.ps1

# Install/Update reportlab
Write-Host "Installing reportlab..." -ForegroundColor Cyan
pip install reportlab==4.0.7 --quiet

if ($LASTEXITCODE -eq 0) {
    Write-Host "reportlab installed successfully" -ForegroundColor Green
} else {
    Write-Host "Warning: reportlab installation had issues" -ForegroundColor Yellow
}

# Start the server
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting Backend Server..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "API will be available at: http://localhost:8000" -ForegroundColor Yellow
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""

# Run the server
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
