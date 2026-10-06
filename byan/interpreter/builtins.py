# -*- coding: utf-8 -*-
"""الدوال المدمجة في بيان"""

from .errors import ByanRuntimeError, ByanTypeError


# ===================== الدوال =====================

def _builtin_اطبع(*args, **kwargs):
    """اطبع(قيمة, ...) — يطبع قيمة أو أكثر"""
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
    text = " ".join(parts)
    print(text)
    return None


def _builtin_طول(x):
    """طول(شيء) — يرجّع عدد العناصر"""
    if x is None:
        return 0
    try:
        return len(x)
    except TypeError:
        raise ByanTypeError(f"لا يمكن أخذ طول '{type(x).__name__}'")


def _builtin_نوع(x):
    """نوع(قيمة) — يرجّع اسم النوع بالعربي"""
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
        # لو كائن OOP
        if '__class__' in x:
            cls = x['__class__']
            return cls.name if hasattr(cls, 'name') else "كائن"
        return "قاموس"
    if callable(x):
        return "دالة"
    return type(x).__name__


def _builtin_حول(x, إلى=None):
    """حول(قيمة, 'إلى نوع') — تحويل نوع
    
    حول("5", "عدد") → 5
    حول(5, "نص") → "5"
    """
    if إلى is None:
        # محاولة ذكية
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
    try:
        if إلى in ("عدد", "عدد_صحيح", "int", "رقم"):
            return int(float(x))
        if إلى in ("عدد_عشري", "float", "كسري"):
            return float(x)
        if إلى in ("نص", "string", "str"):
            if isinstance(x, bool):
                return "صحيح" if x else "خطأ"
            return str(x)
        if إلى in ("منطقي", "bool"):
            if isinstance(x, str):
                return x.strip() not in ("", "0", "خطأ", "false", "False")
            return bool(x)
        if إلى in ("قائمة", "list"):
            return list(x)
    except (ValueError, TypeError) as e:
        raise ByanTypeError(f"لا يمكن التحويل إلى '{إلى}': {e}")

    raise ByanTypeError(f"نوع غير معروف للتحويل: '{إلى}'")


def _builtin_جمع(*args):
    """جمع(أ, ب, ...) — يجمع الأعداد
    
    لو أول وسيط قائمة → يجمع عناصرها
    """
    if len(args) == 1 and isinstance(args[0], (list, tuple)):
        items = args[0]
    else:
        items = args

    total = 0
    for x in items:
        if isinstance(x, bool):
            raise ByanTypeError("لا يمكن جمع قيمة منطقية")
        if not isinstance(x, (int, float)):
            raise ByanTypeError(f"لا يمكن جمع '{type(x).__name__}'")
        total += x
    return total


def _builtin_اقرأ(*args, **kwargs):
    """اقرأ(رسالة) — يقرأ من المستخدم
    
    ملاحظة: في Android/Termux بيشتغل عادي.
    """
    prompt = args[0] if args else ""
    try:
        return input(str(prompt))
    except EOFError:
        return ""


def _builtin_مدى(*args):
    """مدى(نهاية) أو مدى(بداية, نهاية) أو مدى(بداية, نهاية, خطوة)"""
    if len(args) == 1:
        return list(range(int(args[0])))
    if len(args) == 2:
        return list(range(int(args[0]), int(args[1])))
    if len(args) == 3:
        return list(range(int(args[0]), int(args[1]), int(args[2])))
    raise ByanTypeError("مدى() يأخذ 1 أو 2 أو 3 وسائط")


def _builtin_أول(x):
    """أول(قائمة) — أول عنصر"""
    if not x:
        return None
    return x[0]


def _builtin_آخر(x):
    """آخر(قائمة) — آخر عنصر"""
    if not x:
        return None
    return x[-1]


def _builtin_أضف(lst, item):
    """أضف(قائمة, عنصر) — يضيف للقائمة (in-place)"""
    if not isinstance(lst, list):
        raise ByanTypeError("أضف() محتاج قائمة")
    lst.append(item)
    return lst


