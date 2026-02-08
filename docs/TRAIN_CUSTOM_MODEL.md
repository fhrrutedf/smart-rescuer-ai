# دليل تدريب نموذج AI مخصص لكشف الإصابات

## 🎓 الخيار 2: تدريب نموذج من الصفر

---

## 📋 **نظرة عامة**

### ما سنفعله:
```
1. جمع البيانات (صور الإصابات)
2. تجهيز وتصنيف البيانات
3. تدريب النموذج
4. تحويل للـ TFLite (للـ Edge AI)
5. دمج مع المشروع
```

### المدة المتوقعة:
- 📊 **جمع البيانات**: 1-2 أسبوع
- 🏋️ **التدريب**: 2-6 ساعات (حسب الجهاز)
- ⚙️ **التحسين**: 1-3 أيام

---

## 1️⃣ **جمع البيانات (Dataset Collection)**

### ما نحتاجه:

#### الحد الأدنى:
```
📁 dataset/
├── bleeding/          # 200+ صورة نزيف
├── bruise/            # 200+ صورة كدمات
├── burn/              # 200+ صورة حروق
├── cut/               # 200+ صورة جروح
├── fracture/          # 200+ صورة كسور
├── swelling/          # 200+ صورة تورم
└── normal/            # 300+ صورة طبيعية (بدون إصابة)
```

#### الأفضل:
```
✅ 500-1000 صورة لكل فئة
✅ تنوع في:
   - الإضاءة (نهار، ليل، داخلي، خارجي)
   - الزوايا (قريب، بعيد، جانبي)
   - أنواع البشرة
   - شدة الإصابة
```

### 🔍 مصادر البيانات:

#### 1. Datasets طبية موجودة (مجانية):
```python
# مثال: Kaggle Datasets
- Wound Detection Dataset
- Medical Image Dataset
- Skin Lesion Dataset

# التحميل:
# https://www.kaggle.com/datasets
# https://github.com/topics/medical-imaging
```

#### 2. إنشاء بياناتك الخاصة:
```python
✅ التقط صور تدريبية (مع الإذن!)
✅ استخدم صور simulation/makeup للإصابات
✅ صور من الإنترنت (مع مراعاة الحقوق)
```

#### 3. Data Augmentation:
```python
# لزيادة عدد الصور من خلال التعديلات
- Rotation (تدوير)
- Flip (قلب)
- Brightness (سطوع)
- Zoom (تقريب)
- Noise (ضوضاء)

# النتيجة: 200 صورة → 1000+ صورة!
```

---

## 2️⃣ **تجهيز البيانات (Data Preparation)**

### سكريبت تجهيز البيانات:

```python
# scripts/prepare_dataset.py
import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# 1. قراءة البيانات
def load_dataset(data_dir):
    """تحميل الصور والتصنيفات"""
    images = []
    labels = []
    
    classes = ['normal', 'bleeding', 'bruise', 'burn', 'cut', 'fracture', 'swelling']
    
    for idx, class_name in enumerate(classes):
        class_dir = os.path.join(data_dir, class_name)
        
        for img_name in os.listdir(class_dir):
            img_path = os.path.join(class_dir, img_name)
            
            # قراءة الصورة
            img = cv2.imread(img_path)
            if img is None:
                continue
                
            # Resize to 224x224 (حجم قياسي)
            img = cv2.resize(img, (224, 224))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            images.append(img)
            labels.append(idx)
    
    return np.array(images), np.array(labels)

# 2. تقسيم البيانات
images, labels = load_dataset('dataset/')

# 80% تدريب، 20% اختبار
X_train, X_test, y_train, y_test = train_test_split(
    images, labels, 
    test_size=0.2, 
    random_state=42,
    stratify=labels  # توزيع متساوٍ
)

print(f"Training samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")

# 3. Data Augmentation
datagen = ImageDataGenerator(
    rotation_range=20,        # تدوير 20 درجة
    width_shift_range=0.2,    # إزاحة أفقية
    height_shift_range=0.2,   # إزاحة عمودية
    horizontal_flip=True,     # قلب أفقي
    zoom_range=0.2,          # تقريب
    brightness_range=[0.8, 1.2]  # تغيير السطوع
)

# 4. Normalization (تطبيع القيم)
X_train = X_train.astype('float32') / 255.0
X_test = X_test.astype('float32') / 255.0

print("✅ Data preparation complete!")
```

---

## 3️⃣ **بناء النموذج (Model Architecture)**

### الخيار 1: من الصفر (Custom CNN)

```python
# scripts/train_model.py
import tensorflow as tf
from tensorflow.keras import layers, models

def create_injury_model(num_classes=7):
    """بناء نموذج CNN مخصص"""
    
    model = models.Sequential([
        # Block 1
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Block 2
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Block 3
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Block 4
        layers.Conv2D(256, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.5),
        
        # Classification Head
        layers.Flatten(),
        layers.Dense(512, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    return model

# إنشاء النموذج
model = create_injury_model()
model.summary()  # عرض البنية

# Compile
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)
```

