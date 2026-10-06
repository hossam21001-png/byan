# -*- coding: utf-8 -*-
"""وحدة النصوص"""


def استبدل(نص, قديم, جديد):
    """استبدال كل"""
    return str(نص).replace(str(قديم), str(جديد))


def اقتطع(نص, فاصل=None):
    """تقسيم"""
    if فاصل is None:
        return str(نص).split()
    return str(نص).split(str(فاصل))


def ادمج(قائمة, فاصل=""):
    """دمج قائمة"""
    return str(فاصل).join(str(x) for x in قائمة)


def كبير(نص):
    """UPPERCASE"""
    return str(نص).upper()


def صغير(نص):
    """lowercase"""
    return str(نص).lower()


def نظّف(نص):
    """trim"""
    return str(نص).strip()


def نظّف_يسار(نص):
    """lstrip"""
    return str(نص).lstrip()


def نظّف_يمين(نص):
    """rstrip"""
    return str(نص).rstrip()


def يحتوي(نص, جزء):
    """هل يحتوي على؟"""
    return str(جزء) in str(نص)


def يبدأ_بـ(نص, جزء):
    """startswith"""
    return str(نص).startswith(str(جزء))


def ينتهي_بـ(نص, جزء):
    """endswith"""
    return str(نص).endswith(str(جزء))


def مقطع(نص, بداية, نهاية=None):
    """substring"""
    s = str(نص)
    if نهاية is None:
        return s[بداية:]
    return s[بداية:نهاية]


def موضع(نص, جزء):
    """indexOf — يرجّع -1 لو مش موجود"""
    return str(نص).find(str(جزء))


def عدّ(نص, جزء):
    """count"""
    return str(نص).count(str(جزء))


def كرّر(نص, مرة):
    """تكرار"""
    return str(نص) * int(مرة)


def اعكس_نص(نص):
    """عكس النص"""
    return str(نص)[::-1]


def حرف(نص, فهرس):
    """الحرف في الفهرس"""
    return str(نص)[int(فهرس)]


def طول(نص):
    """طول النص"""
    return len(str(نص))


def رقم_لنص(x):
    """تحويل لنص"""
    return str(x)


def نص_لرقم(نص, افتراضي=0):
    """تحويل لرقم"""
    try:
        s = str(نص).strip()
        if '.' in s:
            return float(s)
        return int(s)
    except (ValueError, AttributeError):
        return افتراضي


def تنسيق(نص, *args):
    """تنسيق بنمط {}"""
    return str(نص).format(*args)


FUNCTIONS = {
    'استبدل': استبدل,
    'اقتطع': اقتطع,
    'ادمج': ادمج,
    'كبير': كبير,
    'صغير': صغير,
    'نظّف': نظّف,
    'نظّف_يسار': نظّف_يسار,
    'نظّف_يمين': نظّف_يمين,
    'يحتوي': يحتوي,
    'يبدأ_بـ': يبدأ_بـ,
    'ينتهي_بـ': ينتهي_بـ,
    'مقطع': مقطع,
    'موضع': موضع,
    'عدّ': عدّ,
    'كرّر': كرّر,
    'اعكس_نص': اعكس_نص,
    'حرف': حرف,
    'طول': طول,
    'رقم_لنص': رقم_لنص,
    'نص_لرقم': نص_لرقم,
    'تنسيق': تنسيق,
}