def _builtin_احذف(lst, index=None):
    """احذف(قائمة, [فهرس]) — يحذف عنصر"""
    if not isinstance(lst, list):
        raise ByanTypeError("احذف() محتاج قائمة")
    if index is None:
        if lst:
            return lst.pop()
        return None
    return lst.pop(int(index))


def _builtin_رتب(lst):
    """رتب(قائمة) — يرتب القائمة (in-place)"""
    if not isinstance(lst, list):
        raise ByanTypeError("رتب() محتاج قائمة")
    lst.sort()
    return lst


def _builtin_اعكس(lst):
    """اعكس(قائمة) — يعكس القائمة"""
    if not isinstance(lst, list):
        raise ByanTypeError("اعكس() محتاج قائمة")
    return list(reversed(lst))


def _builtin_يحتوي(container, item):
    """يحتوي(حاوية, عنصر) — هل يحتوي عليه؟"""
    if container is None:
        return False
    return item in container


# ===================== دوال القواميس =====================

def _builtin_مفاتيح(d):
    """مفاتيح(قاموس) — قائمة المفاتيح"""
    if not isinstance(d, dict):
        raise ByanTypeError("مفاتيح() محتاج قاموس")
    return list(d.keys())


def _builtin_قيم(d):
    """قيم(قاموس) — قائمة القيم"""
    if not isinstance(d, dict):
        raise ByanTypeError("قيم() محتاج قاموس")
    return list(d.values())


def _builtin_عناصر(d):
    """عناصر(قاموس) — قائمة (مفتاح, قيمة)"""
    if not isinstance(d, dict):
        raise ByanTypeError("عناصر() محتاج قاموس")
    return list(d.items())


def _builtin_دمج(*args):
    """دمج(قاموس1, قاموس2, ...) — قاموس مدمج"""
    result = {}
    for d in args:
        if not isinstance(d, dict):
            raise ByanTypeError("دمج() محتاج قواميس")
        result.update(d)
    return result


def _builtin_يحتوي_مفتاح(d, k):
    """يحتوي_مفتاح(قاموس, مفتاح) — هل المفتاح موجود؟"""
    if not isinstance(d, dict):
        raise ByanTypeError("يحتوي_مفتاح() محتاج قاموس")
    return k in d


def _builtin_احذف_مفتاح(d, k):
    """احذف_مفتاح(قاموس, مفتاح) — يحذف مفتاح"""
    if not isinstance(d, dict):
        raise ByanTypeError("احذف_مفتاح() محتاج قاموس")
    if k in d:
        del d[k]
        return True
    return False


def _builtin_امسح_القاموس(d):
    """امسح_القاموس(قاموس) — يفرّغ القاموس"""
    if not isinstance(d, dict):
        raise ByanTypeError("امسح_القاموس() محتاج قاموس")
    d.clear()
    return d


def _builtin_نسخ(d):
    """نسخ(شيء) — نسخة سطحية"""
    if isinstance(d, dict):
        return dict(d)
    if isinstance(d, list):
        return list(d)
    return d


# ===================== الانعكاس (Metaprogramming) =====================

def _builtin_خاصيات(كائن):
    """خاصيات(كائن) — قائمة أسماء الحقول"""
    if isinstance(كائن, dict) and '__fields__' in كائن:
        return list(كائن['__fields__'].keys())
    if isinstance(كائن, dict):
        return list(كائن.keys())
    raise ByanTypeError("خاصيات() محتاج كائن أو قاموس")


def _builtin_دوال(كائن):
    """دوال(كائن) — قائمة أسماء الدوال"""
    if isinstance(كائن, dict) and '__class__' in كائن:
        cls = كائن['__class__']
        return [m.name for m in cls.methods]
    return []


