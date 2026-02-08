# 🚀 النشر باستخدام GitHub + VPS

## الفكرة
بدلاً من نسخ الملفات يدوياً، سنقوم بـ:
1. **GitHub**: سنرفع المشروع إلى مستودع خاص.
2. **VPS**: سنسحب النسخة من GitHub إلى الخادم.
3. **Deploy**: سنشغل سكريبت التثبيت الموجود داخل المشروع.

---

## الخطوة 1: رفع المشروع إلى GitHub

### المتطلبات:
1.  حساب في [GitHub.com](https://github.com/login).
2.  أنشئ **Repository** جديداً (New Repository)
    *   **Repository Name**: `smart-rescuer-vps`
    *   **Privacy**: Make it **Private** (خاص)
    *   لا تضف README أو .gitignore الآن (نحن أنشأناهم).

### على جهازك المحلي (Windows):

لقد قمت بإنشاء سكريبت لمساعدتك. افتح PowerShell كمسؤول (Run as Administrator):

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\github-setup.ps1
```

اتبع التعليمات:
1.  سيتم إنشاء Git Repo محلياً.
2.  سيطلب منك رابط الـ GitHub Repo الذي أنشأته (مثلاً: `https://github.com/yourusername/smart-rescuer.git`).
3.  سيقوم برفع الكود.

إذا واجهت مشاكل في تسجيل الدخول، استخدم [Git Credential Manager](https://github.com/git-ecosystem/git-credential-manager/blob/release/docs/install.md) أو SSH key.

---

## الخطوة 2: السحب والنشر على VPS

### 1. اتصل بـ VPS:
```bash
ssh root@76.13.40.84
# أدخل كلمة السر
```

### 2. تثبيت Git (إذا لم يكن مثبتاً):
```bash
apt update && apt install git -y
```

### 3. سحب المشروع (Clone):
```bash
cd /var/www
git clone https://github.com/yourusername/smart-rescuer-vps.git smart-rescuer
```
*(سيطلب منك Username و Password/Token)*

> **نصيحة أمنية**:
> استخدم **Personal Access Token (Classic)** بدلاً من كلمة السر لـ GitHub.
> [كيفية إنشاء Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic)

### 4. تشغيل سكريبت النشر:
```bash
cd smart-rescuer
chmod +x vps-deploy-complete.sh
./vps-deploy-complete.sh
```

---

## الخطوة 3: التحديثات المستقبلية

عندما تقوم بتعديل أي كود على جهازك:

### 1. ارفع التعديلات (Push):
```powershell
# على جهازك
git add .
git commit -m "تحديث جديد"
git push
```

### 2. اسحب التحديثات على VPS (Pull):
```bash
# على VPS
cd /var/www/smart-rescuer
git pull
./vps-deploy-complete.sh  # لإعادة بناء الـ Containers بالتعديلات الجديدة
```

---

## ملاحظة حول الملفات السرية (.env)

ملف `.env` يحتوي على أسرار ولا يتم رفعه إلى GitHub.
لحسن الحظ، السكريبت `vps-deploy-complete.sh` يقوم **بإنشاء ملف .env تلقائياً** على الـ VPS إذا لم يكن موجوداً، أو يمكنك استخدام `nano .env` لتعديله يدوياً على السيرفر.

---

**انتهى!** مشروعك الآن مربوط بـ GitHub ومرفوع على VPS. 🚀
