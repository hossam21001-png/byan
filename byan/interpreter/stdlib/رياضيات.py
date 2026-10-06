# -*- coding: utf-8 -*-
"""وحدة الرياضيات"""

import math as _math


def جذر(x):
    """الجذر التربيعي"""
    if x < 0:
        raise ValueError("لا يمكن جذر رقم سالب")
    return _math.sqrt(x)


def قوة(أساس, أس):
    """قوة: أساس^أس"""
    return أساس ** أس


def جيب(x):
    """sin (بالراديان)"""
    return _math.sin(x)


def جيب_تمام(x):
    """cos (بالراديان)"""
    return _math.cos(x)


def ظل(x):
    """tan (بالراديان)"""
    return _math.tan(x)


def لوغاريتم(x, أساس=_math.e):
    """log"""
    return _math.log(x, أساس)


def لوغاريتم10(x):
    """log10"""
    return _math.log10(x)


def مطلق(x):
    """|x|"""
    return abs(x)


def تقريب(x, منازل=0):
    """تقريب"""
    return round(x, منازل)


def أعلى_عدد(*args):
    """أكبر عدد"""
    return max(args)


def أدنى_عدد(*args):
    """أصغر عدد"""
    return min(args)


def أرضية(x):
    """floor"""
    return _math.floor(x)


def سقف(x):
    """ceil"""
    return _math.ceil(x)


def باقي(أ, ب):
    """باقي القسمة"""
    return أ % ب


def مكافي(أ, ب):
    """أ^ب (بكسل)"""
    return pow(أ, ب)


def فاي():
    """π"""
    return _math.pi


def هـ():
    """e"""
    return _math.e


FUNCTIONS = {
    'جذر': جذر,
    'قوة': قوة,
    'جيب': جيب,
    'جيب_تمام': جيب_تمام,
    'ظل': ظل,
    'لوغاريتم': لوغاريتم,
    'لوغاريتم10': لوغاريتم10,
    'مطلق': مطلق,
    'تقريب': تقريب,
    'أعلى_عدد': أعلى_عدد,
    'أدنى_عدد': أدنى_عدد,
    'أرضية': أرضية,
    'سقف': سقف,
    'باقي': باقي,
    'مكافي': مكافي,
    'فاي': فاي,
    'هـ': هـ,
    'pi': فاي,      # alias
    'e': هـ,        # alias
}
