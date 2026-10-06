# -*- coding: utf-8 -*-
"""وحدة CSV"""

import csv as _csv


def قراءة(مسار):
    """قراءة CSV → قائمة قوائم"""
    with open(مسار, 'r', encoding='utf-8', newline='') as f:
        return [row for row in _csv.reader(f)]


def كتابة(مسار, صفوف):
    """كتابة CSV"""
    with open(مسار, 'w', encoding='utf-8', newline='') as f:
        writer = _csv.writer(f)
        for row in صفوف:
            writer.writerow(row)
    return True


def قراءة_قاموس(مسار):
    """قراءة CSV → قائمة قواميس"""
    with open(مسار, 'r', encoding='utf-8', newline='') as f:
        return [dict(row) for row in _csv.DictReader(f)]


def كتابة_قاموس(مسار, قائمة_قواميس):
    """كتابة قائمة قواميس"""
    if not قائمة_قواميس:
        return False
    with open(مسار, 'w', encoding='utf-8', newline='') as f:
        fieldnames = list(قائمة_قواميس[0].keys())
        writer = _csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in قائمة_قواميس:
            writer.writerow(row)
    return True


FUNCTIONS = {
    'قراءة': قراءة,
    'كتابة': كتابة,
    'قراءة_قاموس': قراءة_قاموس,
    'كتابة_قاموس': كتابة_قاموس,
}
