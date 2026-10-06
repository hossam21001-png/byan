# -*- coding: utf-8 -*-
"""Byan Runtime Library — تعمل مع الكود المترجم من Byan

هذا الملف يحتوي على كل ما يحتاجه البرنامج المترجم:
- Environment للـ scopes
- ByanObject للكائنات
- Builtins
- ByanThrow للأخطاء
"""

import sys
import os
import math as _math
import json as _json
import time as _time
import datetime as _dt
import random as _random
import hashlib as _hash
import base64 as _b64
import uuid as _uuid
import shutil as _shutil


# ===================== أخطاء =====================

class ByanThrow(Exception):
    """خطأ من Byan"""
    def __init__(self, message):
        self.message = message
        super().__init__(str(message))


class ByanNameError(ByanThrow):
    pass


# ===================== البيئة =====================

class Environment:
    """بيئة المتغيرات"""

    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent

    def define(self, name, value):
        self.vars[name] = value
        return value

    def get(self, name):
        if name in self.vars:
            return self.vars[name]
        if self.parent is not None:
            return self.parent.get(name)
        raise ByanNameError(f"المتغير '{name}' غير معرّف")

    def set(self, name, value):
        if name in self.vars:
            self.vars[name] = value
            return value
        env = self.parent
        while env is not None:
            if name in env.vars:
                env.vars[name] = value
                return value
            env = env.parent
        self.vars[name] = value
        return value

    def has(self, name):
        if name in self.vars:
            return True
        if self.parent is not None:
            return self.parent.has(name)
        return False

    def child(self):
        return Environment(parent=self)

    def root(self):
        env = self
        while env.parent is not None:
            env = env.parent
        return env

    def define_global(self, name, value):
        self.root().vars[name] = value
        return value

    def set_global(self, name, value):
        root = self.root()
        if name not in root.vars:
            raise ByanNameError(f"المتغير العام '{name}' غير معرّف")
        root.vars[name] = value
        return value

    def set_nonlocal(self, name, value):
        env = self.parent
        while env is not None:
            if name in env.vars:
                env.vars[name] = value
                return value
            env = env.parent
        raise ByanNameError(f"المتغير '{name}' غير موجود في الأب")


# ===================== Builtins =====================

def اطبع(*args):
    parts = []
    for a in args:
        if a is None:
            parts.append("لا_شيء")
        elif a is True:
            parts.append("صحيح")
        elif a is False:
            parts.append("خطأ")
        else:
            parts.append(str(a))
    print(" ".join(parts))
    return None


def اعرض(*args):
    return اطبع(*args)


def اقرأ(رسالة=""):
    try:
        return input(str(رسالة))
    except EOFError:
        return ""


def اسأل(رسالة=""):
    return اقرأ(رسالة)


def طول(x):
    if x is None:
        return 0
    return len(x)


def نوع(x):
    if x is None:
        return "لا_شيء"
    if isinstance(x, bool):
        return "منطقي"
    if isinstance(x, int):
        return "عدد"
    if isinstance(x, float):
        return "عدد_عشري"
    if isinstance(x, str):
        return "نص"
    if isinstance(x, list):
        return "قائمة"
    if isinstance(x, dict):
        if '__class__' in x:
            cls = x['__class__']
            return cls.name if hasattr(cls, 'name') else "كائن"
        return "قاموس"
    if callable(x):
        return "دالة"
    return type(x).__name__


def حول(x, إلى=None):
    if إلى is None:
        if isinstance(x, str):
            try:
                return int(x)
            except ValueError:
                try:
                    return float(x)
                except ValueError:
                    return x
        return str(x)
    إلى = str(إلى).strip()
    if إلى in ("عدد", "عدد_صحيح", "int", "رقم"):
        return int(float(x))
    if إلى in ("عدد_عشري", "float"):
        return float(x)
    if إلى in ("نص", "str", "string"):
        if isinstance(x, bool):
            return "صحيح" if x else "خطأ"
        return str(x)
    if إلى in ("منطقي", "bool"):
        if isinstance(x, str):
            return x.strip() not in ("", "0", "خطأ", "false", "False")
        return bool(x)
    if إلى in ("قائمة", "list"):
        return list(x)
    raise ByanThrow(f"لا يمكن التحويل إلى '{إلى}'")


def جمع(*args):
    if len(args) == 1 and isinstance(args[0], (list, tuple)):
        items = args[0]
    else:
        items = args
    total = 0
    for x in items:
        if isinstance(x, bool):
            raise ByanThrow("لا يمكن جمع قيمة منطقية")
        if not isinstance(x, (int, float)):
            raise ByanThrow(f"لا يمكن جمع '{type(x).__name__}'")
        total += x
    return total