def _builtin_قيمة(كائن, اسم):
    """قيمة(كائن, "اسم") — قراءة خاصية"""
    اسم = str(اسم)
    if isinstance(كائن, dict) and '__fields__' in كائن:
        fields = كائن['__fields__']
        if اسم in fields:
            return fields[اسم]
        raise ByanRuntimeError(f"الخاصية '{اسم}' غير موجودة")
    if isinstance(كائن, dict):
        if اسم in كائن:
            return كائن[اسم]
        raise ByanRuntimeError(f"المفتاح '{اسم}' غير موجود")
    raise ByanTypeError("قيمة() محتاج كائن أو قاموس")


def _builtin_ضع_خاصية(كائن, اسم, قيمة_جديدة):
    """ضع_خاصية(كائن, "اسم", قيمة) — تعديل خاصية"""
    اسم = str(اسم)
    if isinstance(كائن, dict) and '__fields__' in كائن:
        كائن['__fields__'][اسم] = قيمة_جديدة
        return True
    if isinstance(كائن, dict):
        كائن[اسم] = قيمة_جديدة
        return True
    raise ByanTypeError("ضع_خاصية() محتاج كائن أو قاموس")


def _builtin_نوع_كائن(كائن):
    """نوع_كائن(كائن) — اسم الفئة"""
    if isinstance(كائن, dict) and '__class__' in كائن:
        cls = كائن['__class__']
        return cls.name if hasattr(cls, 'name') else "كائن"
    return "كائن"


def _builtin_هل_فئة(كائن):
    """هل_فئة(كائن) — هل هو كائن من فئة؟"""
    return isinstance(كائن, dict) and '__class__' in كائن


def _builtin_معلومات(كائن):
    """معلومات(كائن) — قاموس معلومات كامل"""
    result = {}
    if isinstance(كائن, dict) and '__class__' in كائن:
        cls = كائن['__class__']
        result['الفئة'] = cls.name if hasattr(cls, 'name') else "كائن"
        result['الأب'] = cls.extends if hasattr(cls, 'extends') else ""
        result['الحقول'] = list(كائن['__fields__'].keys())
        result['الدوال'] = [m.name for m in cls.methods]
        result['القيم'] = dict(كائن['__fields__'])
        return result
    if isinstance(كائن, dict):
        result['النوع'] = "قاموس"
        result['المفاتيح'] = list(كائن.keys())
        result['القيم'] = dict(كائن)
        return result
    result['النوع'] = type(كائن).__name__
    result['القيمة'] = str(كائن)
    return result


# ===================== إدارة الذاكرة =====================

# قاموس عالمي لتتبع "التحرير"
_FREED_IDS = set()


def _builtin_حجم(شيء):
    """حجم(شيء) — حجم تقديري بالبايت"""
    import sys
    try:
        return sys.getsizeof(شيء)
    except (TypeError, ValueError):
        return 0


def _builtin_عدد_المراجع(شيء):
    """عدد_المراجع(شيء) — عدد المراجع الفعلي"""
    import sys
    try:
        return sys.getrefcount(شيء) - 1  # -1 لـ arg نفسه
    except Exception:
        return 0


def _builtin_نسخة_عميقة(شيء):
    """نسخة_عميقة(شيء) — deep copy"""
    import copy
    return copy.deepcopy(شيء)


def _builtin_نسخة_سطحية(شيء):
    """نسخة_سطحية(شيء) — shallow copy"""
    import copy
    return copy.copy(شيء)


def _builtin_حرر(شيء):
    """حرر(شيء) — محاكاة تحرير يدوي

    ملاحظة: Python عنده garbage collection تلقائي.
    الدالة دي بتسجّل الـ id كـ freed — للمحاكاة فقط.
    """
    if isinstance(شيء, dict):
        شيء.clear()
    elif isinstance(شيء, list):
        شيء.clear()
    elif isinstance(شيء, set):
        شيء.clear()
    _FREED_IDS.add(id(شيء))
    return True


def _builtin_محرر(شيء):
    """محرر(شيء) — هل تم تحريره؟"""
    return id(شيء) in _FREED_IDS


def _builtin_معرف(شيء):
    """معرف(شيء) — id فريد"""
    return id(شيء)


