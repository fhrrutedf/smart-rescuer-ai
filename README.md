# المنقذ الذكي (Smart Rescuer) 🚑

<div align="center">

![Smart Rescuer](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Version](https://img.shields.io/badge/Version-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.11+-yellow)
![React](https://img.shields.io/badge/React-18+-61DAFB)
![License](https://img.shields.io/badge/License-MIT-green)

**نظام ذكاء اصطناعي طبي للطوارئ مع مراقبة مباشرة**

[التثبيت المحلي](#-التثبيت-المحلي) • [النشر على VPS](#-النشر-على-vps) • [الميزات](#-المميزات) • [API Docs](#-api-documentation)

</div>

---

## 🌟 نظرة عامة

المنقذ الذكي هو نظام طبي متقدم يستخدم **الذكاء الاصطناعي الطرفي** (Edge AI) لتقييم الحالات الطارئة في الوقت الفعلي. يدعم **المراقبة المباشرة بالفيديو** مع تحليل فوري للإصابات.

### 🎯 الميزات الرئيسية

#### 🎥 **المراقبة المباشرة (NEW!)**
- ✅ تحليل فيديو لحظي كل 3 ثوانِ
- ✅ عرض النتائج على الشاشة مباشرة
- ✅ كشف الإصابات تلقائياً
- ✅ دعم الكاميرا الأمامية والخلفية

#### 🚑 **نظام إنقاذ الحياة**
- تقييم فوري للحالات الطارئة
- دمج بيانات الحساسات الحيوية
- كشف الإصابات بالرؤية الحاسوبية
- تقييم مستوى الخطورة التلقائي
- توليد تقارير EMS احترافية

#### 🤖 **نظام الاستشارة الذكية**
- روبوت محلي للاستشارات الطبية
- يعمل بدون إنترنت
- استجابة فورية

#### 📊 **الحساسات الذكية**
- ECG - رسم القلب
- SpO2 - نسبة الأكسجين
- درجة الحرارة
- GPS - تحديد الموقع

---

## 🛠 البنية التقنية

```
smart-rescuer/
├── backend/              # Python Backend (FastAPI)
│   ├── api/             # REST API endpoints
│   ├── ai_engine/       # AI models & inference
│   ├── sensors/         # Hardware interfaces
│   ├── core/            # Business logic
│   └── utils/           # Utilities
├── frontend/            # React + Material-UI
│   ├── src/
│   │   ├── pages/       # Pages (Home, Emergency)
│   │   ├── services/    # API services
│   │   └── components/  # Reusable components
│   └── Dockerfile       # Production build
├── nginx/               # Reverse proxy config
├── docs/                # Documentation
│   ├── INSTALLATION.md  # تثبيت محلي
│   └── DEPLOYMENT.md    # نشر على VPS
└── docker-compose.yml   # Production deployment
```

---

## 💻 التثبيت المحلي

### المتطلبات
- Python 3.11+
- Node.js 18+
- Git

### الخطوات

#### 1️⃣ تحميل المشروع
```bash
git clone https://github.com/your-repo/smart-rescuer.git
cd smart-rescuer
```

#### 2️⃣ Backend Setup
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

#### 3️⃣ Frontend Setup
```bash
cd frontend
npm install
```

#### 4️⃣ تشغيل النظام

**Terminal 1 - Backend:**
```bash
cd backend
.\venv\Scripts\activate  # Windows
python -m uvicorn backend.api.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

#### 5️⃣ الوصول للتطبيق
- 🌐 **Frontend**: http://localhost:3000
- 📡 **Backend API**: http://localhost:8000
- 📚 **API Docs**: http://localhost:8000/docs

---

## 🚀 النشر على VPS

### ⚡ النشر السريع (موصى به)

```bash
# 1. تسجيل الدخول للـ VPS
ssh root@your-vps-ip

# 2. تحميل المشروع
git clone https://github.com/your-repo/smart-rescuer.git
cd smart-rescuer

# 3. تشغيل سكريبت النشر التلقائي
chmod +x deploy.sh
sudo ./deploy.sh
```

السكريبت سيقوم تلقائياً بـ:
- ✅ تثبيت Docker & Docker Compose
- ✅ إعداد Nginx
- ✅ الحصول على شهادة SSL (HTTPS)
- ✅ بناء وتشغيل الحاويات
- ✅ تفعيل التجديد التلقائي للـ SSL

### 📖 النشر اليدوي

للحصول على دليل مفصل خطوة بخطوة، راجع:  
👉 **[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)**

### 🔒 متطلبات HTTPS للكاميرا

⚠️ **مهم جداً**: ميزة الكاميرا والمراقبة المباشرة **تتطلب HTTPS** للعمل على الإنترنت!

السكريبت التلقائي يوفر:
- ✅ شهادة SSL مجانية من Let's Encrypt
- ✅ تجديد تلقائي كل 90 يوم
- ✅ إعادة توجيه HTTP → HTTPS تلقائياً

---

## 📱 استخدام المراقبة المباشرة

### على الكمبيوتر:
1. افتح: `https://yourdomain.com/emergency`
2. اضغط **"🎥 بدء المراقبة والتحليل المباشر"**
3. اسمح بالوصول للكاميرا
4. شاهد التحليل الفوري!

###على الموبايل:
- تستخدم الكاميرا الخلفية تلقائياً
- التحليل كل 3 ثوانٍ
- النتائج تظهر على الشاشة مباشرة

---

## 🔧 الإدارة والصيانةعلى VPS

### عرض السجلات
```bash
docker-compose logs -f
docker-compose logs -f backend
docker-compose logs -f frontend
```

### إعادة التشغيل
```bash
docker-compose restart
```

### إيقاف الخدمات
```bash
docker-compose down
```

### تحديث التطبيق
```bash
git pull
docker-compose up -d --build
```

---

## 📊 API Documentation

### Endpoints

#### 🏥 نظام الطوارئ
```http
POST /api/emergency/assess
Content-Type: multipart/form-data

{
  "patient_conscious": true,
  "image": <file>
}
```

#### 💬 Chatbot
```http
POST /api/chat
Content-Type: application/json

{
  "message": "ما هي أعراض الجفاف؟",
  "reset_history": false
}
```

#### 📍 الموقع
```http
GET /api/location
```

#### 📈 العلامات الحيوية
```http
GET /api/sensors/vitals
```

للوصول للوثائق التفاعلية الكاملة:  
👉 `https://yourdomain.com/docs`

---

## 🎓 التوثيق الكامل

- 📘 [دليل التثبيت المحلي](docs/INSTALLATION.md)
- 🚀 [دليل النشر على VPS](docs/DEPLOYMENT.md)
- 📝 [Walkthrough التطوير](walkthrough.md)
- ✅ [قائمة المهام](task.md)

---

## 🧪 التطوير

### تشغيل الاختبارات
```bash
cd backend
pytest tests/ -v
```

### فحص جودة الكود
```bash
# Python
black backend/
flake8 backend/

# JavaScript
cd frontend
npm run lint
```

---

## 🔐 الأمان

- ✅ HTTPS إلزامي للإنتاج
- ✅ Rate limiting على API
- ✅ CORS محمي
- ✅ Input validation
- ✅ Security headers
- ✅ SSL/TLS 1.2+

---

## 🤝 المساهمة

هذا مشروع أكاديمي. للمساهمة:
1. Fork المشروع
2. أنشئ branch جديد
3. Commit التغييرات
4. Push وافتح Pull Request

---

## 📄 الترخيص

MIT License - مشروع أكاديمي للأغراض التعليمية

---

## 👥 الفريق

مشروع تخرج - قسم الهندسة الطبية الحيوية

---

## 📞 الدعم

- 📧 Email: support@smartrescuer.com
- 📚 Documentation: `/docs`
- 🐛 Issues: GitHub Issues

---

<div align="center">

**⭐ إذا أعجبك المشروع، لا تنسَ النجمة! ⭐**

Made with ❤️ for saving lives

</div>