def مدى(*args):
    if len(args) == 1:
        return list(range(int(args[0])))
    if len(args) == 2:
        return list(range(int(args[0]), int(args[1])))
    if len(args) == 3:
        return list(range(int(args[0]), int(args[1]), int(args[2])))
    raise ByanThrow("مدى() يأخذ 1 أو 2 أو 3 وسائط")


def أول(x):
    if not x:
        return None
    return x[0]


def آخر(x):
    if not x:
        return None
    return x[-1]


def أضف(lst, item):
    if not isinstance(lst, list):
        raise ByanThrow("أضف() محتاج قائمة")
    lst.append(item)
    return lst


def احذف(lst, index=None):
    if not isinstance(lst, list):
        raise ByanThrow("احذف() محتاج قائمة")
    if index is None:
        return lst.pop() if lst else None
    return lst.pop(int(index))


def رتب(lst):
    if not isinstance(lst, list):
        raise ByanThrow("رتب() محتاج قائمة")
    lst.sort()
    return lst


def اعكس(lst):
    if not isinstance(lst, list):
        raise ByanThrow("اعكس() محتاج قائمة")
    return list(reversed(lst))


def يحتوي(container, item):
    if container is None:
        return False
    return item in container


# ===================== الوقت =====================

def انتظر(ثواني):
    _time.sleep(float(ثواني))
    return True


def الوقت():
    return _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ===================== ملفات =====================

def اقرأ_ملف(مسار, ترميز="utf-8"):
    if not os.path.exists(مسار):
        raise ByanThrow(f"الملف مش موجود: {مسار}")
    with open(مسار, 'r', encoding=ترميز) as f:
        return f.read()


def اكتب_ملف(مسار, محتوى, ترميز="utf-8"):
    د = os.path.dirname(مسار)
    if د and not os.path.exists(د):
        os.makedirs(د, exist_ok=True)
    with open(مسار, 'w', encoding=ترميز) as f:
        f.write(str(محتوى))
    return True


def موجود(مسار):
    return os.path.exists(مسار)


def احذف_ملف(مسار):
    if not os.path.exists(مسار):
        return False
    if os.path.isfile(مسار):
        os.remove(مسار)
    else:
        _shutil.rmtree(مسار)
    return True


def قائمة_ملفات(مجلد="."):
    return os.listdir(مجلد)


# ===================== قواميس =====================

def مفاتيح(d):
    if not isinstance(d, dict):
        raise ByanThrow("مفاتيح() محتاج قاموس")
    return list(d.keys())


def قيم(d):
    if not isinstance(d, dict):
        raise ByanThrow("قيم() محتاج قاموس")
    return list(d.values())


def عناصر(d):
    if not isinstance(d, dict):
        raise ByanThrow("عناصر() محتاج قاموس")
    return list(d.items())


def دمج(*args):
    result = {}
    for d in args:
        if not isinstance(d, dict):
            raise ByanThrow("دمج() محتاج قواميس")
        result.update(d)
    return result


def يحتوي_مفتاح(d, k):
    if not isinstance(d, dict):
        raise ByanThrow("يحتوي_مفتاح() محتاج قاموس")
    return k in d


def احذف_مفتاح(d, k):
    if not isinstance(d, dict):
        raise ByanThrow("احذف_مفتاح() محتاج قاموس")
    if k in d:
        del d[k]
        return True
    return False


# ===================== انعكاس =====================

def خاصيات(كائن):
    if isinstance(كائن, dict) and '__fields__' in كائن:
        return list(كائن['__fields__'].keys())
    if isinstance(كائن, dict):
        return list(كائن.keys())
    raise ByanThrow("خاصيات() محتاج كائن أو قاموس")


def دوال(كائن):
    if isinstance(كائن, dict) and '__class__' in كائن:
        cls = كائن['__class__']
        return [m.name for m in cls.methods]
    return []


def قيمة(كائن, اسم):
    اسم = str(اسم)
    if isinstance(كائن, dict) and '__fields__' in كائن:
        if اسم in كائن['__fields__']:
            return كائن['__fields__'][اسم]
        raise ByanThrow(f"الخاصية '{اسم}' غير موجودة")
    if isinstance(كائن, dict):
        if اسم in كائن:
            return كائن[اسم]
        raise ByanThrow(f"المفتاح '{اسم}' غير موجود")
    raise ByanThrow("قيمة() محتاج كائن أو قاموس")