def _builtin_كبير_الحجم(عناصر=None, عدد=5):
    """كبير_الحجم(قائمة, [عدد]) — أكبر العناصر حجماً"""
    import sys
    if عناصر is None:
        return []
    if not isinstance(عناصر, (list, tuple)):
        return []
    items = [(x, sys.getsizeof(x)) for x in عناصر]
    items.sort(key=lambda t: t[1], reverse=True)
    return [(str(x), size) for x, size in items[:int(عدد)]]


def _builtin_فرّغ():
    """فرّغ() — يفرّغ سجل التحرير"""
    _FREED_IDS.clear()
    return True


def _builtin_عدد_المحرر():
    """عدد_المحرر() — عدد الكائنات المحررة"""
    return len(_FREED_IDS)


# ===================== دوال تفاعلية جديدة =====================

def _builtin_اعرض(*args, **kwargs):
    """اعرض(...) — alias لـ اطبع"""
    return _builtin_اطبع(*args, **kwargs)


def _builtin_انتظر(*args):
    """انتظر(عدد, [وحدة]) — تأخير
    
    انتظر(2)              → 2 ثواني
    انتظر(500, "ملي")     → 500 مللي ثانية
    انتظر(1, "ثانية")     → 1 ثانية
    """
    import time
    if not args:
        return None
    n = args[0]
    if not isinstance(n, (int, float)):
        raise ByanTypeError("انتظر() محتاج رقم")
    unit = args[1] if len(args) > 1 else "ثانية"
    unit = str(unit).strip()
    
    if unit in ("ملي", "ملي_ثانية", "ms", "مللي"):
        time.sleep(n / 1000.0)
    elif unit in ("ثانية", "ثواني", "s", "sec"):
        time.sleep(n)
    elif unit in ("دقيقة", "دقائق", "min"):
        time.sleep(n * 60)
    else:
        time.sleep(n)
    return None


def _builtin_اسأل(*args):
    """اسأل([رسالة]) — قراءة من المستخدم"""
    prompt = args[0] if args else ""
    try:
        return input(str(prompt))
    except EOFError:
        return ""


def _builtin_اقرأ_ملف(*args):
    """اقرأ_ملف(مسار) — قراءة ملف نصي"""
    if not args:
        raise ByanTypeError("اقرأ_ملف() محتاج مسار")
    import os
    p = str(args[0])
    enc = str(args[1]) if len(args) > 1 else "utf-8"
    if not os.path.exists(p):
        raise ByanRuntimeError(f"الملف مش موجود: {p}")
    try:
        with open(p, "r", encoding=enc) as f:
            return f.read()
    except Exception as e:
        raise ByanRuntimeError(f"فشل قراءة الملف: {e}")


def _builtin_اكتب_ملف(*args):
    """اكتب_ملف(مسار, محتوى, [إلحاق]) — كتابة ملف نصي"""
    if len(args) < 2:
        raise ByanTypeError("اكتب_ملف() محتاج مسار ومحتوى")
    p = str(args[0])
    content = str(args[1])
    append = bool(args[2]) if len(args) > 2 else False
    mode = "a" if append else "w"
    try:
        import os
        parent = os.path.dirname(p)
        if parent and not os.path.exists(parent):
            os.makedirs(parent, exist_ok=True)
        with open(p, mode, encoding="utf-8") as f:
            f.write(content)
        return len(content)
    except Exception as e:
        raise ByanRuntimeError(f"فشل كتابة الملف: {e}")


def _builtin_موجود(*args):
    """موجود(مسار) — هل الملف/المجلد موجود؟"""
    if not args:
        return False
    import os
    return os.path.exists(str(args[0]))


def _builtin_احذف_ملف(*args):
    """احذف_ملف(مسار) — حذف ملف"""
    if not args:
        raise ByanTypeError("احذف_ملف() محتاج مسار")
    import os
    p = str(args[0])
    if not os.path.exists(p):
        return False
    try:
        if os.path.isfile(p):
            os.remove(p)
        else:
            import shutil as _sh
            _sh.rmtree(p)
        return True
    except Exception as e:
        raise ByanRuntimeError(f"فشل الحذف: {e}")


