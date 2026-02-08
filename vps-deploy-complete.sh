#!/bin/bash
# ========================================
# Smart Rescuer - VPS Deployment Script
# سكريبت نشر كامل على Hostinger VPS
# ========================================

set -e  # إيقاف عند أي خطأ

# Colors for better output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}🚀 Smart Rescuer - VPS Deployment${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

VPS_IP="76.13.40.84"
API_PORT="8000"
FRONTEND_PORT="3000"

# ========================================
# الخطوة 1: تحديث النظام
# ========================================
echo -e "${BLUE}[1/10]${NC} تحديث النظام..."
sudo apt update && sudo apt upgrade -y

# ========================================
# الخطوة 2: تثبيت المتطلبات الأساسية
# ========================================
echo -e "${BLUE}[2/10]${NC} تثبيت المتطلبات الأساسية..."
sudo apt install -y \
    curl \
    wget \
    git \
    build-essential \
    software-properties-common \
    ca-certificates \
    gnupg \
    lsb-release

# ========================================
# الخطوة 3: تثبيت Docker
# ========================================
echo -e "${BLUE}[3/10]${NC} تثبيت Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
    echo -e "${GREEN}✓ Docker installed successfully${NC}"
else
    echo -e "${YELLOW}✓ Docker already installed${NC}"
fi

# ========================================
# الخطوة 4: تثبيت Docker Compose
# ========================================
echo -e "${BLUE}[4/10]${NC} تثبيت Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    echo -e "${GREEN}✓ Docker Compose installed successfully${NC}"
else
    echo -e "${YELLOW}✓ Docker Compose already installed${NC}"
fi

# ========================================
# الخطوة 5: إعداد مجلد المشروع
# ========================================
echo -e "${BLUE}[5/10]${NC} التحقق من مجلد المشروع..."
PROJECT_DIR="/var/www/smart-rescuer"
CURRENT_DIR=$(pwd)

# إذا كنا لسنا داخل المجلد، نحاول الانتقال إليه أو إنشائه
if [ "$CURRENT_DIR" != "$PROJECT_DIR" ]; then
    echo "نقل الملفات إلى $PROJECT_DIR..."
    sudo mkdir -p $PROJECT_DIR
    sudo cp -r ./* $PROJECT_DIR/
    sudo chown -R $USER:$USER $PROJECT_DIR
    cd $PROJECT_DIR
fi

# ========================================
# الخطوة 6: التأكد من وجود الملفات الضرورية
# ========================================
echo -e "${BLUE}[6/10]${NC} التحقق من الملفات..."
if [ ! -f "docker-compose.yml" ]; then
    echo -e "${RED}خطأ: ملف docker-compose.yml غير موجود!${NC}"
    echo "تأكد من أنك قمت بـ git clone بشكل صحيح."
    exit 1
fi
echo -e "${GREEN}✓ الملفات موجودة${NC}"


# ========================================
# الخطوة 7: إنشاء ملف .env
# ========================================
echo -e "${BLUE}[7/10]${NC} إنشاء ملف البيئة..."
cat > .env <<EOF
# API Configuration
API_HOST=0.0.0.0
API_PORT=${API_PORT}
DEBUG=False

# Frontend Configuration  
VITE_API_URL=http://${VPS_IP}:${API_PORT}

# AI Configuration
ENABLE_AI=True
AI_MODEL_PATH=/app/ai_engine/models

# Performance
WORKERS=4

# Security
SECRET_KEY=$(openssl rand -hex 32)

# Hardware Sensors (Disabled for VPS)
ENABLE_ECG=False
ENABLE_SPO2=False
ENABLE_TEMP=False
ENABLE_GPS=False
EOF

echo -e "${GREEN}✓ Environment file created${NC}"

# ========================================
# الخطوة 8: بناء وتشغيل Docker Containers
# ========================================
echo -e "${BLUE}[8/10]${NC} بناء وتشغيل الـ Containers..."

# Build images
docker-compose build --no-cache

# Start containers
docker-compose up -d

# Wait for services to start
echo "انتظار تشغيل الخدمات..."
sleep 15

# ========================================
# الخطوة 9: تثبيت مكتبات AI داخل الـ Container
# ========================================
echo -e "${BLUE}[9/10]${NC} تثبيت مكتبات AI..."
docker-compose exec -T backend pip install --upgrade pip
docker-compose exec -T backend pip install tensorflow==2.15.0 --no-cache-dir
docker-compose exec -T backend pip install torch==2.1.0 torchvision==0.16.0 --index-url https://download.pytorch.org/whl/cpu --no-cache-dir

# Test AI installation
echo "اختبار تثبيت AI..."
docker-compose exec -T backend python -c "import tensorflow as tf; print(f'✓ TensorFlow {tf.__version__} installed')"

# ========================================
# الخطوة 10: إعداد الـ Firewall
# ========================================
echo -e "${BLUE}[10/10]${NC} إعداد الـ Firewall..."
if command -v ufw &> /dev/null; then
    sudo ufw --force enable
    sudo ufw allow 22/tcp    # SSH
    sudo ufw allow ${API_PORT}/tcp    # Backend API
    sudo ufw allow ${FRONTEND_PORT}/tcp   # Frontend
    sudo ufw allow 80/tcp    # HTTP
    sudo ufw allow 443/tcp   # HTTPS
    echo -e "${GREEN}✓ Firewall configured${NC}"
fi

# ========================================
# التحقق من التشغيل
# ========================================
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✓ التشغيل مكتمل!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${YELLOW}المشروع يعمل الآن على:${NC}"
echo -e "  Backend API:  ${GREEN}http://${VPS_IP}:${API_PORT}${NC}"
echo -e "  Frontend:     ${GREEN}http://${VPS_IP}:${FRONTEND_PORT}${NC}"
echo -e "  Health Check: ${GREEN}http://${VPS_IP}:${API_PORT}/health${NC}"
echo ""
echo -e "${YELLOW}أوامر مفيدة:${NC}"
echo "  docker-compose logs -f              # عرض السجلات"
echo "  docker-compose ps                   # حالة الخدمات"
echo "  docker-compose restart              # إعادة التشغيل"
echo "  docker-compose down                 # إيقاف الخدمات"
echo "  docker-compose up -d --build        # إعادة البناء والتشغيل"
echo ""
echo -e "${YELLOW}اختبار الـ API:${NC}"
echo "  curl http://${VPS_IP}:${API_PORT}/health"
echo ""
echo -e "${GREEN}========================================${NC}"

# Restart services one more time to ensure everything is loaded
echo "إعادة تشغيل نهائية..."
docker-compose restart

echo -e "${GREEN}✅ جميع الخدمات جاهزة!${NC}"
