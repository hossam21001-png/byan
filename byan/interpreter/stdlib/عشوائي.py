# -*- coding: utf-8 -*-
"""وحدة العشوائية"""

import random as _random


def عدد(أ=0, ب=100):
    """عدد صحيح عشوائي"""
    return _random.randint(int(أ), int(ب))


def عشري():
    """عشري [0, 1)"""
    return _random.random()


def اختر(قائمة):
    """عنصر عشوائي"""
    return _random.choice(قائمة) if قائمة else None


def اخلط(قائمة):
    """خلط (in-place)"""
    _random.shuffle(قائمة)
    return قائمة


def عينة(قائمة, عدد_):
    """عينة عشوائية"""
    return _random.sample(قائمة, min(int(عدد_), len(قائمة)))


def بذرة(x):
    """تعيين بذرة"""
    _random.seed(x)
    return True


def من_قائمة(قائمة):
    """alias اختر"""
    return اختر(قائمة)


def رمز(طول=8):
    """نص عشوائي"""
    import string
    chars = string.ascii_letters + string.digits
    return ''.join(_random.choice(chars) for _ in range(int(طول)))


FUNCTIONS = {
    'عدد': عدد,
    'عشري': عشري,
    'اختر': اختر,
    'اخلط': اخلط,
    'عينة': عينة,
    'بذرة': بذرة,
    'من_قائمة': من_قائمة,
    'رمز': رمز,
}
