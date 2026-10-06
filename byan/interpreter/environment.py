# -*- coding: utf-8 -*-
"""بيئة المتغيرات — تدعم scope chain (والد ← ابن)"""


class ByanNameError(Exception):
    """خطأ: متغير غير معرّف"""
    pass


class Environment:
    """بيئة متغيرات. لو فيه parent، البحث يكون تصاعديًا."""

    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent

    def define(self, name, value):
        """يعرّف متغير في البيئة الحالية (يتجاوز لو موجود)"""
        self.vars[name] = value
        return value

    def get(self, name):
        """يبحث عن متغير — لو مش موجود هنا، يدور في الوالد"""
        if name in self.vars:
            return self.vars[name]
        if self.parent is not None:
            return self.parent.get(name)
        raise ByanNameError(f"المتغير '{name}' غير معرّف")

    def set(self, name, value):
        """يحدّث متغير موجود — لو مش موجود، يعرّفه هنا"""
        if name in self.vars:
            self.vars[name] = value
            return value
        # حاول في الوالد
        env = self.parent
        while env is not None:
            if name in env.vars:
                env.vars[name] = value
                return value
            env = env.parent
        # مش موجود في أي مكان → عرّفه هنا
        self.vars[name] = value
        return value

    def has(self, name):
        """هل المتغير معرّف؟ (بحث تصاعدي)"""
        if name in self.vars:
            return True
        if self.parent is not None:
            return self.parent.has(name)
        return False

    def child(self):
        """ينشئ بيئة ابن (للـ function scope)"""
        return Environment(parent=self)

    def root(self):
        """يرجّع البيئة الجذر (global)"""
        env = self
        while env.parent is not None:
            env = env.parent
        return env

    def define_global(self, name, value):
        """يعرّف في البيئة الجذر"""
        root = self.root()
        root.vars[name] = value
        return value

    def set_global(self, name, value):
        """يحدّث متغير في الجذر"""
        root = self.root()
        if name not in root.vars:
            raise ByanNameError(f"المتغير العام '{name}' غير معرّف")
        root.vars[name] = value
        return value

    def set_nonlocal(self, name, value):
        """يحدّث متغير في الأب (مش الجذر)"""
        env = self.parent
        while env is not None:
            if name in env.vars:
                env.vars[name] = value
                return value
            env = env.parent
        raise ByanNameError(f"المتغير '{name}' غير موجود في الأب")

    def __repr__(self):
        return f"Environment({list(self.vars.keys())})"
