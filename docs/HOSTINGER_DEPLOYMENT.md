# Smart Rescuer - دليل النشر على Hostinger VPS

## 🚀 نشر المشروع على VPS

### المتطلبات:
- VPS من Hostinger
- Domain (اختياري)
- SSH Access

---

## 📋 الخطوات:

### 1️⃣ الاتصال بالـ VPS

```bash
ssh root@your-vps-ip
```

### 2️⃣ تحديث النظام وتثبيت المتطلبات

```bash
# تحديث النظام
apt update && apt upgrade -y

# تثبيت Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# تثبيت Docker Compose
apt install docker-compose -y

# تثبيت Git
apt install git -y
```

### 3️⃣ رفع المشروع للـ VPS

**الطريقة 1: من GitHub**
```bash
cd /var/www
git clone https://github.com/your-username/smart-rescuer.git
cd smart-rescuer
```

**الطريقة 2: رفع مباشر (من جهازك)**
```bash
# على جهازك (Windows)
scp -r "d:\ghaz tbee\smart-rescuer" root@your-vps-ip:/var/www/
```

### 4️⃣ إعداد ملفات البيئة

```bash
cd /var/www/smart-rescuer

# إنشاء ملف .env
cat > .env << EOF
# Domain Configuration
DOMAIN=your-domain.com
EMAIL=your-email@example.com

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False

# Frontend Configuration
VITE_API_URL=https://your-domain.com

# Security
SECRET_KEY=$(openssl rand -hex 32)
EOF
```

### 5️⃣ بناء وتشغيل المشروع

```bash
# بناء الصور
docker-compose build

# تشغيل الخدمات
docker-compose up -d
```

### 6️⃣ إعداد SSL (HTTPS)

```bash
# تشغيل Certbot للحصول على شهادة SSL
docker-compose run --rm certbot certonly \
  --webroot \
  --webroot-path=/var/www/certbot \
  -d your-domain.com \
  -d www.your-domain.com \
  --email your-email@example.com \
  --agree-tos \
  --no-eff-email

# إعادة تشغيل Nginx
docker-compose restart nginx
```

### 7️⃣ تشغيل setup للـ AI Model

```bash
# الدخول للـ container
docker-compose exec backend bash

# تشغيل setup AI
python scripts/setup_ai_quick.py

# الخروج
exit

# إعادة تشغيل Backend
docker-compose restart backend
```

---

## 🔧 إدارة المشروع

### عرض الـ Logs
```bash
# كل الخدمات
docker-compose logs -f

# Backend فقط
docker-compose logs -f backend

# Frontend فقط
docker-compose logs -f frontend
```

### إيقاف وتشغيل
```bash
# إيقاف
docker-compose stop

# تشغيل
docker-compose start

# إعادة تشغيل
docker-compose restart
```

### تحديث المشروع
```bash
# سحب آخر تحديثات
cd /var/www/smart-rescuer
git pull origin main

# إعادة البناء والتشغيل
docker-compose down
docker-compose build
docker-compose up -d
```

---

## 🌐 الوصول للمشروع

بعد النشر بنجاح:

### Frontend:
```
https://your-domain.com
```

### Backend API:
```
https://your-domain.com/api
```

### API Documentation:
```
https://your-domain.com/docs
```

---

## 🔒 الأمان

### إعداد Firewall
```bash
# تفعيل UFW
ufw enable

# السماح بـ SSH
ufw allow 22/tcp

# السماح بـ HTTP/HTTPS
ufw allow 80/tcp
ufw allow 443/tcp

# التحقق
ufw status
```

### تغيير كلمة مرور SSH
```bash
passwd
```

---

## 📊 مراقبة الأداء

### استخدام الموارد
```bash
# CPU & Memory
docker stats

# Disk Usage
df -h

# Docker Images
docker images
```

### تنظيف Docker
```bash
# حذف الصور غير المستخدمة
docker system prune -a

# حذف الـ volumes غير المستخدمة
docker volume prune
```

---

## 🚨 استكشاف الأخطاء

### المشروع لا يعمل؟

1. **تحقق من الـ Logs**
```bash
docker-compose logs backend
docker-compose logs frontend
docker-compose logs nginx
```

2. **تحقق من الـ Containers**
```bash
docker-compose ps
```

