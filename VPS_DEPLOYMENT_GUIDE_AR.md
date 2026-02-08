# 🚀 دليل النشر الكامل على Hostinger VPS

## نظرة عامة
هذا الدليل يشرح كيفية نشر مشروع Smart Rescuer على Hostinger VPS بسرعة وبدون أخطاء.

---

## 📋 المتطلبات الأساسية

### على جهازك المحلي:
- ✅ مشروع Smart Rescuer 
- ✅ WinSCP أو FileZilla لنقل الملفات
- ✅ PuTTY أو Windows Terminal للـ SSH

### معلومات VPS:
- **IP Address**: `76.13.40.84`
- **Username**: `root` (أو اسم المستخدم الخاص بك)
- **Password**: كلمة المرور الخاصة بك
- **SSH Port**: `22` (الافتراضي)

---

## 🎯 خطوات النشر السريعة

### الخطوة 1: الاتصال بـ VPS عبر SSH

#### طريقة 1: استخدام PuTTY
```
1. افتح PuTTY
2. Host Name: 76.13.40.84
3. Port: 22
4. اضغط Open
5. أدخل username و password
```

#### طريقة 2: استخدام Windows Terminal/PowerShell
```powershell
ssh root@76.13.40.84
# أدخل كلمة المرور عندما يطلب منك
```

---

### الخطوة 2: نقل ملفات المشروع إلى VPS

#### طريقة 1: استخدام SCP (من PowerShell على جهازك)
```powershell
# انتقل إلى مجلد المشروع
cd "d:\ghaz tbee"

# انسخ جميع ملفات المشروع
scp -r smart-rescuer root@76.13.40.84:/var/www/
```

#### طريقة 2: استخدام WinSCP
```
1. افتح WinSCP
2. Host: 76.13.40.84
3. Username: root
4. Password: كلمة المرور
5. Port: 22
6. اتصل
7. انسخ مجلد smart-rescuer إلى /var/www/
```

---

### الخطوة 3: تشغيل سكريبت النشر التلقائي

بعد الاتصال بـ VPS عبر SSH:

```bash
# انتقل إلى مجلد المشروع
cd /var/www/smart-rescuer

# اجعل السكريبت قابل للتنفيذ
chmod +x vps-deploy-complete.sh

# شغّل السكريبت
./vps-deploy-complete.sh
```

**⏱️ المدة المتوقعة:** 15-20 دقيقة

السكريبت سيقوم تلقائياً بـ:
- ✅ تحديث النظام
- ✅ تثبيت Docker و Docker Compose
- ✅ إنشاء ملف .env
- ✅ بناء وتشغيل الـ Containers
- ✅ تثبيت مكتبات AI (TensorFlow, PyTorch)
- ✅ إعداد Firewall

---

### الخطوة 4: التحقق من التشغيل

#### 1. فحص حالة الخدمات:
```bash
cd /var/www/smart-rescuer
docker-compose ps
```

يجب أن ترى:
```
NAME                        STATUS              PORTS
smart-rescuer-backend       Up (healthy)        0.0.0.0:8000->8000/tcp
smart-rescuer-frontend      Up (healthy)        0.0.0.0:3000->80/tcp
smart-rescuer-nginx         Up                  0.0.0.0:80->80/tcp, 0.0.0.0:443->443/tcp
```

#### 2. اختبار الـ Backend API:
```bash
curl http://76.13.40.84:8000/health
```

النتيجة المتوقعة:
```json
{
  "status": "healthy",
  "ai_enabled": true,
  "version": "1.0.0"
}
```

#### 3. اختبار الـ Frontend:
افتح المتصفح وانتقل إلى:
```
http://76.13.40.84:3000
```

---

## 🤖 التحقق من تفعيل AI

### 1. فحص حالة AI:
```bash
# ادخل إلى الـ Backend Container
docker-compose exec backend bash

# اختبر TensorFlow
python -c "import tensorflow as tf; print(f'TensorFlow {tf.__version__} installed ✓')"

# اختبر PyTorch
python -c "import torch; print(f'PyTorch {torch.__version__} installed ✓')"

# اخرج من الـ Container
exit
```

### 2. عرض سجلات AI:
```bash
docker-compose logs backend | grep -i "ai\|model\|tensorflow"
```

يجب أن ترى:
```
✓ TensorFlow 2.15.0 loaded
✓ Injury detection model loaded
✓ AI engine initialized
```

---

## 📊 الأوامر المفيدة

### إدارة الخدمات:
```bash
# عرض السجلات المباشرة
docker-compose logs -f

# عرض سجلات خدمة معينة
docker-compose logs -f backend
docker-compose logs -f frontend

# فحص حالة الخدمات
docker-compose ps

# إعادة تشغيل الخدمات
docker-compose restart

# إيقاف الخدمات
docker-compose down

# بدء الخدمات
docker-compose up -d

# إعادة البناء والتشغيل
docker-compose down && docker-compose up -d --build
```

### مراقبة الموارد:
```bash
# عرض استخدام موارد الـ Containers
docker stats

# عرض مساحة القرص
df -h

# عرض استخدام الذاكرة
free -h
```

### إدارة الملفات:
```bash
# عرض التقارير المحفوظة
ls -lh /var/www/smart-rescuer/backend/reports/

# عرض الصور المرفوعة
ls -lh /var/www/smart-rescuer/backend/uploads/

# حذف الملفات القديمة (أكثر من 7 أيام)
find /var/www/smart-rescuer/backend/uploads/ -type f -mtime +7 -delete
```

---

## 🔧 حل المشاكل الشائعة

