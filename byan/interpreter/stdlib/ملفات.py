# -*- coding: utf-8 -*-
"""وحدة الملفات"""

import os as _os
import shutil as _shutil


def اقرأ(مسار, ترميز="utf-8"):
    """قراءة ملف"""
    with open(مسار, 'r', encoding=ترميز) as f:
        return f.read()


def اكتب(مسار, محتوى, ترميز="utf-8"):
    """كتابة ملف"""
    د = _os.path.dirname(مسار)
    if د and not _os.path.exists(د):
        _os.makedirs(د, exist_ok=True)
    with open(مسار, 'w', encoding=ترميز) as f:
        f.write(str(محتوى))
    return True


def أضف(مسار, محتوى, ترميز="utf-8"):
    """إضافة لملف"""
    with open(مسار, 'a', encoding=ترميز) as f:
        f.write(str(محتوى))
    return True


def موجود(مسار):
    """هل موجود؟"""
    return _os.path.exists(مسار)


def احذف(مسار):
    """حذف"""
    if _os.path.isfile(مسار):
        _os.remove(مسار)
        return True
    if _os.path.isdir(مسار):
        _shutil.rmtree(مسار)
        return True
    return False


def قائمة(مجلد="."):
    """قائمة الملفات"""
    return _os.listdir(مجلد)


def انسخ(من, إلى):
    """نسخ"""
    _shutil.copy2(من, إلى)
    return True


def انقل(من, إلى):
    """نقل"""
    _shutil.move(من, إلى)
    return True


def حجم(مسار):
    """حجم بالبايت"""
    return _os.path.getsize(مسار)


def هو_ملف(مسار):
    """هل ملف؟"""
    return _os.path.isfile(مسار)


def هو_مجلد(مسار):
    """هل مجلد؟"""
    return _os.path.isdir(مسار)


def اسم_الملف(مسار):
    """اسم الملف"""
    return _os.path.basename(مسار)


def امتداد(مسار):
    """الامتداد"""
    return _os.path.splitext(مسار)[1]


def مجلد(مسار):
    """مسار المجلد"""
    return _os.path.dirname(مسار)


def الحالي():
    """المجلد الحالي"""
    return _os.getcwd()


FUNCTIONS = {
    'اقرأ': اقرأ,
    'اكتب': اكتب,
    'أضف': أضف,
    'موجود': موجود,
    'احذف': احذف,
    'قائمة': قائمة,
    'انسخ': انسخ,
    'انقل': انقل,
    'حجم': حجم,
    'هو_ملف': هو_ملف,
    'هو_مجلد': هو_مجلد,
    'اسم_الملف': اسم_الملف,
    'امتداد': امتداد,
    'مجلد': مجلد,
    'الحالي': الحالي,
}
