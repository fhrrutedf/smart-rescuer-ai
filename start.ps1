# تشغيل Smart Rescuer - Full Stack

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Smart Rescuer - Full Stack Launch" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Starting Backend and Frontend servers..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Backend API: http://localhost:8000" -ForegroundColor Green
Write-Host "Frontend UI: http://localhost:5173" -ForegroundColor Green
Write-Host ""
Write-Host "IMPORTANT: This will open 2 terminal windows." -ForegroundColor Yellow
Write-Host "Keep both windows open while using the application." -ForegroundColor Yellow
Write-Host ""

# Start Backend in new window
Write-Host "Starting Backend server..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-ExecutionPolicy Bypass -NoExit -File `"$PSScriptRoot\start-backend.ps1`""

# Wait a bit for backend to start
Write-Host "Waiting for backend to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Start Frontend in new window
Write-Host "Starting Frontend server..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-ExecutionPolicy Bypass -NoExit -File `"$PSScriptRoot\start-frontend.ps1`""

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Servers are starting!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Once both servers are ready:" -ForegroundColor Yellow
Write-Host "1. Backend will be at: http://localhost:8000" -ForegroundColor White
Write-Host "2. Frontend will be at: http://localhost:5173" -ForegroundColor White
Write-Host ""
Write-Host "The frontend will automatically open in your browser." -ForegroundColor Green
Write-Host ""
Write-Host "Press any key to exit this launcher..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
