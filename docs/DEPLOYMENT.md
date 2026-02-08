# دليل النشر على VPS - Smart Rescuer Deployment Guide

## المتطلبات الأساسية | Prerequisites

### VPS Requirements
- Ubuntu 20.04+ / Debian 11+ / CentOS 8+
- 2GB RAM minimum (4GB recommended)
- 20GB disk space
- Public IP address
- Domain name (للحصول على شهادة SSL)

### Software Required
- Docker & Docker Compose
- Git

---

## 1️⃣ إعداد VPS | VPS Setup

### تسجيل الدخول للخادم
```bash
ssh root@your-vps-ip
```

### تحديث النظام
```bash
apt update && apt upgrade -y
```

### تثبيت Docker
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Verify installation
docker --version
docker-compose --version
```

### تثبيت Git
```bash
apt install git -y
```

---

## 2️⃣ ربط النطاق (Domain) | Domain Configuration

### إعداد DNS Records
في لوحة تحكم النطاق، أضف:

```
Type    Name    Value           TTL
A       @       your-vps-ip     3600
A       www     your-vps-ip     3600
```

### التحقق من DNS
```bash
ping yourdomain.com
```

---

## 3️⃣ تحميل المشروع | Clone Project

```bash
cd /opt
git clone https://github.com/your-username/smart-rescuer.git
cd smart-rescuer
```

---

## 4️⃣ إعداد المتغيرات | Environment Configuration

### تعديل docker-compose.yml
```bash
nano docker-compose.yml
```

غيّر:
- `your-email@example.com` → بريدك الإلكتروني
- `yourdomain.com` → نطاقك

### تعديل nginx.conf
```bash
nano nginx/nginx.conf
```

غيّر جميع `yourdomain.com` → نطاقك

### إعداد Frontend API URL
```bash
nano frontend/src/services/api.js
```

غيّر:
```javascript
const API_BASE_URL = 'https://yourdomain.com/api';
```

---

## 5️⃣ الحصول على شهادة SSL (HTTPS) | Get SSL Certificate

⚠️ **مهم جداً**: الكاميرا لا تعمل بدون HTTPS!

### الطريقة التلقائية باستخدام Let's Encrypt:

```bash
# 1. بدء الخدمات المؤقتة
docker-compose up -d nginx

# 2. الحصول على الشهادة
docker-compose run --rm certbot

# 3. إعادة تشغيل nginx
docker-compose restart nginx
```

### تجديد الشهادة تلقائياً
```bash
# إضافة cron job للتجديد التلقائي
crontab -e

# أضف هذا السطر:
0 0 1 * * docker-compose run --rm certbot renew && docker-compose restart nginx
```

---

## 6️⃣ تشغيل التطبيق | Run Application

### بناء وتشغيل الحاويات
```bash
docker-compose up -d --build
```

### التحقق من الحالة
```bash
docker-compose ps
docker-compose logs -f
```

يجب أن ترى:
- ✅ backend: running
- ✅ frontend: running
- ✅ nginx: running

---

## 7️⃣ الوصول للتطبيق | Access Application

افتح المتصفح:
```
https://yourdomain.com
```

### API Documentation
```
https://yourdomain.com/docs
```

---

## 8️⃣ اختبار الكاميرا | Test Camera

1. افتح صفحة الطوارئ: `https://yourdomain.com/emergency`
2. اضغط "🎥 بدء المراقبة والتحليل المباشر"
3. اسمح للمتصفح بالوصول للكاميرا
4. يجب أن تعمل المراقبة المباشرة!

---

## 9️⃣ الإدارة والصيانة | Management

### عرض السجلات
```bash
# كل الخدمات
docker-compose logs -f

# خدمة معينة
docker-compose logs -f backend
docker-compose logs -f frontend
```

### إعادة التشغيل
```bash
docker-compose restart
```

### إيقاف التطبيق
```bash
docker-compose down
```

### تحديث التطبيق
```bash
git pull
docker-compose up -d --build
```

### تنظيف الموارد
```bash
docker system prune -a
```

---

## 🔒 الأمان | Security

### Firewall Configuration
```bash
# السماح فقط بالمنافذ الضرورية
ufw allow 22/tcp      # SSH
ufw allow 80/tcp      # HTTP
ufw allow 443/tcp     # HTTPS
ufw enable
```

### تغيير منفذ SSH (اختياري)
```bash
nano /etc/ssh/sshd_config
# غيّر: Port 22 → Port 2222
systemctl restart sshd

# لا تنسَ تحديث firewall:
ufw allow 2222/tcp
ufw delete allow 22/tcp
```

---

## 📊 المراقبة | Monitoring

### استخدام الموارد
```bash
docker stats
```

### حجم القرص
```bash
df -h
du -sh /opt/smart-rescuer/*
```

---

## ❌ حل المشاكل | Troubleshooting

### الكاميرا لا تعمل
✅ **تأكد من**:
1. الموقع يعمل على HTTPS
2. المتصفح يدعم `getUserMedia`
3. الإذن ممنوح للكاميرا

```bash
# تحقق من SSL
curl -I https://yourdomain.com
```

### Backend لا يستجيب
```bash
docker-compose logs backend
docker-compose restart backend
```

### Frontend صفحة بيضاء
```bash
docker-compose logs frontend

# تحقق من الـ build
docker-compose exec frontend ls /usr/share/nginx/html
```

### خطأ 502 Bad Gateway
```bash
# تحقق من الخدمات
docker-compose ps

# إعادة تشغيل nginx
docker-compose restart nginx
```

---

## 🚀 التحسين للإنتاج | Production Optimization

### تفعيل Redis للـ Caching (اختياري)
```yaml
# أضف في docker-compose.yml
redis:
  image: redis:alpine
  container_name: smart-rescuer-redis
  restart: unless-stopped
```

### Database للتقارير (اختياري)
```yaml
postgres:
  image: postgres:15-alpine
  environment:
    POSTGRES_DB: smart_rescuer
    POSTGRES_USER: rescuer
    POSTGRES_PASSWORD: your-secure-password
  volumes:
    - postgres-data:/var/lib/postgresql/data
```

---

## 📱 اختبار على الموبايل | Mobile Testing

1. افتح `https://yourdomain.com` على الموبايل
2. جرب المراقبة المباشرة - ستستخدم الكاميرا الخلفية تلقائياً
3. تأكد من سرعة الاستجابة

---

## 🎯 الخلاصة | Summary

✅ **تم إعداد**:
- ✅ Docker containers
- ✅ HTTPS with Let's Encrypt
- ✅ Nginx reverse proxy
- ✅ Auto SSL renewal
- ✅ Camera access working
- ✅ Real-time video monitoring

**الموقع الآن جاهز للاستخدام على**: `https://yourdomain.com`

---

## 📞 الدعم | Support

للمساعدة أو الأسئلة، راجع:
- Documentation: `/docs`
- Logs: `docker-compose logs`
- GitHub Issues

---

**تم! المشروع الآن يعمل على VPS مع دعم كامل للمراقبة المباشرة! 🎉**
