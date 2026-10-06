# -*- coding: utf-8 -*-
"""حالة التنفيذ — للتحكم في break/continue/return"""


class LoopContext:
    """حالة الحلقة الحالية"""
    def __init__(self):
        self.break_flag = False
        self.continue_flag = False

    def reset(self):
        self.break_flag = False
        self.continue_flag = False


class ReturnSignal(Exception):
    """إشارة داخلية لـ return — تُلتقط في FunctionCall"""
    def __init__(self, value):
        self.value = value
        super().__init__(f"return({value})")


class BreakSignal(Exception):
    """إشارة داخلية لـ break — تُلتقط في While/For"""
    pass


class ContinueSignal(Exception):
    """إشارة داخلية لـ continue — تُلتقط في While/For"""
    pass


class ByanThrow(Exception):
    """إشارة خطأ داخلية — تُلتقط في TryCatchFinally"""
    def __init__(self, message):
        self.message = message
        super().__init__(f"خطأ: {message}")