3. **إعادة بناء كامل**
```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### SSL لا يعمل؟

```bash
# تجديد الشهادة
docker-compose run --rm certbot renew

# إعادة تشغيل Nginx
docker-compose restart nginx
```

---

## 📝 ملاحظات هامة

1. ✅ **AI Model**: سيعمل offline بعد أول setup
2. ✅ **Sensors**: في وضع Simulation حتى توصيل الجهاز
3. ✅ **Database**: SQLite (يمكن ترقية لـ PostgreSQL)
4. ✅ **Auto-Renew SSL**: يتجدد تلقائياً كل 90 يوم

---

## 🎯 الخطوات المختصرة

```bash
# 1. الاتصال
ssh root@your-vps-ip

# 2. تثبيت Docker
curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh

# 3. رفع المشروع
cd /var/www
# (رفع الملفات هنا)

# 4. تشغيل
cd smart-rescuer
docker-compose up -d

# 5. Setup AI
docker-compose exec backend python scripts/setup_ai_quick.py

# ✅ جاهز!
```

---

**المشروع الآن على الإنترنت! 🎉**

الوصول: `https://your-domain.com`

---

## 💾 النسخ الاحتياطي والاستعادة

### إنشاء نسخة احتياطية

```bash
# إنشاء مجلد للنسخ الاحتياطية
mkdir -p /backups/smart-rescuer

# نسخ قاعدة البيانات
docker-compose exec backend cp /app/data/smart_rescuer.db /app/backups/
docker cp $(docker-compose ps -q backend):/app/backups/smart_rescuer.db /backups/smart-rescuer/db_$(date +%Y%m%d_%H%M%S).db

# نسخ ملفات التكوين
cp -r /var/www/smart-rescuer/.env /backups/smart-rescuer/env_$(date +%Y%m%d_%H%M%S)

# نسخ AI Models
docker cp $(docker-compose ps -q backend):/app/models /backups/smart-rescuer/models_$(date +%Y%m%d_%H%M%S)
```

### جدولة النسخ الاحتياطي التلقائي

```bash
# فتح crontab
crontab -e

# إضافة نسخ احتياطي يومي في الساعة 2 صباحاً
0 2 * * * /var/www/smart-rescuer/scripts/backup.sh
```

### إنشاء سكريبت النسخ الاحتياطي

```bash
cat > /var/www/smart-rescuer/scripts/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/backups/smart-rescuer"
DATE=$(date +%Y%m%d_%H%M%S)

# إنشاء مجلد
mkdir -p $BACKUP_DIR

# نسخ قاعدة البيانات
docker-compose -f /var/www/smart-rescuer/docker-compose.yml exec -T backend \
  cp /app/data/smart_rescuer.db /app/backups/

docker cp $(docker-compose -f /var/www/smart-rescuer/docker-compose.yml ps -q backend):/app/backups/smart_rescuer.db \
  $BACKUP_DIR/db_$DATE.db

# حذف النسخ القديمة (أكثر من 7 أيام)
find $BACKUP_DIR -name "db_*.db" -mtime +7 -delete

echo "Backup completed: $DATE"
EOF

# جعل السكريبت قابل للتنفيذ
chmod +x /var/www/smart-rescuer/scripts/backup.sh
```

### استعادة النسخة الاحتياطية

```bash
# إيقاف الخدمات
docker-compose down

# استعادة قاعدة البيانات
docker-compose up -d backend
docker cp /backups/smart-rescuer/db_YYYYMMDD_HHMMSS.db \
  $(docker-compose ps -q backend):/app/data/smart_rescuer.db

# إعادة تشغيل كل الخدمات
docker-compose restart
```

---

## ⚡ تحسين الأداء

### 1. تحسين Nginx

```bash
# تحرير ملف nginx.conf
nano /var/www/smart-rescuer/nginx/nginx.conf
```

إضافة التحسينات التالية:

```nginx
# Gzip Compression
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/javascript application/json;

# Cache Control
location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}

# Rate Limiting
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
limit_req zone=api_limit burst=20 nodelay;
```

### 2. تحسين Docker

```bash
# تحرير docker-compose.yml
nano /var/www/smart-rescuer/docker-compose.yml
```

