# -*- coding: utf-8 -*-
"""المكتبة القياسية لبيان — 12 وحدة"""

from .registry import (
    get_module, list_modules, has_module,
    call_module_func, MODULES, register_module,
)

# ============ تسجيل كل الوحدات ============

from . import رياضيات as _رياضيات
register_module('رياضيات', _رياضيات.FUNCTIONS)

from . import نصوص as _نصوص
register_module('نصوص', _نصوص.FUNCTIONS)

from . import قوائم as _قوائم
register_module('قوائم', _قوائم.FUNCTIONS)

from . import قواميس as _قواميس
register_module('قواميس', _قواميس.FUNCTIONS)

from . import ملفات as _ملفات
register_module('ملفات', _ملفات.FUNCTIONS)

from . import وقت as _وقت
register_module('وقت', _وقت.FUNCTIONS)

from . import عشوائي as _عشوائي
register_module('عشوائي', _عشوائي.FUNCTIONS)

from . import نظام as _نظام
register_module('نظام', _نظام.FUNCTIONS)

from . import JSON as _JSON
register_module('JSON', _JSON.FUNCTIONS)

from . import CSV as _CSV
register_module('CSV', _CSV.FUNCTIONS)

from . import تشفير as _تشفير
register_module('تشفير', _تشفير.FUNCTIONS)

from . import شبكة as _شبكة
register_module('شبكة', _شبكة.FUNCTIONS)

__all__ = [
    "get_module", "list_modules", "has_module",
    "call_module_func", "MODULES", "register_module",
]
