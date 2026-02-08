# 🚀 نشر سريع على VPS - Quick VPS Deployment

## ⚡ البدء السريع (3 خطوات فقط!)

### 1️⃣ على Windows (جهازك)
```powershell
cd "d:\ghaz tbee\smart-rescuer"
.\setup-vps.ps1
```

### 2️⃣ نسخ المشروع إلى VPS
```powershell
scp -r . root@76.13.40.84:/var/www/smart-rescuer
```

### 3️⃣ على VPS (عبر SSH)
```bash
ssh root@76.13.40.84
cd /var/www/smart-rescuer
chmod +x vps-deploy-complete.sh
./vps-deploy-complete.sh
```

## ✅ انتهى!

بعد التشغيل، المشروع سيعمل على:
- **Frontend**: http://76.13.40.84:3000
- **Backend API**: http://76.13.40.84:8000
- **Health Check**: http://76.13.40.84:8000/health

---

## 📁 الملفات المهمة

| الملف | الوصف |
|-------|-------|
| `setup-vps.ps1` | سكريبت Windows لإعداد الإعدادات |
| `vps-deploy-complete.sh` | سكريبت النشر الكامل على VPS |
| `VPS_DEPLOYMENT_GUIDE_AR.md` | دليل شامل بالعربية |
| `.env.vps` | إعدادات VPS |
| `docker-compose.yml` | تكوين Docker |
| `backend/requirements-production.txt` | مكتبات Python كاملة |

---

## 🤖 تفعيل AI

AI مفعّل افتراضياً! السكريبت سيثبت:
- ✅ TensorFlow 2.15.0 (CPU)
- ✅ PyTorch 2.1.0 (CPU)  
- ✅ OpenCV
- ✅ جميع مكتبات المعالجة

---

## ⚡ المميزات

- ✅ **تثبيت تلقائي**: Docker, Docker Compose, مكتبات AI
- ✅ **سرعة محسّنة**: Workers متعددة، timeout طويل
- ✅ **أمان**: Firewall تلقائي، CORS محدد
- ✅ **مراقبة**: Health checks، logs
- ✅ **سهولة**: سكريبت واحد فقط!

---

## 🔧 الأوامر الأساسية

### على VPS:
```bash
# عرض حالة الخدمات
docker-compose ps

# عرض السجلات
docker-compose logs -f

# إعادة تشغيل
docker-compose restart

# إيقاف
docker-compose down

# بدء
docker-compose up -d
```

---

## 🆘 حل المشاكل

### 1. لا يمكن الاتصال بـ VPS
```powershell
# اختبر الاتصال
ping 76.13.40.84

# جرّب SSH مع verbose
ssh -v root@76.13.40.84
```

### 2. AI غير مفعل
```bash
# ادخل إلى الـ container
docker-compose exec backend bash

# اختبر TensorFlow
python -c "import tensorflow as tf; print(tf.__version__)"

# أعد التثبيت
pip install --upgrade tensorflow-cpu==2.15.0

# اخرج وأعد التشغيل
exit
docker-compose restart backend
```

### 3. بطء في الأداء
```bash
# فحص الموارد
docker stats

# تقليل الـ workers (في docker-compose.yml)
# WORKERS=2

# إعادة بناء
docker-compose down
docker-compose up -d --build
```

---

## 📊 معلومات النظام

| المكون | القيمة |
|--------|--------|
| VPS IP | 76.13.40.84 |
| API Port | 8000 |
| Frontend Port | 3000 |
| AI | ✅ مفعّل |
| Workers | 4 |
| Timeout | 180s |
| Max Upload | 10MB |

---

## 📖 مزيد من المعلومات

اقرأ الدليل الشامل: **VPS_DEPLOYMENT_GUIDE_AR.md**

---

## ✨ نصائح للسرعة

1. ✅ AI مفعّل بـ CPU optimized
2. ✅ Workers متعددة (4)
3. ✅ Timeout طويل (180s)
4. ✅ Caching محسّن
5. ✅ Gzip compression مفعّل

---

## 🎉 نجاح النشر

إذا رأيت هذا:
```json
{
  "status": "healthy",
  "ai_enabled": true
}
```

**تهانينا!** 🎊 المشروع يعمل بنجاح!

---

**Need Help? تحتاج مساعدة؟**  
راجع `VPS_DEPLOYMENT_GUIDE_AR.md` للدليل الكامل
