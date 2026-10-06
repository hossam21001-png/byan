# -*- coding: utf-8 -*-
"""وحدة الوقت"""

import time as _time
import datetime as _dt


def الآن():
    """الآن كنص"""
    return _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def اليوم():
    """تاريخ اليوم"""
    return _dt.date.today().isoformat()


def انتظر(ثواني):
    """تأخير"""
    _time.sleep(float(ثواني))
    return True


def طابع_زمني():
    """timestamp"""
    return _time.time()


def سنة():
    return _dt.datetime.now().year


def شهر():
    return _dt.datetime.now().month


def يوم():
    return _dt.datetime.now().day


def ساعة():
    return _dt.datetime.now().hour


def دقيقة():
    return _dt.datetime.now().minute


def ثانية():
    return _dt.datetime.now().second


def نسّق(طابع, نمط="%Y-%m-%d %H:%M:%S"):
    """تنسيق timestamp"""
    return _dt.datetime.fromtimestamp(طابع).strftime(نمط)


def فرق(طابع1, طابع2):
    """الفرق بالثواني"""
    return abs(float(طابع1) - float(طابع2))


def مؤقت():
    """بدء مؤقت — يرجّع timestamp"""
    return _time.time()


FUNCTIONS = {
    'الآن': الآن,
    'اليوم': اليوم,
    'انتظر': انتظر,
    'طابع_زمني': طابع_زمني,
    'سنة': سنة,
    'شهر': شهر,
    'يوم': يوم,
    'ساعة': ساعة,
    'دقيقة': دقيقة,
    'ثانية': ثانية,
    'نسّق': نسّق,
    'فرق': فرق,
    'مؤقت': مؤقت,
}
