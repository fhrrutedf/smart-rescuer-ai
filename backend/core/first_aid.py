"""
First Aid Instructions Generator
مولد إرشادات الإسعافات الأولية
"""
from typing import List, Dict, Any


class FirstAidInstructions:
    """توليد إرشادات الإسعافات الأولية حسب الحالة"""
    
    # قاعدة بيانات الإسعافات الأولية
    INSTRUCTIONS_DB = {
        'bleeding': {
            'ar_title': 'نزيف',
            'en_title': 'Bleeding',
            'severity': 'high',
            'steps': [
                "1. اضغط مباشرة على الجرح بقطعة قماش نظيفة",
                "2. ارفع المنطقة المصابة فوق مستوى القلب إن أمكن",
                "3. حافظ على الضغط المستمر لمد 10-15 دقيقة",
                "4. لا تزل الضمادة إذا تشبعت بالدم، أضف المزيد فوقها",
                "5. اطلب المساعدة الطبية فوراً"
            ],
            'warnings': [
                "⚠️ لا تزيل أي جسم ع الق في الجرح",
                "⚠️ لا تستخدم العاصبة إلا في الحالات القصوى",
                "⚠️ راقب علامات الصدمة"
            ]
        },
        'burn': {
            'ar_title': 'حروق',
            'en_title': 'Burns',
            'severity': 'high',
            'steps': [
                "1. أبعد المصاب عن مصدر الحريق",
                "2. اغسل المنطقة المحروقة بماء بارد جاري لمدة 10-20 دقيقة",
                "3. غطِ الحرق بضمادة نظيفة غير لاصقة",
                "4. لا تضع ثلج مباشرة على الحرق",
                "5. ارفع المنطقة المصابة إن أمكن"
            ],
            'warnings': [
                "⚠️ لا تفتح البثور",
                "⚠️ لا تضع معجون أسنان أو زيت",
                "⚠️ اطلب الطوارئ للحروق الكبيرة"
            ]
        },
        'fracture': {
            'ar_title': 'كسر',
            'en_title': 'Fracture',
            'severity': 'high',
            'steps': [
                "1. لا تحرك المصاب إلا للضرورة القصوى",
                "2. ثبت المنطقة المصابة في وضعها الحالي",
                "3. ضع جبيرة مؤقتة باستخدام أي مادة صلبة",
                "4. ضع قطع قماش بين الجبيرة والجلد",
                "5. ثبت الجبيرة بلطف فوق وتحت منطقة الكسر"
            ],
            'warnings': [
                "⚠️ لا تحاول إرجاع العظم لمكانه",
                " لا تحرك المصاب إذا كان الكسر في العمود الفقري",
                "⚠️ راقب الدورة الدموية في الأطراف"
            ]
        },
        'unconscious': {
            'ar_title': 'فقدان وعي',
            'en_title': 'Unconsciousness',
            'severity': 'critical',
            'steps': [
                "1. تحقق من التنفس والنبض",
                "2. ضع المصاب في وضعية الإفاقة إذا كان يتنفس",
                "3. ابدأ CPR إذا لم يكن يتنفس",
                "4. افتح مجرى التنفس (رأس للخلف، ذقن للأعلى)",
                "5. اتصل بالطوارئ فوراً"
            ],
            'warnings': [
                "⚠️ لا تترك المصاب وحده",
                "⚠️ لا تعطه أي شيء عن طريق الفم",
                "⚠️ راقب التنفس باستمرار"
            ]
        },
        'choking': {
            'ar_title': 'اختناق',
            'en_title': 'Choking',
            'severity': 'critical',
            'steps': [
                "1. شجع المصاب على السعال بقوة",
                "2. إذا لم يستطع السعال، قف خلفه",
                "3. اعمل 5 ضربات على الظهر بين الكتفين",
                "4. ثم اعمل 5 ضغطات بطنية (مناورة هايمليك)",
                "5. كرر حتى يخرج الجسم الغريب"
            ],
            'warnings': [
                "⚠️ لا تبحث عن الجسم الغريب بأصابعك إلا إذا رأيته",
                "⚠️ للرضع: استخدم تقنية مختلفة",
                "⚠️ اتصل بالطوارئ فوراً"
            ]
        },
        'heart_attack': {
            'ar_title': 'نوبة قلبية',
            'en_title': 'Heart Attack',
            'severity': 'critical',
            'steps': [
                "1. اتصل بالطوارئ فوراً",
                "2. اجعل المصاب يجلس ويرتاح",
                "3. فك أي ملابس ضيقة",
                "4. أعطه أسبرين (إذا لم يكن لديه حساسية)",
                "5. ابق معه حتى تصل المساعدة"
            ],
            'warnings': [
                "⚠️ لا تدعه يقود السيارة",
                "⚠️ استعد لعمل CPR إذا توقف القلب",
                "⚠️ لا تعطه أي شيء للشرب"
            ]
        },
        'shock': {
            'ar_title': 'صدمة',
            'en_title': 'Shock',
            'severity': 'critical',
            'steps': [
                "1. اجعل المصاب يستلقي على ظهره",
                "2. ارفع قدميه 30 سم إن أمكن",
                "3. غطه ببطانية لإبقائه دافئاً",
                "4. لا تعطه أي شيء عن طريق الفم",
                "5. اطلب المساعدة الطبية فوراً"
            ],
            'warnings': [
                "⚠️ لا ترفع الرأس",
                "⚠️ راقب التنفس والنبض",
                "⚠️ لا تحرك المصاب إذا كان هناك إصابة في الرقبة"
            ]
        },
        'low_oxygen': {
            'ar_title': 'نقص أكسجين',
            'en_title': 'Low Oxygen',
            'severity': 'critical',
            'steps': [
                "1. انقل المصاب لمكان جيد التهوية",
                "2. فك أي ملابس ضيقة على الصدر",
                "3. ساعده على الجلوس منتصباً",
                "4. شجعه على التنفس ببطء وعمق",
                "5. اتصل بالطوارئ"
            ],
            'warnings': [
                "⚠️ لا تتركه وحده",
                "⚠️ راقب مستوى الوعي",
                "⚠️ استعد لعمل إنعاش إذا لزم الأمر"
            ]
        }
    }
    
    @classmethod
    def get_instructions(cls, condition: str, injuries: List[Dict] = None, vital_signs: Dict = None) -> Dict[str, Any]:
        """الحصول على إرشادات الإسعافات حسب الحالة"""
        
        instructions = []
        
        # من الإصابات (Computer Vision)
        if injuries:
            for injury in injuries[:3]:  # أهم 3 إصابات
                injury_type = injury.get('type', '')
                if injury_type in cls.INSTRUCTIONS_DB:
                    instructions.append(cls.INSTRUCTIONS_DB[injury_type])
        
        # من العلامات الحيوية (Sensors)
        if vital_signs:
            # نقص أكسجين
            if vital_signs.get('spo2', {}).get('status') == 'critical':
                instructions.append(cls.INSTRUCTIONS_DB['low_oxygen'])
            
            # نبض غير طبيعي جداً - قد يشير لنوبة قلبية
            pulse = vital_signs.get('pulse', {}).get('value', 0)
            if pulse > 140 or pulse < 40:
                instructions.append(cls.INSTRUCTIONS_DB['heart_attack'])
            
            # علامات الصدمة
            bp_status = vital_signs.get('blood_pressure', {}).get('status')
            if bp_status == 'high' and pulse > 100:
                instructions.append(cls.INSTRUCTIONS_DB['shock'])
        
        # إذا لم نجد أي إرشادات محددة، نرجع إرشادات عامة
        if not instructions:
            instructions = [cls._get_general_instructions()]
        
        return {
            'instructions': instructions,
            'count': len(instructions),
            'emergency_number': '112',  # رقم الطوارئ الموحد
            'note': 'هذه إرشادات أولية فقط - اطلب المساعدة الطبية فوراً'
        }
    
    @classmethod
    def _get_general_instructions(cls) -> Dict[str, Any]:
        """إرشادات عامة"""
        return {
            'ar_title': 'إرشادات عامة',
            'en_title': 'General Instructions',
            'severity': 'medium',
            'steps': [
                "1. حافظ على هدوئك",
                "2. قيّم الوضع بسرعة",
                "3. اتصل بالطوارئ 112",
                "4. لا تحرك المصاب إلا للضرورة",
                "5. ابقَ مع المصاب حتى تصل المساعدة"
            ],
            'warnings': [
                "⚠️ لا تعطِ أي أدوية دون استشارة",
                "⚠️ لا تحرك المصاب إذا كان هناك إصابة في العمود الفقري",
                "⚠️ سجل ما حدث لإخبار الإسعاف"
            ]
        }


# مثال للاستخدام
first_aid = FirstAidInstructions()
