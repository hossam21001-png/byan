# -*- coding: utf-8 -*-
"""وحدة JSON"""

import json as _json


def حلّل(نص):
    """parse JSON"""
    return _json.loads(str(نص))


def حوّل(كائن, جميل=False):
    """stringify"""
    if جميل:
        return _json.dumps(كائن, ensure_ascii=False, indent=2)
    return _json.dumps(كائن, ensure_ascii=False)


def قراءة(مسار):
    """قراءة ملف JSON"""
    with open(مسار, 'r', encoding='utf-8') as f:
        return _json.load(f)


def كتابة(مسار, كائن, جميل=True):
    """كتابة ملف JSON"""
    with open(مسار, 'w', encoding='utf-8') as f:
        _json.dump(كائن, f, ensure_ascii=False, indent=2 if جميل else None)
    return True


def صحيح(نص):
    """هل JSON صحيح؟"""
    try:
        _json.loads(str(نص))
        return True
    except (ValueError, TypeError):
        return False


FUNCTIONS = {
    'حلّل': حلّل,
    'حوّل': حوّل,
    'قراءة': قراءة,
    'كتابة': كتابة,
    'صحيح': صحيح,
    'parse': حلّل,      # alias
    'stringify': حوّل,  # alias
}
