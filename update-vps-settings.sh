#!/bin/bash
# ========================================
# تحديث سريع للإعدادات - Quick Settings Update
# ========================================

VPS_IP="76.13.40.84"
API_PORT="8000"
FRONTEND_PORT="3000"

echo "========================================="
echo "🔧 تحديث إعدادات المشروع للـ VPS"
echo "========================================="
echo ""
echo "VPS IP: $VPS_IP"
echo "API Port: $API_PORT"
echo "Frontend Port: $FRONTEND_PORT"
echo ""

# ========================================
# تحديث ملف .env
# ========================================
echo "📝 إنشاء ملف .env..."
cat > .env <<EOF
# VPS Configuration
VPS_IP=${VPS_IP}
API_PORT=${API_PORT}
FRONTEND_PORT=${FRONTEND_PORT}

# API Configuration
API_HOST=0.0.0.0
API_PORT=${API_PORT}
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
SECRET_KEY=$(openssl rand -hex 32 2>/dev/null || echo "change-me-in-production")
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
EOF

echo "✅ ملف .env تم إنشاؤه"

# ========================================
# تحديث frontend .env.production
# ========================================
echo "📝 تحديث frontend .env.production..."
cat > frontend/.env.production <<EOF
# Production environment variables
VITE_API_URL=http://${VPS_IP}:${API_PORT}
EOF

echo "✅ frontend .env.production تم تحديثه"

# ========================================
# إنشاء ملف تكوين nginx محسّن
# ========================================
echo "📝 تحديث nginx configuration..."
mkdir -p nginx

cat > nginx/nginx.conf <<'EOF'
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Performance settings
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    client_max_body_size 10M;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript application/json application/javascript application/xml+rss application/rss+xml font/truetype font/opentype application/vnd.ms-fontobject image/svg+xml;

    # Upstream backend
    upstream backend {
        server backend:8000;
    }

    # Upstream frontend
    upstream frontend {
        server frontend:80;
    }

    server {
        listen 80;
        server_name _;

        # Frontend
        location / {
            proxy_pass http://frontend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
        }

        # Backend API
        location /api/ {
            rewrite ^/api/(.*) /$1 break;
            proxy_pass http://backend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_cache_bypass $http_upgrade;
            proxy_read_timeout 180s;
            proxy_connect_timeout 180s;
            proxy_send_timeout 180s;
        }

        # Health check endpoint
        location /health {
            proxy_pass http://backend/health;
            access_log off;
        }
    }
}
EOF

echo "✅ nginx configuration تم تحديثه"

# ========================================
# النتائج
# ========================================
echo ""
echo "========================================="
echo "✅ تم تحديث جميع الإعدادات بنجاح!"
echo "========================================="
echo ""
echo "📋 الملفات المحدثة:"
echo "  ✓ .env"
echo "  ✓ frontend/.env.production"
echo "  ✓ nginx/nginx.conf"
echo ""
echo "🚀 الخطوة التالية:"
echo "  1. انسخ المشروع إلى VPS:"
echo "     scp -r smart-rescuer root@${VPS_IP}:/var/www/"
echo ""
echo "  2. اتصل بـ VPS:"
echo "     ssh root@${VPS_IP}"
echo ""
echo "  3. شغّل سكريبت النشر:"
echo "     cd /var/www/smart-rescuer"
echo "     chmod +x vps-deploy-complete.sh"
echo "     ./vps-deploy-complete.sh"
echo ""
echo "========================================="