إضافة حدود للموارد:

```yaml
services:
  backend:
    # ... existing config
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 512M
          
  frontend:
    # ... existing config
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
```

### 3. تمكين Redis للـ Caching (اختياري)

```bash
# إضافة Redis للـ docker-compose.yml
cat >> docker-compose.yml << 'EOF'
  redis:
    image: redis:alpine
    restart: unless-stopped
    volumes:
      - redis_data:/data
    networks:
      - backend

volumes:
  redis_data:
EOF

# إعادة تشغيل
docker-compose up -d
```

---

## 🌍 ربط الدومين (Domain Setup)

### في لوحة تحكم Hostinger:

1. الذهاب إلى **DNS/Nameservers**
2. إضافة/تعديل السجلات:

```
Type    Name    Content            TTL
A       @       YOUR_VPS_IP        3600
A       www     YOUR_VPS_IP        3600
CNAME   api     your-domain.com    3600
```

### التحقق من الدومين:

```bash
# انتظر 5-10 دقائق ثم تحقق
ping your-domain.com
nslookup your-domain.com

# إذا كان يشير لـ VPS IP، جاهز للاستخدام
```

### تحديث ملف .env:

```bash
nano /var/www/smart-rescuer/.env

# تحديث:
DOMAIN=your-domain.com
VITE_API_URL=https://your-domain.com
```

### إعادة إصدار SSL للدومين الجديد:

```bash
# إيقاف Nginx مؤقتاً
docker-compose stop nginx

# إصدار الشهادة
docker-compose run --rm certbot certonly \
  --standalone \
  -d your-domain.com \
  -d www.your-domain.com \
  --email your-email@example.com \
  --agree-tos

# تشغيل Nginx
docker-compose up -d nginx
```

---

## 🔄 التحديث التلقائي (CI/CD)

### إعداد GitHub Actions (اختياري)

إنشاء `.github/workflows/deploy.yml`:

```yaml
name: Deploy to VPS

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - name: Deploy to VPS
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.VPS_HOST }}
        username: root
        key: ${{ secrets.VPS_SSH_KEY }}
        script: |
          cd /var/www/smart-rescuer
          git pull origin main
          docker-compose down
          docker-compose build
          docker-compose up -d
          docker system prune -f
```

### إضافة Secrets في GitHub:

1. الذهاب إلى **Settings** → **Secrets and variables** → **Actions**
2. إضافة:
   - `VPS_HOST`: عنوان IP للـ VPS
   - `VPS_SSH_KEY`: المفتاح الخاص SSH

---

## 📧 إعداد التنبيهات

### تنبيهات البريد الإلكتروني عند توقف الخدمة:

```bash
# تثبيت أداة المراقبة
apt install mailutils -y

# إنشاء سكريبت المراقبة
cat > /var/www/smart-rescuer/scripts/monitor.sh << 'EOF'
#!/bin/bash
SERVICE="smart-rescuer"
EMAIL="your-email@example.com"

if ! docker-compose -f /var/www/smart-rescuer/docker-compose.yml ps | grep -q "Up"; then
    echo "Service $SERVICE is down!" | mail -s "Alert: $SERVICE Down" $EMAIL
    # محاولة إعادة التشغيل
    cd /var/www/smart-rescuer
    docker-compose restart
fi
EOF

chmod +x /var/www/smart-rescuer/scripts/monitor.sh

# جدولة الفحص كل 5 دقائق
crontab -e
# إضافة:
*/5 * * * * /var/www/smart-rescuer/scripts/monitor.sh
```

---

## 🔐 تحسين الأمان المتقدم

### 1. تعطيل SSH Password Login

```bash
# تحرير ملف SSH
nano /etc/ssh/sshd_config

# تغيير:
PasswordAuthentication no
PermitRootLogin prohibit-password

# إعادة تشغيل SSH
systemctl restart sshd
```

### 2. تثبيت Fail2Ban

```bash
# تثبيت
apt install fail2ban -y

# إنشاء ملف التكوين
cat > /etc/fail2ban/jail.local << 'EOF'
[sshd]
enabled = true
port = 22
maxretry = 3
bantime = 3600

[nginx-http-auth]
enabled = true
port = http,https
maxretry = 5
EOF

# تشغيل
systemctl enable fail2ban
systemctl start fail2ban
```

