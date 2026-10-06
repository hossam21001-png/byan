# -*- coding: utf-8 -*-
"""وحدة التشفير"""

import hashlib as _hash
import base64 as _b64
import uuid as _uuid


def md5(نص):
    """MD5"""
    return _hash.md5(str(نص).encode('utf-8')).hexdigest()


def sha1(نص):
    """SHA1"""
    return _hash.sha1(str(نص).encode('utf-8')).hexdigest()


def sha256(نص):
    """SHA256"""
    return _hash.sha256(str(نص).encode('utf-8')).hexdigest()


def تشفير_base64(نص):
    """base64 encode"""
    return _b64.b64encode(str(نص).encode('utf-8')).decode('ascii')


def فك_base64(نص):
    """base64 decode"""
    return _b64.b64decode(str(نص).encode('ascii')).decode('utf-8')


def معرف_فريد():
    """UUID4"""
    return str(_uuid.uuid4())


def معرف_قصير():
    """UUID قصير (8 حروف)"""
    return str(_uuid.uuid4())[:8]


FUNCTIONS = {
    'md5': md5,
    'sha1': sha1,
    'sha256': sha256,
    'تشفير_base64': تشفير_base64,
    'فك_base64': فك_base64,
    'معرف_فريد': معرف_فريد,
    'معرف_قصير': معرف_قصير,
}
