# -*- coding: utf-8 -*-
"""مُفسِّر بيان — ينفذ شجرة AST مباشرة"""

import os
from .environment import Environment, ByanNameError
from .builtins import call_builtin, BUILTINS
from .errors import (
    ByanRuntimeError, ByanTypeError,
    ByanIndexError, ByanZeroDivisionError,
)
from .context import ReturnSignal, BreakSignal, ContinueSignal, ByanThrow
from .. import ast_nodes as ast


class Interpreter:
    """مُفسِّر بيان الأساسي"""

    def __init__(self, output_callback=None):
        """output_callback: دالة(نص) بديلة عن print"""
        self.globals = Environment()
        self.env = self.globals
        self.functions = {}       # اسم → FunctionDef
        self.classes = {}         # اسم → ClassDef
        self.output = output_callback or print
        self._running = False
        self._declared_globals = set()
        self._declared_nonlocals = set()

    # =====================================================
    # الدخول
    # =====================================================
    def run(self, program):
        """يبدأ تنفيذ البرنامج"""
        self._running = True

        # 1. اجمع تعريفات الدوال والفئات أولًا
        for el in program.elements:
            if isinstance(el, ast.FunctionDef):
                self.functions[el.name] = el
            elif isinstance(el, ast.ClassDef):
                self.classes[el.name] = el

        # 2. نفّذ باقي العناصر
        for el in program.elements:
            if isinstance(el, (ast.FunctionDef, ast.ClassDef)):
                continue  # اتجمعت فوق
            self.execute(el)

        self._running = False
        return None

    # =====================================================
    # تنفيذ statements
    # =====================================================
    def execute(self, node):
        """ينفذ statement — مش يرجّع قيمة"""
        if node is None:
            return

        # === تعريف دوال (متقدم: يدعم الدوال المتداخلة) ===
        if isinstance(node, ast.FunctionDef):
            self.env.define(node.name, node)
            return

        # === محلي/عالمي/غير_محلي ===
        if isinstance(node, ast.LocalDecl):
            value = self.evaluate(node.value) if node.value is not None else None
            self.env.define(node.name, value)
            return

        if isinstance(node, ast.GlobalDecl):
            # نضيف اسم للـ declared_globals
            if hasattr(self, '_declared_globals'):
                self._declared_globals.add(node.name)
            if node.value is not None:
                value = self.evaluate(node.value)
                self.env.define_global(node.name, value)
            return

        if isinstance(node, ast.NonlocalDecl):
            # نضيف اسم للـ declared_nonlocals
            if hasattr(self, '_declared_nonlocals'):
                self._declared_nonlocals.add(node.name)
            return

        # === متغيرات ===
        if isinstance(node, ast.VarDecl):
            value = self.evaluate(node.value)
            self.env.define(node.name, value)
            return

        if isinstance(node, ast.TypeDecl):
            value = self.evaluate(node.value) if node.value is not None else None
            # تحقق من النوع
            if node.type_hint and value is not None:
                actual = self._infer_type(value)
                if not self._type_matches(actual, node.type_hint):
                    raise ByanRuntimeError(
                        f"خطأ نوع: '{node.name}' متوقع '{node.type_hint}' "
                        f"لكن القيمة '{actual}'"
                    )
            self.env.define(node.name, value)
            # نخزّن النوع كـ metadata
            if not hasattr(self, '_type_info'):
                self._type_info = {}
            self._type_info[node.name] = node.type_hint or self._infer_type(value)
            return

        if isinstance(node, ast.ConstDecl):
            value = self.evaluate(node.value) if node.value is not None else None
            self.env.define(node.name, value)
            # نمنع التعديل
            if not hasattr(self, '_constants'):
                self._constants = set()
            self._constants.add(node.name)
            return

        if isinstance(node, ast.Assign):
            value = self.evaluate(node.value)
            # هل ثابت؟
            if node.name in getattr(self, '_constants', set()):
                raise ByanRuntimeError(f"لا يمكن تعديل الثابت '{node.name}'")
            # هل معرّف كـ global؟
            if node.name in getattr(self, '_declared_globals', set()):
                self.env.set_global(node.name, value)
            # هل معرّف كـ nonlocal؟
            elif node.name in getattr(self, '_declared_nonlocals', set()):
                self.env.set_nonlocal(node.name, value)
            else:
                self.env.set(node.name, value)
            return

        if isinstance(node, ast.CompoundAssign):
            self._handle_compound_assign(node)
            return

        if isinstance(node, ast.DictSet):
            self._handle_dict_set(node)
            return

        if isinstance(node, ast.MemberSet):
            self._handle_member_set(node)
            return

        if isinstance(node, ast.TryCatchFinally):
            self._handle_try(node)
            return

        if isinstance(node, ast.Import):
            self._handle_import(node)
            return

        if isinstance(node, ast.ThrowError):
            raise ByanThrow(self.evaluate(node.message) if not isinstance(node.message, str) else node.message)

        if isinstance(node, ast.MethodCall):
            self.evaluate(node)
            return

        if isinstance(node, ast.AddAssign):
            current = self.env.get(node.name)
            value = self.evaluate(node.value)
            self.env.set(node.name, current + value)
            return

        # === طباعة / دوال ===
        if isinstance(node, ast.FunctionCall):
            self.evaluate(node)
            return

        if isinstance(node, ast.BuiltinCall):
            self.evaluate(node)
            return

        # === تحكم ===
        if isinstance(node, ast.If):
            self._handle_if(node)
            return

        if isinstance(node, ast.While):
            self._handle_while(node)
            return

        if isinstance(node, ast.ForIn):
            self._handle_for_in(node)
            return

        if isinstance(node, ast.ForIndex):
            self._handle_for_index(node)
            return

        if isinstance(node, ast.ForDict):
            self._handle_for_dict(node)
            return

        if isinstance(node, ast.Break):
            raise BreakSignal()

        if isinstance(node, ast.Continue):
            raise ContinueSignal()

        if isinstance(node, ast.Return):
            value = None
            if node.value is not None:
                value = self.evaluate(node.value)
            raise ReturnSignal(value)

        # === غير مدعوم (UI أو API) ===
        # نتجاهلها بهدوء
        return

    # =====================================================
    # تقييم expressions
    # =====================================================
    def evaluate(self, node):
        """يقيّم expression — يرجّع قيمة"""
        if node is None:
            return None

        # === قيم حرفية ===
        if isinstance(node, ast.Number):
            return node.value

        if isinstance(node, ast.Bool):
            return node.value

        if isinstance(node, ast.String):
            return node.value

        if isinstance(node, ast.NullLit):
            return None

        # === قيم منطقية ===
        if isinstance(node, bool):
            return node

        if isinstance(node, (int, float, str)):
            return node

        # === مراجع ===
        if isinstance(node, ast.VarRef):
            try:
                return self.env.get(node.name)
            except ByanNameError as e:
                raise ByanRuntimeError(str(e))

        # === عمليات حسابية ===
        if isinstance(node, ast.BinOp):
            return self._handle_binop(node)

        if isinstance(node, ast.Compare):
            return self._handle_compare(node)

        # === قوائم ===
        if isinstance(node, ast.ListLiteral):
            return [self.evaluate(item) for item in node.items]

        # === قواميس ===
        if isinstance(node, ast.DictLiteral):
            result = {}
            for key_node, val_node in node.pairs:
                k = self.evaluate(key_node)
                v = self.evaluate(val_node)
                result[k] = v
            return result

        if isinstance(node, ast.IndexAccess):
            return self._handle_index(node)

        # === كائنات (OOP) ===
        if isinstance(node, ast.NewInstance):
            return self._handle_new_instance(node)

        if isinstance(node, ast.MemberAccess):
            return self._handle_member_access(node)

        if isinstance(node, ast.MethodCall):
            return self._handle_method_call(node)

        # === دوال ===
        if isinstance(node, ast.FunctionCall):
            return self._handle_function_call(node)

        if isinstance(node, ast.BuiltinCall):
            return self._handle_builtin_call(node)

        # === InputAsk ===
        if isinstance(node, ast.InputAsk):
            return self._builtin_input(node.prompt)

        # === افتراضي: نرجّع None ===
        return None

    # =====================================================
    # معالجات محددة
    # =====================================================
    def _handle_binop(self, node):
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)
        op = node.op

        # نص
        if isinstance(left, str) or isinstance(right, str):
            if op in ("+", "زائد"):
                return str(left) + str(right)

        # حسابي
        try:
            if op in ("+", "زائد"):
                return left + right
            if op in ("-", "ناقص"):
                return left - right
            if op in ("*", "في", "ضرب"):
                return left * right
            if op in ("/", "قسمة"):
                if right == 0:
                    raise ByanZeroDivisionError("قسمة على صفر")
                return left / right
            if op in ("%", "باقي"):
                return left % right
            if op in ("**", "أس"):
                return left ** right
            if op in ("//",):
                if right == 0:
                    raise ByanZeroDivisionError("قسمة على صفر")
                return left // right
        except ByanRuntimeError:
            raise
        except Exception as e:
            raise ByanRuntimeError(f"خطأ في العملية '{op}': {e}")

        raise ByanRuntimeError(f"عملية غير معروفة: '{op}'")

    def _handle_compare(self, node):
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)
        op = node.op

        if op in ("==", "يساوي"):
            return left == right
        if op in ("!=", "<>", "لا_يساوي"):
            return left != right
        if op in (">", "أكبر"):
            return left > right
        if op in ("<", "أصغر"):
            return left < right
        if op in (">=", "أكبر_أو_يساوي"):
            return left >= right
        if op in ("<=", "أصغر_أو_يساوي"):
            return left <= right

        raise ByanRuntimeError(f"مقارنة غير معروفة: '{op}'")

    def _handle_dict_set(self, node):
        """قاموس[مفتاح] = قيمة"""
        d = self.evaluate(node.dict_expr)
        k = self.evaluate(node.key)
        v = self.evaluate(node.value)
        if not isinstance(d, dict):
            raise ByanTypeError(f"لا يمكن الإسناد لفهرس '{type(d).__name__}'")
        d[k] = v

    def _handle_index(self, node):
        target = self.evaluate(node.target)
        idx = self.evaluate(node.index)
        try:
            return target[idx]
        except (IndexError, KeyError):
            raise ByanIndexError(f"فهرس خارج النطاق: {idx}")
        except TypeError as e:
            raise ByanTypeError(f"لا يمكن الفهرسة: {e}")

    def _handle_if(self, node):
        cond = self.evaluate(node.condition)
        if cond:
            for stmt in node.then_body:
                self.execute(stmt)
        else:
            for stmt in node.else_body:
                self.execute(stmt)

    def _handle_while(self, node):
        max_iter = 1_000_000  # حماية من الحلقات اللانهائية
        count = 0
        while self.evaluate(node.condition):
            count += 1
            if count > max_iter:
                raise ByanRuntimeError(
                    f"حلقة 'طالما' تجاوزت {max_iter} دورة — ممكن لانهائية"
                )
            try:
                for stmt in node.body:
                    self.execute(stmt)
            except BreakSignal:
                break
            except ContinueSignal:
                continue

    def _handle_for_in(self, node):
        iterable = self.evaluate(node.iterable)
        if iterable is None:
            raise ByanTypeError(f"لا يمكن التكرار على 'لا_شيء'")
        if not hasattr(iterable, "__iter__"):
            raise ByanTypeError(
                f"لا يمكن التكرار على '{type(iterable).__name__}'"
            )

        for item in iterable:
            self.env.set(node.var_name, item)
            try:
                for stmt in node.body:
                    self.execute(stmt)
            except BreakSignal:
                break
            except ContinueSignal:
                continue

    def _handle_for_index(self, node):
        iterable = self.evaluate(node.iterable)
        if iterable is None:
            return
        for i, item in enumerate(iterable):
            self.env.set(node.idx_name, i)
            self.env.set(node.var_name, item)
            try:
                for stmt in node.body:
                    self.execute(stmt)
            except BreakSignal:
                break
            except ContinueSignal:
                continue

    def _handle_for_dict(self, node):
        """لكل مفتاح, قيمة في قاموس: ..."""
        iterable = self.evaluate(node.dict_expr)
        if not isinstance(iterable, dict):
            raise ByanTypeError(f"لا يمكن التكرار على '{type(iterable).__name__}'")
        for k, v in iterable.items():
            self.env.set(node.key_name, k)
            self.env.set(node.val_name, v)
            try:
                for stmt in node.body:
                    self.execute(stmt)
            except BreakSignal:
                break
            except ContinueSignal:
                continue

    def _handle_compound_assign(self, node):
        current = self.env.get(node.name)
        value = self.evaluate(node.value)
        op = node.op

        if op in ("+=", "زائد_يساوي"):
            self.env.set(node.name, current + value)
        elif op in ("-=", "ناقص_يساوي"):
            self.env.set(node.name, current - value)
        elif op in ("*=", "ضرب_يساوي"):
            self.env.set(node.name, current * value)
        elif op in ("/=", "قسمة_يساوي"):
            if value == 0:
                raise ByanZeroDivisionError("قسمة على صفر")
            self.env.set(node.name, current / value)
        else:
            raise ByanRuntimeError(f"عملية مركبة غير معروفة: '{op}'")

    # =====================================================
    # الاستيراد
    # =====================================================
    def _handle_import(self, node):
        """استورد ملف أو وحدة مكتبة"""
        path = node.file_path

        # 1. وحدة stdlib؟
        try:
            from .stdlib import has_module, get_module
            if has_module(path):
                module = get_module(path)
                self.env.define(path, module)
                return
        except ImportError:
            pass

        # 2. ملف .byan — يتعالج في cli.py قبل التنفيذ
        # لو وصل هنا يعني مش اتدمج — نطبع تحذير
        # (بس ده مش بيحصل عادةً)

    # =====================================================
    # معالجة الأخطاء
    # =====================================================
    def _handle_try(self, node):
        """حاول/التقط/أخيرًا"""
        try:
            for stmt in node.body:
                self.execute(stmt)
        except ByanThrow as e:
            # اربط المتغير "خطأ" برسالة الخطأ
            self.env.define('خطأ', e.message)
            for stmt in node.catch_body:
                self.execute(stmt)
        except ByanRuntimeError as e:
            self.env.define('خطأ', str(e))
            for stmt in node.catch_body:
                self.execute(stmt)
        finally:
            for stmt in node.finally_body:
                self.execute(stmt)

    # =====================================================
    # OOP Handlers
    # =====================================================
    def _get_class_chain(self, cls):
        """يرجّع سلسلة الوراثة: [الأب الأعلى, ..., الفئة]"""
        chain = []
        seen = set()
        cur = cls
        while cur is not None and id(cur) not in seen:
            seen.add(id(cur))
            chain.insert(0, cur)  # نضيف في الأول
            if cur.extends:
                cur = self.classes.get(cur.extends)
            else:
                break
        return chain

    def _find_in_chain(self, cls, attr):
        """يبحث عن field أو method في سلسلة الوراثة"""
        cur = cls
        seen = set()
        while cur is not None and id(cur) not in seen:
            seen.add(id(cur))
            for f in cur.fields:
                if f.name == attr:
                    return ('field', f)
            for m in cur.methods:
                if m.name == attr:
                    return ('method', m)
            if cur.extends:
                cur = self.classes.get(cur.extends)
            else:
                break
        return (None, None)

    def _find_method_in_chain(self, cls, method_name):
        """يبحث عن method بس في السلسلة"""
        cur = cls
        seen = set()
        while cur is not None and id(cur) not in seen:
            seen.add(id(cur))
            for m in cur.methods:
                if m.name == method_name:
                    return m
            if cur.extends:
                cur = self.classes.get(cur.extends)
            else:
                break
        return None

    def _handle_new_instance(self, node):
        """جديد صنف(وسائط)"""
        cls = self.classes.get(node.class_name)
        if cls is None:
            raise ByanRuntimeError(f"الفئة غير معروفة: '{node.class_name}'")
        instance = {
            '__class__': cls,
            '__fields__': {},
        }

        # اجمع حقول الأب ثم الابن (الابن ياخد أولوية)
        chain = self._get_class_chain(cls)
        for c in chain:
            for field in c.fields:
                value = self.evaluate(field.value)
                instance['__fields__'][field.name] = value

        # ابحث عن method هيئ في السلسلة (الابن أولوية)
        init_method = self._find_method_in_chain(cls, 'هيئ')
        if init_method is None:
            init_method = self._find_method_in_chain(cls, '__init__')
        if init_method is None:
            init_method = self._find_method_in_chain(cls, 'init')

        # نفّذ هيئ
        if init_method is not None:
            args = [self.evaluate(a) for a in node.args]
            self._call_method(instance, init_method, args)

        return instance

    def _handle_member_access(self, node):
        """هذا.اسم أو كائن.خاصية أو وحدة.دالة"""
        obj = self.evaluate(node.obj)

        # وحدة stdlib
        try:
            from .stdlib.registry import ModuleProxy, MODULES
            if isinstance(obj, ModuleProxy):
                mod_name = obj.__module_name__
                if node.attr in MODULES.get(mod_name, {}):
                    # نرجّع مرجع للدالة
                    return ('__module_func__', mod_name, node.attr)
                raise ByanRuntimeError(f"الدالة '{node.attr}' غير موجودة في '{mod_name}'")
        except ImportError:
            pass

        if isinstance(obj, dict) and '__fields__' in obj:
            fields = obj['__fields__']
            if node.attr in fields:
                return fields[node.attr]
            # يمكن method — ابحث في السلسلة
            cls = obj.get('__class__')
            if cls:
                kind, found = self._find_in_chain(cls, node.attr)
                if found is not None:
                    return found
            raise ByanRuntimeError(f"الخاصية غير موجودة: '{node.attr}'")
        # قاموس عادي
        if isinstance(obj, dict):
            if node.attr in obj:
                return obj[node.attr]
            raise ByanRuntimeError(f"المفتاح غير موجود: '{node.attr}'")
        raise ByanRuntimeError(f"لا يمكن الوصول لـ '{node.attr}' من '{type(obj).__name__}'")

    def _handle_member_set(self, node):
        """هذا.اسم = قيمة"""
        obj = self.evaluate(node.obj)
        value = self.evaluate(node.value)
        if isinstance(obj, dict) and '__fields__' in obj:
            obj['__fields__'][node.attr] = value
            return
        if isinstance(obj, dict):
            obj[node.attr] = value
            return
        raise ByanRuntimeError(f"لا يمكن الإسناد لـ '{node.attr}'")

    def _handle_method_call(self, node):
        """كائن.دالة(وسائط) أو أساس(وسائط) أو وحدة.دالة(وسائط)"""
        obj = self.evaluate(node.obj)

        # وحدة stdlib
        try:
            from .stdlib.registry import ModuleProxy, call_module_func
            if isinstance(obj, ModuleProxy):
                args = [self.evaluate(a) for a in node.args]
                return call_module_func(obj.__module_name__, node.method, args)
        except ImportError:
            pass

        args = [self.evaluate(a) for a in node.args]

        if isinstance(obj, dict) and '__class__' in obj:
            cls = obj['__class__']

            # أساس(...) — super call: استدعي method الأب
            if node.method == 'أساس':
                # ابحث عن method الأب اللي بيستدعيها
                # نحتاج نعرف اسم method الأب الحالية
                parent_name = cls.extends
                if not parent_name:
                    raise ByanRuntimeError("لا يوجد أب للفئة")
                parent_cls = self.classes.get(parent_name)
                if parent_cls is None:
                    raise ByanRuntimeError(f"الفئة الأب غير موجودة: '{parent_name}'")
                # نستدعي 'هيئ' الأب (الأكثر شيوعًا)
                init_method = self._find_method_in_chain(parent_cls, 'هيئ')
                if init_method is None:
                    init_method = self._find_method_in_chain(parent_cls, '__init__')
                if init_method is None:
                    raise ByanRuntimeError("لا يوجد هيئ في الفئة الأب")
                return self._call_method(obj, init_method, args)

            # عادي — ابحث في السلسلة
            m = self._find_method_in_chain(cls, node.method)
            if m is not None:
                return self._call_method(obj, m, args)
            raise ByanRuntimeError(f"الدالة غير موجودة: '{node.method}'")

        raise ByanRuntimeError(f"لا يمكن نداء '{node.method}'")

    def _call_method(self, instance, method_def, args):
        """نفّذ method على instance"""
        old_env = self.env
        old_globals = getattr(self, '_declared_globals', set())
        old_nonlocals = getattr(self, '_declared_nonlocals', set())
        self.env = old_env.child()
        self._declared_globals = set()
        self._declared_nonlocals = set()
        # اربط هذا
        self.env.define('هذا', instance)
        # اربط الوسائط
        for i, pname in enumerate(method_def.params):
            if i < len(args):
                self.env.define(pname, args[i])
            else:
                self.env.define(pname, None)
        # نفّذ
        result = None
        try:
            for stmt in method_def.body:
                self.execute(stmt)
        except ReturnSignal as r:
            result = r.value
        finally:
            self.env = old_env
            self._declared_globals = old_globals
            self._declared_nonlocals = old_nonlocals
        return result

    def _handle_function_call(self, node):
        # 1. دوال من env (محلي + parent chain)
        fn = None
        if self.env.has(node.name):
            candidate = self.env.get(node.name)
            if isinstance(candidate, ast.FunctionDef):
                fn = candidate

        # 2. دوال من functions dict (global)
        if fn is None and node.name in self.functions:
            fn = self.functions[node.name]

        if fn is not None:
            args = [self.evaluate(a) for a in node.args]

            # scope جديد
            old_env = self.env
            old_globals = getattr(self, '_declared_globals', set())
            old_nonlocals = getattr(self, '_declared_nonlocals', set())
            self.env = old_env.child()
            self._declared_globals = set()
            self._declared_nonlocals = set()

            # اربط المعاملات
            for i, pname in enumerate(fn.params):
                if i < len(args):
                    self.env.define(pname, args[i])
                else:
                    self.env.define(pname, None)

            # نفّذ
            result = None
            old_globals = getattr(self, '_declared_globals', set())
            old_nonlocals = getattr(self, '_declared_nonlocals', set())
            self._declared_globals = set()
            self._declared_nonlocals = set()
            try:
                for stmt in fn.body:
                    self.execute(stmt)
            except ReturnSignal as r:
                result = r.value
            finally:
                self.env = old_env
                self._declared_globals = old_globals
                self._declared_nonlocals = old_nonlocals

            return result

        # 3. لو builtin
        if node.name in BUILTINS:
            args = [self.evaluate(a) for a in node.args]
            return call_builtin(node.name, args)

        # 4. نادِ — metaprogramming (يحتاج access للـ interpreter)
        if node.name == 'نادِ':
            args = [self.evaluate(a) for a in node.args]
            if len(args) < 2:
                raise ByanRuntimeError("نادِ() محتاج كائن واسم method")
            obj = args[0]
            method_name = str(args[1])
            extra_args = args[2] if len(args) > 2 and isinstance(args[2], list) else []
            if not isinstance(obj, dict) or '__class__' not in obj:
                raise ByanRuntimeError("نادِ() محتاج كائن فئة")
            cls = obj['__class__']
            m = self._find_method_in_chain(cls, method_name)
            if m is None:
                raise ByanRuntimeError(f"الدالة '{method_name}' غير موجودة")
            return self._call_method(obj, m, extra_args)

        # 5. غير معروف
        raise ByanRuntimeError(f"دالة غير معروفة: '{node.name}'")

    def _handle_builtin_call(self, node):
        # معالجة خاصة لـ نادِ (يحتاج access لـ interpreter)
        if node.name == 'نادِ':
            args = [self.evaluate(a) for a in node.args]
            if len(args) < 2:
                raise ByanRuntimeError("نادِ() محتاج كائن واسم method")
            obj = args[0]
            method_name = str(args[1])
            extra_args = args[2] if len(args) > 2 and isinstance(args[2], list) else []
            if not isinstance(obj, dict) or '__class__' not in obj:
                raise ByanRuntimeError("نادِ() محتاج كائن فئة")
            cls = obj['__class__']
            m = self._find_method_in_chain(cls, method_name)
            if m is None:
                raise ByanRuntimeError(f"الدالة '{method_name}' غير موجودة")
            return self._call_method(obj, m, extra_args)

        args = [self.evaluate(a) for a in node.args]
        return call_builtin(node.name, args)

    # =====================================================
    # Type System
    # =====================================================
    def _infer_type(self, value):
        """يستنتج نوع القيمة"""
        if value is None:
            return "لا_شيء"
        if isinstance(value, bool):
            return "منطقي"
        if isinstance(value, int):
            return "عدد"
        if isinstance(value, float):
            return "عدد_عشري"
        if isinstance(value, str):
            return "نص"
        if isinstance(value, list):
            return "قائمة"
        if isinstance(value, dict):
            if '__class__' in value:
                cls = value['__class__']
                return cls.name if hasattr(cls, 'name') else "كائن"
            return "قاموس"
        if callable(value):
            return "دالة"
        return type(value).__name__

    def _type_matches(self, actual, declared):
        """هل النوع الفعلي يطابق المعلن؟"""
        if not declared:
            return True
        # aliases
        aliases = {
            "عدد": {"عدد", "int", "عدد_صحيح", "رقم"},
            "عدد_عشري": {"عدد_عشري", "float", "عشري"},
            "نص": {"نص", "str", "string"},
            "منطقي": {"منطقي", "bool"},
            "قائمة": {"قائمة", "list"},
            "قاموس": {"قاموس", "dict"},
            "لا_شيء": {"لا_شيء", "none", "null"},
            "أي": set(),  # أي نوع
        }
        if declared in ("أي", "any"):
            return True
        if declared in aliases:
            return actual in aliases[declared]
        # نوع مخصص (فئة)
        return actual == declared

    def _builtin_input(self, prompt):
        try:
            return input(str(prompt))
        except EOFError:
            return ""
