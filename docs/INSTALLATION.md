# دليل التثبيت اليدوي - المنقذ الذكي
## Manual Installation Guide

---

## 📋 المتطلبات الأساسية | Prerequisites

قبل البدء، تأكد من تثبيت:
- **Python 3.11 أو أحدث** - [تحميل من هنا](https://www.python.org/downloads/)
- **Node.js 20 أو أحدث** - [تحميل من هنا](https://nodejs.org/)
- **Git** (اختياري) - [تحميل من هنا](https://git-scm.com/)

---

## 🪟 التثبيت على Windows

### الخطوة 1️⃣: انتقل لمجلد المشروع

```powershell
cd "d:\ghaz tbee\smart-rescuer"
```

### الخطوة 2️⃣: إعداد Python Backend

```powershell
# الانتقال لمجلد backend
cd backend

# إنشاء البيئة الافتراضية
python -m venv venv

# تفعيل البيئة الافتراضية
.\venv\Scripts\Activate.ps1

# تحديث pip
python -m pip install --upgrade pip

# تثبيت المكتبات المطلوبة
pip install -r requirements.txt

# العودة للمجلد الرئيسي
cd ..
```

> **ملاحظة:** إذا واجهت مشكلة في تنفيذ السكريبت، قم بتشغيل:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### الخطوة 3️⃣: إعداد React Frontend

```powershell
# الانتقال لمجلد frontend
cd frontend

# تثبيت المكتبات
npm install

# العودة للمجلد الرئيسي
cd ..
```

### الخطوة 4️⃣: إعداد ملف الإعدادات

```powershell
# نسخ ملف الإعدادات المثالي
copy .env.example .env

# (اختياري) فتح الملف للتعديل
notepad .env
```

### الخطوة 5️⃣: تشغيل النظام

**الطريقة 1: باستخدام السكريبت (موصى به)**
```powershell
.\scripts\start.ps1
```

**الطريقة 2: يدوياً (نافذتين منفصلتين)**

**نافذة PowerShell الأولى - Backend:**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

**نافذة PowerShell الثانية - Frontend:**
```powershell
cd frontend
npm run dev
```

---

## 🐧 التثبيت على Linux / macOS

### الخطوة 1️⃣: انتقل لمجلد المشروع

```bash
cd /path/to/smart-rescuer
```

### الخطوة 2️⃣: إعداد Python Backend

```bash
# الانتقال لمجلد backend
cd backend

# إنشاء البيئة الافتراضية
python3 -m venv venv

# تفعيل البيئة الافتراضية
source venv/bin/activate

# تحديث pip
pip install --upgrade pip

# تثبيت المكتبات المطلوبة
pip install -r requirements.txt

# العودة للمجلد الرئيسي
cd ..
```

### الخطوة 3️⃣: إعداد React Frontend

```bash
# الانتقال لمجلد frontend
cd frontend

# تثبيت المكتبات
npm install

# العودة للمجلد الرئيسي
cd ..
```

### الخطوة 4️⃣: إعداد ملف الإعدادات

```bash
# نسخ ملف الإعدادات المثالي
cp .env.example .env

# (اختياري) فتح الملف للتعديل
nano .env
# أو
vim .env
```

### الخطوة 5️⃣: تشغيل النظام

**الطريقة 1: باستخدام السكريبت (موصى به)**
```bash
# إعطاء صلاحيات التنفيذ
chmod +x scripts/start.sh

# تشغيل
./scripts/start.sh
```

**الطريقة 2: يدوياً (نافذتي Terminal منفصلتين)**

**Terminal الأول - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal الثاني - Frontend:**
```bash
cd frontend
npm run dev
```

---

## 🍓 التثبيت على Raspberry Pi

### إعداد النظام

```bash
# تحديث النظام
sudo apt update && sudo apt upgrade -y

# تثبيت Python و dependencies
sudo apt install python3.11 python3-pip python3-venv -y
sudo apt install python3-opencv -y
sudo apt install libatlas-base-dev -y

# تثبيت Node.js
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install nodejs -y

# تثبيت Git (إذا لم يكن مثبتاً)
sudo apt install git -y
```

### تثبيت مكتبات الحساسات

```bash
# GPIO
sudo apt install python3-rpi.gpio -y

# I2C و SPI
sudo apt install python3-smbus python3-spidev -y

# تفعيل I2C و SPI
sudo raspi-config
# ثم اختر: Interface Options → I2C → Enable
# ثم: Interface Options → SPI → Enable
```

### تثبيت المشروع

```bash
# Clone أو نقل المشروع
cd /home/pi
# إذا كان على GitHub:
# git clone <repository-url> smart-rescuer

cd smart-rescuer

# إعداد Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..

# إعداد Frontend
cd frontend
npm install
cd ..

# تعديل الإعدادات لتفعيل الحساسات
cp .env.example .env
nano .env
```

### في ملف `.env` عدّل التالي:

```env
ENABLE_ECG_SENSOR=True
ENABLE_SPO2_SENSOR=True
ENABLE_TEMP_SENSOR=True
ENABLE_GPS=True
```

### تشغيل كخدمة (Service)

```bash
# إنشاء ملف service
sudo nano /etc/systemd/system/smart-rescuer.service
```

محتوى الملف:
```ini
[Unit]
Description=Smart Rescuer Emergency System
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/smart-rescuer
ExecStart=/home/pi/smart-rescuer/scripts/start.sh
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# تفعيل الخدمة
sudo systemctl daemon-reload
sudo systemctl enable smart-rescuer.service
sudo systemctl start smart-rescuer.service

# التحقق من الحالة
sudo systemctl status smart-rescuer.service
```

---

## ✅ التحقق من التثبيت

### 1️⃣ التحقق من Backend

```bash
# في متصفح الويب
http://localhost:8000

# يجب أن ترى رسالة JSON مع معلومات API
```

أو باستخدام curl:
```bash
curl http://localhost:8000/api/status
```

### 2️⃣ التحقق من Frontend

```bash
# في متصفح الويب
http://localhost:3000

# يجب أن ترى الصفحة الرئيسية للمنقذ الذكي
```

### 3️⃣ التحقق من الحساسات

```bash
curl http://localhost:8000/api/sensors/vitals
```

---

## 🔧 حل المشاكل الشائعة

### ❌ خطأ: "python: command not found"

**Windows:**
```powershell
# تأكد من إضافة Python للـ PATH
# أو استخدم:
python3 -m venv venv
```

**Linux/Mac:**
```bash
# استخدم python3 بدلاً من python
python3 -m venv venv
```

### ❌ خطأ: "pip: command not found"

```bash
# Windows
python -m pip install --upgrade pip

# Linux/Mac
python3 -m pip install --upgrade pip
```

### ❌ خطأ: "npm: command not found"

تأكد من تثبيت Node.js من [nodejs.org](https://nodejs.org/)

### ❌ خطأ: "Port 8000 already in use"

```bash
# Windows: إيقاف العملية
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### ❌ خطأ: "ModuleNotFoundError"

```bash
# تأكد من تفعيل البيئة الافتراضية
# Windows:
.\venv\Scripts\Activate.ps1

# Linux/Mac:
source venv/bin/activate

# ثم أعد تثبيت المكتبات
pip install -r requirements.txt
```

### ❌ Frontend لا يتصل بالـ Backend

تأكد من:
1. Backend يعمل على `http://localhost:8000`
2. في ملف `frontend/vite.config.js` الـ proxy مضبوط صحيح
3. لا يوجد Firewall يمنع الاتصال

---

## 📦 المكتبات المطلوبة

### Backend (Python)

المكتبات الأساسية:
```bash
fastapi==0.109.0
uvicorn[standard]==0.25.0
pydantic==2.5.3
python-multipart==0.0.6
```

للذكاء الاصطناعي:
```bash
tensorflow==2.15.0
opencv-python==4.8.1.78
numpy==1.24.3
```

للحساسات (Raspberry Pi):
```bash
RPi.GPIO
adafruit-circuitpython-max30100
pyserial
```

### Frontend (Node.js)

```bash
react
react-dom
react-router-dom
@mui/material
@mui/icons-material
axios
```

---

## 🚀 الخطوات التالية

بعد التثبيت الناجح:

1. **جرّب نظام الطوارئ**
   - اذهب إلى `http://localhost:3000/emergency`
   - جرب التقييم الطارئ

2. **استكشف API**
   - اذهب إلى `http://localhost:8000/docs`
   - جرب الـ endpoints المختلفة

3. **طوّر المشروع**
   - أضف نماذج AI حقيقية
   - دمج مع نظام الطوارئ الحقيقي
   - أضف المزيد من الميزات

---

## 📞 الدعم

إذا واجهت أي مشاكل:
1. راجع هذا الدليل
2. راجع `README.md`
3. راجع `docs/QUICKSTART.md`
4. تواصل مع فريق التطوير

---

**تم بناؤه بـ ❤️ لإنقاذ الأرواح**
