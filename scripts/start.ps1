# Smart Rescuer - Startup Script for Windows PowerShell

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "المنقذ الذكي - Smart Rescuer" -ForegroundColor Green
Write-Host "Starting System..." -ForegroundColor Yellow
Write-Host "======================================" -ForegroundColor Cyan

# Check if virtual environment exists
if (!(Test-Path "backend\venv")) {
    Write-Host "❌ Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run install.ps1 first" -ForegroundColor Yellow
    exit 1
}

# Start Backend
Write-Host ""
Write-Host "🚀 Starting Backend (FastAPI)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; .\venv\Scripts\Activate.ps1; uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload"

# Wait for backend to start
Start-Sleep -Seconds 3

# Start Frontend
Write-Host ""
Write-Host "🌐 Starting Frontend (React + Vite)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "✅ Smart Rescuer is Running!" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Backend API: http://localhost:8000" -ForegroundColor White
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host "Frontend UI: http://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host "Close the terminal windows to stop services" -ForegroundColor Yellow
Write-Host "======================================" -ForegroundColor Cyan
