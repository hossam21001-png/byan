# -*- coding: utf-8 -*-
"""وحدة النظام"""

import os as _os
import sys as _sys
import platform as _platform
import subprocess as _sub


def نفّذ(أمر):
    """تنفيذ أمر shell"""
    try:
        result = _sub.run(أمر, shell=True, capture_output=True, text=True)
        return {
            'نجح': result.returncode == 0,
            'خرج': result.stdout,
            'خطأ': result.stderr,
            'كود': result.returncode,
        }
    except Exception as e:
        return {'نجح': False, 'خرج': '', 'خطأ': str(e), 'كود': -1}


def متغير(اسم, افتراضي=None):
    """متغير بيئة"""
    return _os.environ.get(str(اسم), افتراضي)


def ضع_متغير(اسم, قيمة):
    """تعيين متغير بيئة"""
    _os.environ[str(اسم)] = str(قيمة)
    return True


def نظام_التشغيل():
    """اسم النظام"""
    return _platform.system()


def معمارية():
    """المعمارية"""
    return _platform.machine()


def إصدار():
    """إصدار بايثون"""
    return _sys.version


def وسائط():
    """وسائط سطر الأوامر"""
    return list(_sys.argv)


def اخرج(كود=0):
    """إنهاء"""
    _sys.exit(int(كود))


def مجلد_العمل():
    """cwd"""
    return _os.getcwd()


def غيّر_مجلد(مسار):
    """cd"""
    _os.chdir(مسار)
    return True


def متغيرات_البيئة():
    """كل متغيرات البيئة"""
    return dict(_os.environ)


FUNCTIONS = {
    'نفّذ': نفّذ,
    'متغير': متغير,
    'ضع_متغير': ضع_متغير,
    'نظام_التشغيل': نظام_التشغيل,
    'معمارية': معمارية,
    'إصدار': إصدار,
    'وسائط': وسائط,
    'اخرج': اخرج,
    'مجلد_العمل': مجلد_العمل,
    'غيّر_مجلد': غيّر_مجلد,
    'متغيرات_البيئة': متغيرات_البيئة,
}
