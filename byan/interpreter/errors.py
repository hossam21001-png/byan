# -*- coding: utf-8 -*-
"""أخطاء وقت التشغيل في بيان"""


class ByanRuntimeError(Exception):
    """خطأ عام في وقت التشغيل"""
    pass


class ByanTypeError(ByanRuntimeError):
    """خطأ في النوع"""
    pass


class ByanIndexError(ByanRuntimeError):
    """خطأ في الفهرس"""
    pass


class ByanZeroDivisionError(ByanRuntimeError):
    """قسمة على صفر"""
    pass
