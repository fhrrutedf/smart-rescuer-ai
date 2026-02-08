# تفعيل الذكاء الاصطناعي - Enable AI

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Smart Rescuer - AI Activation" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "This script will install TensorFlow to enable AI features" -ForegroundColor Yellow
Write-Host ""
Write-Host "Required components:" -ForegroundColor White
Write-Host "  - TensorFlow 2.15.0 (approx. 400-500 MB)" -ForegroundColor Gray
Write-Host "  - NumPy, OpenCV, Pillow" -ForegroundColor Gray
Write-Host ""

$response = Read-Host "Do you want to continue? (Y/N)"

if ($response -ne 'Y' -and $response -ne 'y') {
    Write-Host "Installation cancelled." -ForegroundColor Yellow
    exit 0
}

# Change to backend directory
Set-Location -Path "$PSScriptRoot\backend"

Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Cyan

# Check if virtual environment exists
if (-Not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "Virtual environment not found. Creating..." -ForegroundColor Yellow
    python -m venv venv
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
}

.\venv\Scripts\Activate.ps1

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Installing AI Libraries..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Install TensorFlow
Write-Host "1. Installing TensorFlow..." -ForegroundColor Yellow
pip install tensorflow==2.15.0

if ($LASTEXITCODE -eq 0) {
    Write-Host "   OK TensorFlow installed successfully" -ForegroundColor Green
} else {
    Write-Host "   WARNING Installation had issues, trying CPU-only version..." -ForegroundColor Yellow
    pip install tensorflow-cpu==2.15.0
}

Write-Host ""

# Install other dependencies
Write-Host "2. Installing NumPy..." -ForegroundColor Yellow
pip install numpy==1.24.3 --quiet

Write-Host "3. Installing OpenCV..." -ForegroundColor Yellow
pip install opencv-python==4.8.1.78 --quiet

Write-Host "4. Installing Pillow..." -ForegroundColor Yellow
pip install Pillow==10.1.0 --quiet

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Verifying Installation..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verify TensorFlow
python -c "import tensorflow as tf; print(f'TensorFlow version: {tf.__version__}')"

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "SUCCESS! AI is now enabled" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Restart the backend server" -ForegroundColor White
    Write-Host "2. Look for this message in logs:" -ForegroundColor White
    Write-Host "   'Injury detection model loaded from...'" -ForegroundColor Gray
    Write-Host ""
    Write-Host "The AI will now:" -ForegroundColor Yellow
    Write-Host "  + Detect 7 types of injuries from images" -ForegroundColor Green
    Write-Host "  + Provide confidence scores for each detection" -ForegroundColor Green
    Write-Host "  + Use advanced computer vision" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "Installation had issues" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "The system will still work using rule-based detection" -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