### 3. حماية من DDoS باستخدام Cloudflare (مجاني)

1. الذهاب إلى [Cloudflare](https://www.cloudflare.com)
2. إضافة موقعك
3. تحديث Nameservers في Hostinger
4. تفعيل:
   - SSL/TLS: Full (strict)
   - Under Attack Mode (عند الحاجة)
   - Rate Limiting

---

## 📊 Monitoring Dashboard (اختياري)

### تثبيت Portainer (واجهة إدارة Docker)

```bash
docker volume create portainer_data

docker run -d \
  -p 9000:9000 \
  --name portainer \
  --restart=unless-stopped \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  portainer/portainer-ce:latest
```

الوصول: `http://YOUR_VPS_IP:9000`

---

## ❓ أسئلة شائعة (FAQ)

### س: كم يستغرق النشر؟
**ج:** حوالي 15-30 دقيقة للنشر الكامل (أول مرة)

### س: هل يمكن استخدام VPS صغير؟
**ج:** نعم، يعمل على:
- **الحد الأدنى**: 2GB RAM, 1 CPU, 20GB Storage
- **الموصى به**: 4GB RAM, 2 CPU, 40GB Storage

### س: ماذا لو لم يكن لدي دومين؟
**ج:** يمكنك استخدام IP مباشرة، لكن بدون SSL:
```bash
# الوصول عبر
http://YOUR_VPS_IP
```

### س: كيف أحدّث المشروع؟
**ج:** 
```bash
cd /var/www/smart-rescuer
git pull
docker-compose down
docker-compose build
docker-compose up -d
```

### س: الموقع بطيء؟
**ج:** راجع قسم "⚡ تحسين الأداء" أعلاه

### س: كيف أشاهد الـ logs الحية؟
**ج:**
```bash
docker-compose logs -f --tail=100
```

---

## 🆘 الدعم والمساعدة

### مصادر إضافية:
- 📖 [Docker Documentation](https://docs.docker.com)
- 🌐 [Hostinger Knowledge Base](https://support.hostinger.com)
- 🔧 [Nginx Documentation](https://nginx.org/en/docs/)

### في حالة مشكلة:

1. **تحقق من الـ Logs** أولاً
2. **راجع قسم استكشاف الأخطاء** في هذا الدليل
3. **ابحث عن الخطأ** في Google/StackOverflow
4. **افتح Issue** على GitHub للمشروع

---

## ✅ Checklist قبل الإطلاق

- [ ] تم تثبيت Docker و Docker Compose
- [ ] تم رفع المشروع للـ VPS
- [ ] تم إعداد ملف .env صحيح
- [ ] تعمل جميع الـ containers (backend, frontend, nginx)
- [ ] تم إعداد SSL Certificate
- [ ] تم تشغيل AI Model Setup
- [ ] تم اختبار الوصول عبر الدومين
- [ ] تم إعداد Firewall
- [ ] تم إعداد النسخ الاحتياطي التلقائي
- [ ] تم تفعيل المراقبة والتنبيهات
- [ ] تم تحسين الأداء (Gzip, Caching, etc.)

---

## 🎉 تهانينا!

**مشروع Smart Rescuer الآن على الإنترنت ويعمل بكفاءة!**

```
 ____                       _     ____                               
/ ___| _ __ ___   __ _ _ __| |_  |  _ \ ___  ___  ___ _   _  ___ _ __ 
\___ \| '_ ` _ \ / _` | '__| __| | |_) / _ \/ __|/ __| | | |/ _ \ '__|
 ___) | | | | | | (_| | |  | |_  |  _ <  __/\__ \ (__| |_| |  __/ |   
|____/|_| |_| |_|\__,_|_|   \__| |_| \_\___||___/\___|\__,_|\___|_|   
                                                                       
        🚀 Online & Ready to Save Lives 🚀
```

**للوصول:**
- 🌐 الموقع: `https://your-domain.com`
- 📱 API: `https://your-domain.com/api`
- 📚 Docs: `https://your-domain.com/docs`

---

**آخر تحديث:** 2026-02-07  
**الإصدار:** 1.0  
**المشروع:** Smart Rescuer - نظام الإنقاذ الذكي