### الخيار 2: Transfer Learning (أسرع وأفضل!)

```python
# استخدام نموذج مُدرَّب مسبقاً
from tensorflow.keras.applications import MobileNetV2

def create_transfer_learning_model(num_classes=7):
    """استخدام MobileNetV2 مع Fine-tuning"""
    
    # تحميل MobileNetV2 (مُدرَّب على ImageNet)
    base_model = MobileNetV2(
        input_shape=(224, 224, 3),
        include_top=False,  # بدون طبقة التصنيف
        weights='imagenet'   # أوزان مُدرَّبة
    )
    
    # تجميد الطبقات الأولى (لا نعيد تدريبها)
    base_model.trainable = False
    
    # إضافة طبقات مخصصة
    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    return model

# إنشاء النموذج
model = create_transfer_learning_model()

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)
```

---

## 4️⃣ **التدريب (Training)**

```python
# التدريب الفعلي
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

# Callbacks للتحسين
callbacks = [
    # إيقاف مبكر إذا لم يتحسن
    EarlyStopping(
        monitor='val_accuracy',
        patience=10,
        restore_best_weights=True
    ),
    
    # حفظ أفضل نموذج
    ModelCheckpoint(
        'models/best_injury_model.h5',
        monitor='val_accuracy',
        save_best_only=True
    ),
    
    # تقليل learning rate
    ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=5
    )
]

# بدء التدريب
history = model.fit(
    datagen.flow(X_train, y_train, batch_size=32),
    validation_data=(X_test, y_test),
    epochs=50,  # عدد الدورات
    callbacks=callbacks,
    verbose=1
)

print("✅ Training complete!")

# حفظ النموذج
model.save('models/injury_detector_final.h5')
```

### 📊 مراقبة التدريب:

```python
import matplotlib.pyplot as plt

# رسم منحنيات التدريب
plt.figure(figsize=(12, 4))

# Accuracy
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Train')
plt.plot(history.history['val_accuracy'], label='Validation')
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

# Loss
plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Train')
plt.plot(history.history['val_loss'], label='Validation')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

plt.tight_layout()
plt.savefig('training_history.png')
print("✅ Training plots saved!")
```

---

## 5️⃣ **التقييم (Evaluation)**

```python
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns

# تقييم النموذج
y_pred = model.predict(X_test)
y_pred_classes = np.argmax(y_pred, axis=1)

# تقرير مفصل
classes = ['normal', 'bleeding', 'bruise', 'burn', 'cut', 'fracture', 'swelling']
print(classification_report(y_test, y_pred_classes, target_names=classes))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred_classes)
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=classes, yticklabels=classes)
plt.title('Confusion Matrix')
plt.ylabel('True Label')
plt.xlabel('Predicted Label')
plt.savefig('confusion_matrix.png')

print("✅ Evaluation complete!")
```

---

## 6️⃣ **التحويل لـ TFLite (للنشر على Edge)**

```python
# تحويل النموذج المُدرَّب لـ TensorFlow Lite
import tensorflow as tf

# تحميل النموذج
model = tf.keras.models.load_model('models/injury_detector_final.h5')

# إنشاء Converter
converter = tf.lite.TFLiteConverter.from_keras_model(model)

# تطبيق Optimizations (تقليل الحجم)
converter.optimizations = [tf.lite.Optimize.DEFAULT]

# Optional: Quantization (لتقليل الحجم أكثر)
converter.target_spec.supported_types = [tf.float16]

# التحويل
tflite_model = converter.convert()

# حفظ
output_path = 'backend/ai_engine/models/injury_detector.tflite'
with open(output_path, 'wb') as f:
    f.write(tflite_model)

# معلومات الملف
import os
file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
print(f"✅ TFLite model saved!")
print(f"📦 Size: {file_size:.2f} MB")
```

---

## 7️⃣ **الاختبار في المشروع**

```python
# اختبار النموذج الجديد
from backend.ai_engine.injury_detector import InjuryDetector

# إنشاء detector (سيحمل النموذج الجديد تلقائياً)
detector = InjuryDetector()

# اختبار على صورة
injuries = detector.detect_from_image('test_images/wound.jpg')

for injury in injuries:
    print(f"Type: {injury['type']}")
    print(f"Confidence: {injury['confidence']:.2%}")
    print(f"Severity: {injury['severity']}")
    print("---")
```

---

## 📊 **النتائج المتوقعة**

### بعد التدريب الناجح:

```
✅ Accuracy على Test Set: 85-95%
✅ Model Size: 5-15 MB (TFLite)
✅ Inference Time: 100-200ms per image
✅ يعمل Offline على Raspberry Pi
```

### Confusion Matrix مثالية:
```
              Precision  Recall  F1-Score
normal           0.95     0.97     0.96
bleeding         0.90     0.88     0.89
bruise           0.87     0.85     0.86
burn             0.92     0.90     0.91
cut              0.88     0.87     0.87
fracture         0.85     0.83     0.84
swelling         0.86     0.84     0.85
```

