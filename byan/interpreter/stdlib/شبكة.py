# -*- coding: utf-8 -*-
"""وحدة الشبكة"""


def جلب(رابط, رأسيات=None):
    """HTTP GET — يرجّع نص"""
    try:
        import urllib.request
        req = urllib.request.Request(رابط)
        if رأسيات:
            for k, v in رأسيات.items():
                req.add_header(k, v)
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode('utf-8')
    except Exception as e:
        raise RuntimeError(f"فشل الجلب: {e}")


def إرسال(رابط, بيانات=None, نوع="json"):
    """HTTP POST"""
    try:
        import urllib.request
        import json as _json
        if نوع == "json" and isinstance(بيانات, (dict, list)):
            payload = _json.dumps(بيانات).encode('utf-8')
            headers = {'Content-Type': 'application/json'}
        else:
            payload = str(بيانات or "").encode('utf-8')
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        req = urllib.request.Request(رابط, data=payload, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode('utf-8')
    except Exception as e:
        raise RuntimeError(f"فشل الإرسال: {e}")


def نزّل(رابط, مسار):
    """تنزيل ملف"""
    try:
        import urllib.request
        urllib.request.urlretrieve(رابط, مسار)
        return True
    except Exception as e:
        raise RuntimeError(f"فشل التنزيل: {e}")


def فك_json(نص):
    """decode JSON"""
    import json as _json
    return _json.loads(نص)


FUNCTIONS = {
    'جلب': جلب,
    'إرسال': إرسال,
    'نزّل': نزّل,
    'فك_json': فك_json,
    'get': جلب,        # alias
    'post': إرسال,     # alias
    'download': نزّل,  # alias
}
