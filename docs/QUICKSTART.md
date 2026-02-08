# Smart Rescuer - دليل التشغيل السريع

## 📋 المتطلبات الأساسية

قبل البدء، تأكد من تثبيت:
- **Python 3.11+** - [تحميل](https://www.python.org/downloads/)
- **Node.js 20+** - [تحميل](https://nodejs.org/)
- **Git** (اختياري)

## 🚀 التشغيل السريع

### Windows:
```powershell
# 1. إنشاء البيئة الافتراضية وتثبيت المكتبات
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

cd ..\frontend
npm install

# 2. تشغيل النظام
cd ..
.\scripts\start.ps1
```

### Linux/Mac:
```bash
# 1. إنشاء البيئة الافتراضية وتثبيت المكتبات
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cd ../frontend
npm install

# 2. تشغيل النظام
cd ..
chmod +x scripts/start.sh
./scripts/start.sh
```

## 🌐 الوصول للتطبيق

بعد التشغيل، يمكنك الوصول إلى:

- **الواجهة الرئيسية**: [http://localhost:3000](http://localhost:3000)
- **API Backend**: [http://localhost:8000](http://localhost:8000)
- **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)

## 🔧 الإعدادات

### ملف `.env`
انسخ `.env.example` إلى `.env` وعدّل الإعدادات حسب الحاجة:

```bash
cp .env.example .env
```

### تفعيل الحساسات (Raspberry Pi فقط)
في ملف `.env`:
```
ENABLE_ECG_SENSOR=True
ENABLE_SPO2_SENSOR=True
ENABLE_TEMP_SENSOR=True
ENABLE_GPS=True
```

> **ملاحظة**: على أجهزة التطوير العادية، الحساسات تعمل في وضع المحاكاة (Simulation Mode) تلقائياً.

## 📱 الاستخدام

### 1. نظام إنقاذ الحياة
- اذهب إلى صفحة "طوارئ"
- اختر صورة للإصابة (اختياري)
- اضغط "ابدأ التقييم الطارئ"
- شاهد النتائج والتوصيات

### 2. الاستشارة الذكية
- اذهب إلى صفحة "الدردشة"
- اكتب الأعراض
- احصل على توجيهات طبية

## 🧪 الاختبار

```bash
cd backend
pytest tests/
```

## 📚 الوثائق الكاملة

راجع المجلد `docs/` للمزيد من التفاصيل:
- `setup.md` - دليل التثبيت التفصيلي
- `api_reference.md` - مرجع API كامل
- `user_manual.md` - دليل المستخدم

## ⚠️ المشاكل الشائعة

### Backend لا يعمل
```bash
# تأكد من تفعيل البيئة الافتراضية
source venv/bin/activate  # Linux/Mac
# أو
.\venv\Scripts\Activate.ps1  # Windows

# تأكد من تثبيت المكتبات
pip install -r requirements.txt
```

### Frontend لا يعمل
```bash
cd frontend
npm install
npm run dev
```

### Port مستخدم
غيّر البورت في الملفات:
- Backend: `config.py` → `API_PORT`
- Frontend: `vite.config.js` → `server.port`

## 💡 نصائح

1. **للتطوير**: استخدم وضع Debug بتعديل `.env`:
   ```
   DEBUG=True
   ```

2. **للنشر الإنتاجي**: 
   - غيّر `SECRET_KEY` في `.env`
   - عطّل `DEBUG=False`
   - استخدم `npm run build` للـ frontend

3. **على Raspberry Pi**:
   - فعّل الحساسات في `.env`
   - ثبّت المكتبات الإضافية:
     ```bash
     sudo apt-get install python3-rpi.gpio
     pip install adafruit-circuitpython-max30100
     ```

## 📞 الدعم

للمساعدة أو الإبلاغ عن مشاكل، راجع التوثيق أو تواصل مع فريق التطوير.

---

**تم بناؤه بـ ❤️ لإنقاذ الأرواح**