def _builtin_قائمة_ملفات(*args):
    """قائمة_ملفات(مجلد) — قائمة أسماء الملفات"""
    if not args:
        raise ByanTypeError("قائمة_ملفات() محتاج مجلد")
    import os
    p = str(args[0])
    if not os.path.isdir(p):
        raise ByanRuntimeError(f"المجلد مش موجود: {p}")
    try:
        return os.listdir(p)
    except Exception as e:
        raise ByanRuntimeError(f"فشل سرد الملفات: {e}")


def _builtin_الوقت():
    """الوقت() — الوقت الحالي كنص"""
    import datetime
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _builtin_محيط():
    """محيط() — مسار المجلد الحالي"""
    import os
    return os.getcwd()


# ===================== التسجيل =====================

BUILTINS = {
    # أساسيات
    "اطبع": _builtin_اطبع,
    "اعرض": _builtin_اعرض,
    "اقرأ": _builtin_اقرأ,
    "اسأل": _builtin_اسأل,
    "طول": _builtin_طول,
    "نوع": _builtin_نوع,
    "حول": _builtin_حول,
    "جمع": _builtin_جمع,
    "مدى": _builtin_مدى,
    # قوائم
    "أول": _builtin_أول,
    "آخر": _builtin_آخر,
    "أضف": _builtin_أضف,
    "احذف": _builtin_احذف,
    "رتب": _builtin_رتب,
    "اعكس": _builtin_اعكس,
    "يحتوي": _builtin_يحتوي,
    # ملفات
    "اقرأ_ملف": _builtin_اقرأ_ملف,
    "اكتب_ملف": _builtin_اكتب_ملف,
    "موجود": _builtin_موجود,
    "احذف_ملف": _builtin_احذف_ملف,
    "قائمة_ملفات": _builtin_قائمة_ملفات,
    # وقت/نظام
    "انتظر": _builtin_انتظر,
    "الوقت": _builtin_الوقت,
    "محيط": _builtin_محيط,
    # ذاكرة
    "حجم": _builtin_حجم,
    "عدد_المراجع": _builtin_عدد_المراجع,
    "نسخة_عميقة": _builtin_نسخة_عميقة,
    "نسخة_سطحية": _builtin_نسخة_سطحية,
    "حرر": _builtin_حرر,
    "محرر": _builtin_محرر,
    "معرف": _builtin_معرف,
    "كبير_الحجم": _builtin_كبير_الحجم,
    "فرّغ": _builtin_فرّغ,
    "عدد_المحرر": _builtin_عدد_المحرر,
    # انعكاس
    "خاصيات": _builtin_خاصيات,
    "دوال": _builtin_دوال,
    "قيمة": _builtin_قيمة,
    "ضع_خاصية": _builtin_ضع_خاصية,
    "نوع_كائن": _builtin_نوع_كائن,
    "هل_فئة": _builtin_هل_فئة,
    "معلومات": _builtin_معلومات,
    # قواميس
    "مفاتيح": _builtin_مفاتيح,
    "قيم": _builtin_قيم,
    "عناصر": _builtin_عناصر,
    "دمج": _builtin_دمج,
    "يحتوي_مفتاح": _builtin_يحتوي_مفتاح,
    "احذف_مفتاح": _builtin_احذف_مفتاح,
    "امسح_القاموس": _builtin_امسح_القاموس,
    "نسخ": _builtin_نسخ,
}


def call_builtin(name, args):
    """ينادي دالة مدمجة — يرفض لو مش موجودة"""
    fn = BUILTINS.get(name)
    if fn is None:
        raise ByanRuntimeError(f"دالة مدمجة غير معروفة: '{name}'")
    try:
        return fn(*args)
    except ByanRuntimeError:
        raise
    except Exception as e:
        raise ByanRuntimeError(f"خطأ في '{name}': {e}")