---

## 🚀 **سكريبت كامل جاهز للتشغيل**

```python
# scripts/train_injury_detector.py
"""
سكريبت كامل لتدريب نموذج كشف الإصابات
"""
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # تقليل الرسائل

import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
import cv2

print("🚀 Starting Injury Detection Model Training...")
print(f"TensorFlow version: {tf.__version__}")

# ====================
# 1. إعداد البيانات
# ====================
print("\n📊 Loading dataset...")

# تحميل الصور
def load_images_from_folder(folder, img_size=(224, 224)):
    images = []
    labels = []
    classes = sorted(os.listdir(folder))
    
    for idx, class_name in enumerate(classes):
        class_dir = os.path.join(folder, class_name)
        if not os.path.isdir(class_dir):
            continue
            
        print(f"  Loading {class_name}...")
        count = 0
        
        for img_name in os.listdir(class_dir):
            if not img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue
                
            img_path = os.path.join(class_dir, img_name)
            img = cv2.imread(img_path)
            
            if img is None:
                continue
                
            img = cv2.resize(img, img_size)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            images.append(img)
            labels.append(idx)
            count += 1
        
        print(f"    ✅ Loaded {count} images")
    
    return np.array(images), np.array(labels), classes

images, labels, class_names = load_images_from_folder('dataset/')
print(f"\n✅ Total images: {len(images)}")
print(f"📋 Classes: {class_names}")

# تقسيم البيانات
X_train, X_test, y_train, y_test = train_test_split(
    images, labels, test_size=0.2, random_state=42, stratify=labels
)

# Normalization
X_train = X_train.astype('float32') / 255.0
X_test = X_test.astype('float32') / 255.0

print(f"📈 Training set: {len(X_train)} samples")
print(f"📉 Test set: {len(X_test)} samples")

# ====================
# 2. Data Augmentation
# ====================
datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    zoom_range=0.2,
    brightness_range=[0.8, 1.2]
)

# ====================
# 3. بناء النموذج
# ====================
print("\n🏗️  Building model...")

base_model = MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights='imagenet'
)
base_model.trainable = False

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(len(class_names), activation='softmax')
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(0.001),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# ====================
# 4. التدريب
# ====================
print("\n🏋️  Training model...")

from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

callbacks = [
    EarlyStopping(monitor='val_accuracy', patience=10, restore_best_weights=True),
    ModelCheckpoint('models/best_model.h5', monitor='val_accuracy', save_best_only=True)
]

os.makedirs('models', exist_ok=True)

history = model.fit(
    datagen.flow(X_train, y_train, batch_size=32),
    validation_data=(X_test, y_test),
    epochs=30,
    callbacks=callbacks,
    verbose=1
)

# ====================
# 5. التقييم
# ====================
print("\n📊 Evaluating model...")

test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
print(f"✅ Test Accuracy: {test_acc:.2%}")
print(f"✅ Test Loss: {test_loss:.4f}")

# ====================
# 6. التحويل لـ TFLite
# ====================
print("\n📦 Converting to TFLite...")

converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()

tflite_path = 'backend/ai_engine/models/injury_detector.tflite'
os.makedirs(os.path.dirname(tflite_path), exist_ok=True)

with open(tflite_path, 'wb') as f:
    f.write(tflite_model)

file_size = os.path.getsize(tflite_path) / (1024 * 1024)
print(f"✅ TFLite model saved: {tflite_path}")
print(f"📦 Size: {file_size:.2f} MB")

# حفظ أسماء الفئات
with open('backend/ai_engine/models/class_names.txt', 'w') as f:
    f.write('\n'.join(class_names))

print("\n🎉 Training complete!")
print(f"📈 Final accuracy: {test_acc:.2%}")
print(f"📁 Model saved at: {tflite_path}")
```

---

## ⚡ **تشغيل التدريب**

```bash
# 1. ثبّت المكتبات
pip install tensorflow opencv-python scikit-learn matplotlib seaborn

# 2. جهّز البيانات في:
#    dataset/bleeding/
#    dataset/bruise/
#    ... إلخ

# 3. شغّل التدريب
python scripts/train_injury_detector.py

# 4. انتظر... (2-6 ساعات)

# 5. النموذج جاهز!
# ✅ backend/ai_engine/models/injury_detector.tflite
```

---

## ✅ **الخلاصة**

### ما تحتاجه:
```
1. 📊 بيانات (500+ صورة لكل فئة)
2. 💻 جهاز قوي أو Google Colab (مجاني!)
3. ⏱️ وقت (6-12 ساعة إجمالي)
4. 🧠 صبر وتجربة
```

### النتيجة:
```
✅ نموذج AI مخصص 100%
✅ دقة 85-95%
✅ يعمل Offline
✅ محسّن للـ Raspberry Pi
✅ احترافي لمشروع التخرج
```

---

**جاهز لبدء التدريب؟ 🚀**
