# -*- coding: utf-8 -*-
"""سجل وحدات المكتبة القياسية"""

MODULES = {}          # اسم الوحدة → dict {func_name: callable}
MODULE_INSTANCES = {} # cache


def register_module(name, functions):
    """يسجّل وحدة جديدة"""
    MODULES[name] = functions


def has_module(name):
    """هل الوحدة موجودة؟"""
    return name in MODULES


def get_module(name):
    """يرجّع كائن الوحدة"""
    if name not in MODULES:
        raise KeyError(f"الوحدة غير موجودة: '{name}'")
    if name not in MODULE_INSTANCES:
        MODULE_INSTANCES[name] = ModuleProxy(name)
    return MODULE_INSTANCES[name]


def list_modules():
    """قائمة بأسماء الوحدات"""
    return sorted(MODULES.keys())


def call_module_func(module_name, func_name, args):
    """يستدعي دالة من وحدة"""
    if module_name not in MODULES:
        raise KeyError(f"الوحدة غير موجودة: '{module_name}'")
    funcs = MODULES[module_name]
    if func_name not in funcs:
        raise KeyError(f"الدالة '{func_name}' غير موجودة في '{module_name}'")
    return funcs[func_name](*args)


class ModuleProxy:
    """كائن يمثّل وحدة — يدعم الوصول للدوال"""
    def __init__(self, name):
        self.__name__ = name
        self.__module_name__ = name

    def __getattr__(self, func_name):
        # نرجّع مرجع للدالة
        if func_name in MODULES[self.__module_name__]:
            return MODULES[self.__module_name__][func_name]
        raise AttributeError(f"الدالة '{func_name}' غير موجودة")

    def __repr__(self):
        funcs = ', '.join(sorted(MODULES[self.__module_name__].keys())[:5])
        return f"<وحدة {self.__module_name__}: {funcs}...>"
