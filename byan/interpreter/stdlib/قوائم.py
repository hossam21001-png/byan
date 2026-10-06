# -*- coding: utf-8 -*-
"""وحدة القوائم"""


def رتب(قائمة, عكسي=False):
    """ترتيب"""
    return sorted(قائمة, reverse=عكسي)


def فلتر(قائمة, شرط):
    """فلترة بـ lambda"""
    return [x for x in قائمة if شرط(x)]


def حول_كل(قائمة, دالة):
    """map"""
    return [دالة(x) for x in قائمة]


def احذف_مكرر(قائمة):
    """إزالة التكرار"""
    result = []
    for x in قائمة:
        if x not in result:
            result.append(x)
    return result


def ادمج_قوائم(*قوائم):
    """دمج قوائم"""
    result = []
    for c in قوائم:
        result.extend(c)
    return result


def مقطع(قائمة, بداية, نهاية=None):
    """substring"""
    if نهاية is None:
        return قائمة[بداية:]
    return قائمة[بداية:نهاية]


def اعكس(قائمة):
    """عكس"""
    return list(reversed(قائمة))


def أطول_عنصر(قائمة):
    """أطول عنصر نصي"""
    if not قائمة:
        return ""
    return max(قائمة, key=lambda x: len(str(x)))


def أوسع_عنصر(قائمة):
    """أقصر عنصر"""
    if not قائمة:
        return ""
    return min(قائمة, key=lambda x: len(str(x)))


def مجموع(قائمة):
    """مجموع"""
    return sum(قائمة)


def متوسط(قائمة):
    """متوسط"""
    if not قائمة:
        return 0
    return sum(قائمة) / len(قائمة)


def عنصر_عشوائي(قائمة):
    """عنصر عشوائي"""
    import random
    return random.choice(قائمة) if قائمة else None


FUNCTIONS = {
    'رتب': رتب,
    'فلتر': فلتر,
    'حول_كل': حول_كل,
    'احذف_مكرر': احذف_مكرر,
    'ادمج_قوائم': ادمج_قوائم,
    'مقطع': مقطع,
    'اعكس': اعكس,
    'أطول_عنصر': أطول_عنصر,
    'أوسع_عنصر': أوسع_عنصر,
    'مجموع': مجموع,
    'متوسط': متوسط,
    'عنصر_عشوائي': عنصر_عشوائي,
}