def ضع_خاصية(كائن, اسم, قيمة_جديدة):
    اسم = str(اسم)
    if isinstance(كائن, dict) and '__fields__' in كائن:
        كائن['__fields__'][اسم] = قيمة_جديدة
        return True
    if isinstance(كائن, dict):
        كائن[اسم] = قيمة_جديدة
        return True
    raise ByanThrow("ضع_خاصية() محتاج كائن أو قاموس")


def نوع_كائن(كائن):
    if isinstance(كائن, dict) and '__class__' in كائن:
        cls = كائن['__class__']
        return cls.name if hasattr(cls, 'name') else "كائن"
    return "كائن"


def هل_فئة(كائن):
    return isinstance(كائن, dict) and '__class__' in كائن


def معلومات(كائن):
    result = {}
    if isinstance(كائن, dict) and '__class__' in كائن:
        cls = كائن['__class__']
        result['الفئة'] = cls.name if hasattr(cls, 'name') else "كائن"
        result['الأب'] = cls.extends if hasattr(cls, 'extends') else ""
        result['الحقول'] = list(كائن['__fields__'].keys())
        result['الدوال'] = [m.name for m in cls.methods]
        result['القيم'] = dict(كائن['__fields__'])
    return result


# ===================== ذاكرة =====================

def حجم(شيء):
    try:
        return sys.getsizeof(شيء)
    except (TypeError, ValueError):
        return 0


def عدد_المراجع(شيء):
    try:
        return sys.getrefcount(شيء) - 1
    except Exception:
        return 0


def نسخة_عميقة(شيء):
    import copy
    return copy.deepcopy(شيء)


def نسخة_سطحية(شيء):
    import copy
    return copy.copy(شيء)


# ===================== وحدة الرياضيات =====================

class رياضيات:
    @staticmethod
    def جذر(x):
        if x < 0:
            raise ByanThrow("لا يمكن جذر رقم سالب")
        return _math.sqrt(x)
    
    @staticmethod
    def قوة(أ, ب):
        return أ ** ب
    
    @staticmethod
    def جيب(x):
        return _math.sin(x)
    
    @staticmethod
    def جيب_تمام(x):
        return _math.cos(x)
    
    @staticmethod
    def ظل(x):
        return _math.tan(x)
    
    @staticmethod
    def لوغاريتم(x):
        return _math.log(x)
    
    @staticmethod
    def لوغاريتم10(x):
        return _math.log10(x)
    
    @staticmethod
    def مطلق(x):
        return abs(x)
    
    @staticmethod
    def تقريب(x, منازل=0):
        return round(x, منازل)
    
    @staticmethod
    def أعلى_عدد(*args):
        return max(args)
    
    @staticmethod
    def أدنى_عدد(*args):
        return min(args)
    
    @staticmethod
    def أرضية(x):
        return _math.floor(x)
    
    @staticmethod
    def سقف(x):
        return _math.ceil(x)
    
    @staticmethod
    def باقي(أ, ب):
        return أ % ب
    
    @staticmethod
    def فاي():
        return _math.pi
    
    @staticmethod
    def هـ():
        return _math.e


# ===================== وحدة النصوص =====================

class نصوص:
    @staticmethod
    def استبدل(نص, قديم, جديد):
        return str(نص).replace(str(قديم), str(جديد))
    
    @staticmethod
    def اقتطع(نص, فاصل=None):
        if فاصل is None:
            return str(نص).split()
        return str(نص).split(str(فاصل))
    
    @staticmethod
    def ادمج(قائمة, فاصل=""):
        return str(فاصل).join(str(x) for x in قائمة)
    
    @staticmethod
    def كبير(نص):
        return str(نص).upper()
    
    @staticmethod
    def صغير(نص):
        return str(نص).lower()
    
    @staticmethod
    def نظّف(نص):
        return str(نص).strip()
    
    @staticmethod
    def يحتوي(نص, جزء):
        return str(جزء) in str(نص)
    
    @staticmethod
    def يبدأ_بـ(نص, جزء):
        return str(نص).startswith(str(جزء))
    
    @staticmethod
    def ينتهي_بـ(نص, جزء):
        return str(نص).endswith(str(جزء))
    
    @staticmethod
    def مقطع(نص, بداية, نهاية=None):
        s = str(نص)
        if نهاية is None:
            return s[بداية:]
        return s[بداية:نهاية]
    
    @staticmethod
    def موضع(نص, جزء):
        return str(نص).find(str(جزء))
    
    @staticmethod
    def عدّ(نص, جزء):
        return str(نص).count(str(جزء))
    
    @staticmethod
    def كرّر(نص, مرة):
        return str(نص) * int(مرة)


