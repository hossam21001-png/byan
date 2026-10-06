#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# مولّد تلقائيًا من Byan — اختبار_compiler

from byan_rt import *
import byan_rt

def جمع(أ, ب):
    return (أ + ب)

def __main__():
    س = 5
    اسم = 'أحمد'
    اعرض('مرحبا', اسم)
    اعرض('س =', س)
    if (س > 3):
        اعرض('س أكبر من 3')
    else:
        اعرض('س أصغر')
    for i in [1, 2, 3]:
        اعرض(i)
    اعرض('5 + 7 =', جمع(5, 7))

if __name__ == "__main__":
    byan_run(__main__)