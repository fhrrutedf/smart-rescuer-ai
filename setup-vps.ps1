# ========================================
# Smart Rescuer - VPS Setup Script for Windows
# سكريبت إعداد VPS من Windows
# ========================================

$VPS_IP = "76.13.40.84"
$API_PORT = "8000"
$FRONTEND_PORT = "3000"
$VPS_USER = "root"  # غيّر هذا إذا كان لديك مستخدم مختلف

Write-Host "==========================================" -ForegroundColor Green
Write-Host "🚀 Smart Rescuer - إعداد VPS" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "VPS IP: $VPS_IP" -ForegroundColor Yellow
Write-Host "API Port: $API_PORT" -ForegroundColor Yellow
Write-Host "Frontend Port: $FRONTEND_PORT" -ForegroundColor Yellow
Write-Host ""

# ========================================
# الخطوة 1: تحديث الإعدادات المحلية
# ========================================
Write-Host "[1/4] تحديث الإعدادات المحلية..." -ForegroundColor Cyan

# إنشاء ملف .env
$envContent = @"
# VPS Configuration
VPS_IP=$VPS_IP
API_PORT=$API_PORT
FRONTEND_PORT=$FRONTEND_PORT

# API Configuration
API_HOST=0.0.0.0
API_PORT=$API_PORT
DEBUG=False

# Frontend Configuration  
VITE_API_URL=http://${VPS_IP}:${API_PORT}

# AI Configuration
ENABLE_AI=True
AI_MODEL_PATH=/app/ai_engine/models
USE_GPU=False
AI_BATCH_SIZE=1
AI_CONFIDENCE_THRESHOLD=0.6

# Performance
WORKERS=4
TIMEOUT=180
MAX_REQUEST_SIZE=10485760
KEEP_ALIVE=5

# Security
SECRET_KEY=$(([System.Security.Cryptography.RandomNumberGenerator]::Create()).GetBytes(32) | ForEach-Object { $_.ToString("x2") }) -join ''
ALLOWED_ORIGINS=http://${VPS_IP}:${FRONTEND_PORT},http://${VPS_IP}
CORS_ENABLED=True

# Hardware Sensors (Disabled for VPS)
ENABLE_ECG=False
ENABLE_SPO2=False
ENABLE_TEMP=False
ENABLE_GPS=False

# Logging
LOG_LEVEL=INFO
LOG_FILE=/app/logs/app.log

# Database
DATABASE_URL=sqlite:///./smart_rescuer.db
DATABASE_ECHO=False

# File Storage
UPLOAD_DIR=/app/uploads
REPORTS_DIR=/app/reports
MAX_UPLOAD_SIZE=10485760
"@

$envContent | Out-File -FilePath ".env" -Encoding UTF8
Write-Host "✅ ملف .env تم إنشاؤه" -ForegroundColor Green

# تحديث frontend .env.production
$frontendEnv = @"
# Production environment variables
VITE_API_URL=http://${VPS_IP}:${API_PORT}
"@

$frontendEnv | Out-File -FilePath "frontend\.env.production" -Encoding UTF8
Write-Host "✅ frontend .env.production تم تحديثه" -ForegroundColor Green

# ========================================
# الخطوة 2: فحص الملفات المطلوبة
# ========================================
Write-Host ""
Write-Host "[2/4] فحص الملفات المطلوبة..." -ForegroundColor Cyan

$requiredFiles = @(
    "docker-compose.yml",
    "backend\Dockerfile",
    "backend\requirements-production.txt",
    "frontend\Dockerfile",
    "vps-deploy-complete.sh"
)

$allFilesExist = $true
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file غير موجود!" -ForegroundColor Red
        $allFilesExist = $false
    }
}