### المشكلة 1: الـ Backend لا يعمل
```bash
# فحص السجلات
docker-compose logs backend

# إعادة تشغيل
docker-compose restart backend

# إذا استمرت المشكلة، أعد البناء
docker-compose stop backend
docker-compose rm -f backend
docker-compose up -d --build backend
```

### المشكلة 2: AI غير مفعل
```bash
# ادخل إلى الـ Container
docker-compose exec backend bash

# أعد تثبيت TensorFlow
pip install --upgrade tensorflow-cpu==2.15.0

# أعد تشغيل
exit
docker-compose restart backend
```

### المشكلة 3: بطء في التحليل
```bash
# تحقق من الموارد
docker stats

# إذا كانت الذاكرة ممتلئة، أعد تشغيل
docker-compose restart

# قلل عدد الـ Workers
# عدّل في docker-compose.yml: WORKERS=2
```

### المشكلة 4: لا يمكن الوصول من المتصفح
```bash
# تحقق من الـ Firewall
sudo ufw status

# تأكد من فتح المنافذ
sudo ufw allow 8000/tcp
sudo ufw allow 3000/tcp
sudo ufw allow 80/tcp

# أعد تحميل الـ Firewall
sudo ufw reload
```

---

## 🔐 تحسينات الأمان (اختياري)

### 1. تغيير منفذ SSH:
```bash
# عدّل ملف SSH config
sudo nano /etc/ssh/sshd_config

# غيّر السطر:
# Port 22
# إلى:
# Port 2222

# أعد تشغيل SSH
sudo systemctl restart sshd

# تذكر تحديث الـ Firewall
sudo ufw allow 2222/tcp
sudo ufw delete allow 22/tcp
```

### 2. تعطيل تسجيل الدخول كـ Root:
```bash
# أنشئ مستخدم جديد أولاً
sudo adduser admin
sudo usermod -aG sudo admin
sudo usermod -aG docker admin

# عدّل SSH config
sudo nano /etc/ssh/sshd_config

# غيّر:
# PermitRootLogin yes
# إلى:
# PermitRootLogin no

# أعد تشغيل SSH
sudo systemctl restart sshd
```

### 3. إضافة SSL (HTTPS):
```bash
# تثبيت Certbot
sudo apt install certbot python3-certbot-nginx

# الحصول على شهادة SSL (يتطلب domain name)
sudo certbot --nginx -d yourdomain.com
```

---

## 📈 تحسين الأداء

### 1. تفعيل Log Rotation:
```bash
# إنشاء ملف إعدادات log rotation
sudo nano /etc/logrotate.d/smart-rescuer

# أضف:
/var/www/smart-rescuer/backend/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
}

# اختبر
sudo logrotate -d /etc/logrotate.d/smart-rescuer
```

### 2. إضافة Cron Job لتنظيف الملفات:
```bash
# افتح crontab
crontab -e

# أضف للتنظيف اليومي في الساعة 2 صباحاً:
0 2 * * * find /var/www/smart-rescuer/backend/uploads/ -type f -mtime +7 -delete
0 2 * * * find /var/www/smart-rescuer/backend/reports/ -type f -mtime +30 -delete
```

### 3. تفعيل Docker Log Limits:
```yaml
# أضف في docker-compose.yml لكل service:
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

---

## 🔄 التحديثات المستقبلية

عندما تريد تحديث المشروع:

```bash
# 1. انسخ الملفات الجديدة إلى VPS (باستخدام SCP أو WinSCP)

# 2. اتصل بـ VPS
ssh root@76.13.40.84

# 3. انتقل إلى المشروع
cd /var/www/smart-rescuer

# 4. أوقف الخدمات
docker-compose down

# 5. أعد البناء والتشغيل
docker-compose up -d --build

# 6. تحقق من السجلات
docker-compose logs -f
```

---

## 📞 الدعم والمساعدة

### روابط مفيدة:
- **Backend API**: http://76.13.40.84:8000
- **Frontend**: http://76.13.40.84:3000
- **API Docs**: http://76.13.40.84:8000/docs
- **Health Check**: http://76.13.40.84:8000/health

### ملفات مهمة:
- **السجلات**: `/var/www/smart-rescuer/`
- **Docker Compose**: `/var/www/smart-rescuer/docker-compose.yml`
- **البيئة**: `/var/www/smart-rescuer/.env`
- **Backend**: `/var/www/smart-rescuer/backend/`
- **Frontend**: `/var/www/smart-rescuer/frontend/`

---

## ✅ قائمة التحقق النهائية

- [ ] الاتصال بـ VPS عبر SSH يعمل
- [ ] تم نقل جميع ملفات المشروع
- [ ] تم تشغيل سكريبت النشر بنجاح
- [ ] جميع الـ Containers تعمل (healthy)
- [ ] الـ Backend API يستجيب على http://76.13.40.84:8000/health
- [ ] الـ Frontend يعمل على http://76.13.40.84:3000
- [ ] AI مفعل (TensorFlow و PyTorch مثبتان)
- [ ] يمكن رفع صورة وتحليلها بنجاح
- [ ] التقارير تُحفظ بشكل صحيح
- [ ] السرعة مقبولة (أقل من 15 ثانية للتحليل)

---

## 🎉 تم!

إذا اتبعت جميع الخطوات، مشروعك الآن يعمل على:
- **🌐 Frontend**: http://76.13.40.84:3000
- **🔌 Backend**: http://76.13.40.84:8000
- **🤖 AI**: مفعل وجاهز
- **⚡ الأداء**: محسّن للسرعة

**ملاحظة مهمة:** استبدل `root` باسم المستخدم الخاص بك إذا كان مختلفاً.

---

**Need help? تحتاج مساعدة؟**
راجع قسم حل المشاكل أعلاه أو تحقق من السجلات باستخدام `docker-compose logs -f`