# ===================== وحدة JSON =====================

class JSON:
    @staticmethod
    def حلّل(نص):
        return _json.loads(str(نص))
    
    @staticmethod
    def حوّل(كائن, جميل=False):
        if جميل:
            return _json.dumps(كائن, ensure_ascii=False, indent=2)
        return _json.dumps(كائن, ensure_ascii=False)
    
    @staticmethod
    def صحيح(نص):
        try:
            _json.loads(str(نص))
            return True
        except (ValueError, TypeError):
            return False


# ===================== وحدة عشوائي =====================

class عشوائي:
    @staticmethod
    def عدد(أ=0, ب=100):
        return _random.randint(int(أ), int(ب))
    
    @staticmethod
    def عشري():
        return _random.random()
    
    @staticmethod
    def اختر(قائمة):
        return _random.choice(قائمة) if قائمة else None
    
    @staticmethod
    def اخلط(قائمة):
        _random.shuffle(قائمة)
        return قائمة
    
    @staticmethod
    def عينة(قائمة, عدد_):
        return _random.sample(قائمة, min(int(عدد_), len(قائمة)))


# ===================== وحدة تشفير =====================

class تشفير:
    @staticmethod
    def md5(نص):
        return _hash.md5(str(نص).encode('utf-8')).hexdigest()
    
    @staticmethod
    def sha256(نص):
        return _hash.sha256(str(نص).encode('utf-8')).hexdigest()
    
    @staticmethod
    def تشفير_base64(نص):
        return _b64.b64encode(str(نص).encode('utf-8')).decode('ascii')
    
    @staticmethod
    def فك_base64(نص):
        return _b64.b64decode(str(نص).encode('ascii')).decode('utf-8')
    
    @staticmethod
    def معرف_فريد():
        return str(_uuid.uuid4())


# ===================== كائن Byan =====================

class ByanClass:
    """يمثّل فئة Byan"""
    def __init__(self, name, extends=""):
        self.name = name
        self.extends = extends
        self.methods = []
        self.fields = []


def ByanNew(cls, instance):
    """ينشئ كائن جديد"""
    return {
        '__class__': cls,
        '__fields__': instance,
    }


# ===================== مساعدات =====================

def __safe_div__(أ, ب):
    if ب == 0:
        raise ByanThrow("قسمة على صفر")
    return أ / ب


def __safe_floordiv__(أ, ب):
    if ب == 0:
        raise ByanThrow("قسمة على صفر")
    return أ // ب


BUILTINS = {
    'اطبع': اطبع, 'اعرض': اعرض, 'اقرأ': اقرأ, 'اسأل': اسأل,
    'طول': طول, 'نوع': نوع, 'حول': حول, 'جمع': جمع, 'مدى': مدى,
    'أول': أول, 'آخر': آخر, 'أضف': أضف, 'احذف': احذف,
    'رتب': رتب, 'اعكس': اعكس, 'يحتوي': يحتوي,
    'انتظر': انتظر, 'الوقت': الوقت,
    'اقرأ_ملف': اقرأ_ملف, 'اكتب_ملف': اكتب_ملف,
    'موجود': موجود, 'احذف_ملف': احذف_ملف, 'قائمة_ملفات': قائمة_ملفات,
    'مفاتيح': مفاتيح, 'قيم': قيم, 'عناصر': عناصر,
    'دمج': دمج, 'يحتوي_مفتاح': يحتوي_مفتاح, 'احذف_مفتاح': احذف_مفتاح,
    'خاصيات': خاصيات, 'دوال': دوال, 'قيمة': قيمة,
    'ضع_خاصية': ضع_خاصية, 'نوع_كائن': نوع_كائن,
    'هل_فئة': هل_فئة, 'معلومات': معلومات,
    'حجم': حجم, 'عدد_المراجع': عدد_المراجع,
    'نسخة_عميقة': نسخة_عميقة, 'نسخة_سطحية': نسخة_سطحية,
}


# ===================== الـ Main =====================

def byan_run(main_func):
    """يشغّل main"""
    try:
        main_func()
    except ByanThrow as e:
        print(f"❌ خطأ: {e.message}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 تم الإيقاف")
        sys.exit(0)


def __run__(main_func):
    """alias"""
    return byan_run(main_func)