if (-not $allFilesExist) {
    Write-Host ""
    Write-Host "⚠️ بعض الملفات المطلوبة غير موجودة!" -ForegroundColor Red
    Write-Host "الرجاء التأكد من وجود جميع الملفات قبل المتابعة." -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "✅ جميع الملفات المطلوبة موجودة" -ForegroundColor Green

# ========================================
# الخطوة 3: عرض تعليمات النشر
# ========================================
Write-Host ""
Write-Host "[3/4] تعليمات النشر على VPS" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Yellow

Write-Host ""
Write-Host "📋 الخيار 1: استخدام SCP (مستحسن)" -ForegroundColor Yellow
Write-Host "   نسخ الملفات:" -ForegroundColor White
Write-Host "   scp -r . ${VPS_USER}@${VPS_IP}:/var/www/smart-rescuer" -ForegroundColor Cyan
Write-Host ""
Write-Host "   الاتصال بـ VPS:" -ForegroundColor White
Write-Host "   ssh ${VPS_USER}@${VPS_IP}" -ForegroundColor Cyan
Write-Host ""
Write-Host "   تشغيل النشر:" -ForegroundColor White
Write-Host "   cd /var/www/smart-rescuer" -ForegroundColor Cyan
Write-Host "   chmod +x vps-deploy-complete.sh" -ForegroundColor Cyan
Write-Host "   ./vps-deploy-complete.sh" -ForegroundColor Cyan

Write-Host ""
Write-Host "📋 الخيار 2: استخدام WinSCP" -ForegroundColor Yellow
Write-Host "   1. افتح WinSCP" -ForegroundColor White
Write-Host "   2. اتصل بـ: ${VPS_IP}" -ForegroundColor White
Write-Host "   3. انسخ مجلد المشروع إلى: /var/www/smart-rescuer" -ForegroundColor White
Write-Host "   4. استخدم PuTTY للاتصال وتشغيل السكريبت" -ForegroundColor White

Write-Host ""
Write-Host "==========================================" -ForegroundColor Yellow

# ========================================
# الخطوة 4: عرض معلومات الوصول
# ========================================
Write-Host ""
Write-Host "[4/4] معلومات الوصول بعد النشر" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Yellow
Write-Host "  Backend API:  http://${VPS_IP}:${API_PORT}" -ForegroundColor Green
Write-Host "  Frontend:     http://${VPS_IP}:${FRONTEND_PORT}" -ForegroundColor Green
Write-Host "  Health Check: http://${VPS_IP}:${API_PORT}/health" -ForegroundColor Green
Write-Host "  API Docs:     http://${VPS_IP}:${API_PORT}/docs" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Yellow

# ========================================
# تفعيل النسخ التلقائي (اختياري)
# ========================================
Write-Host ""
$autoUpload = Read-Host "هل تريد نسخ الملفات تلقائياً الآن؟ (y/n)"

if ($autoUpload -eq 'y' -or $autoUpload -eq 'Y') {
    Write-Host ""
    Write-Host "📤 نسخ الملفات إلى VPS..." -ForegroundColor Cyan
    
    # التحقق من وجود SCP
    $scpCommand = Get-Command scp -ErrorAction SilentlyContinue
    if (-not $scpCommand) {
        Write-Host "⚠️ SCP غير متوفر. الرجاء تثبيت OpenSSH أو استخدام WinSCP." -ForegroundColor Red
        Write-Host ""
        Write-Host "لتثبيت OpenSSH على Windows:" -ForegroundColor Yellow
        Write-Host "1. Settings > Apps > Optional Features" -ForegroundColor White
        Write-Host "2. Add a feature" -ForegroundColor White
        Write-Host "3. ابحث عن OpenSSH Client وثبّته" -ForegroundColor White
    } else {
        Write-Host ""
        Write-Host "ملاحظة: سيطلب منك إدخال كلمة مرور VPS" -ForegroundColor Yellow
        Write-Host ""
        
        # نسخ الملفات
        scp -r . ${VPS_USER}@${VPS_IP}:/var/www/smart-rescuer
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "✅ تم نسخ الملفات بنجاح!" -ForegroundColor Green
            Write-Host ""
            Write-Host "الخطوة التالية: اتصل بـ VPS وشغّل سكريبت النشر" -ForegroundColor Yellow
            Write-Host "ssh ${VPS_USER}@${VPS_IP}" -ForegroundColor Cyan
        } else {
            Write-Host ""
            Write-Host "❌ فشل نسخ الملفات. الرجاء المحاولة يدوياً." -ForegroundColor Red
        }
    }
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "✅ إعداد VPS مكتمل!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "📖 للمزيد من التفاصيل، اقرأ: VPS_DEPLOYMENT_GUIDE_AR.md" -ForegroundColor Yellow
Write-Host ""

# فتح الدليل
$openGuide = Read-Host "هل تريد فتح دليل النشر؟ (y/n)"
if ($openGuide -eq 'y' -or $openGuide -eq 'Y') {
    Start-Process "VPS_DEPLOYMENT_GUIDE_AR.md"
}
