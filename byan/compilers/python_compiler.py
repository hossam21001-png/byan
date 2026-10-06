# -*- coding: utf-8 -*-
"""مترجم بيان → Python

يحوّل AST البرنامج إلى كود Python source.
يدعم 3 أنماط:
  - standalone: ملف واحد مدمج
  - split: ملف الكود + byan_rt.py
  - library: يعتمد على مكتبة byan
"""

import os
from .base import BaseCompiler
from .. import ast_nodes as ast


class PythonCompiler(BaseCompiler):
    """يحوّل Byan AST إلى Python source"""

    def __init__(self, program, mode='split', rt_path='byan_rt'):
        super().__init__(program)
        self.mode = mode
        self.rt_path = rt_path
        self.temp_counter = 0

    def _temp(self, prefix='_t'):
        """يولّد اسم متغير مؤقت"""
        self.temp_counter += 1
        return f"{prefix}{self.temp_counter}"

    # ========================================================
    # الدخول
    # ========================================================
    def compile(self):
        """يترجم البرنامج كامل"""
        # 1. الرأس
        self._emit_header()
        
        # 2. جمع الدوال والفئات
        for el in self.program.elements:
            if isinstance(el, ast.FunctionDef):
                self.functions[el.name] = el
            elif isinstance(el, ast.ClassDef):
                self.classes[el.name] = el
        
        # 3. توليد الفئات
        for el in self.program.elements:
            if isinstance(el, ast.ClassDef):
                self._compile_class(el)
                self.emit("")
        
        # 4. توليد الدوال العادية
        for el in self.program.elements:
            if isinstance(el, ast.FunctionDef):
                self._compile_function(el)
                self.emit("")
        
        # 5. main function للكود الرئيسي
        self.emit("def __main__():")
        self.indent()
        has_main_body = False
        for el in self.program.elements:
            if isinstance(el, (ast.FunctionDef, ast.ClassDef)):
                continue
            if isinstance(el, ast.Import):
                # الاستيراد ينفّذ على المستوى العام
                continue
            self._compile_statement(el)
            has_main_body = True
        if not has_main_body:
            self.emit("pass")
        self.dedent()
        
        # 6. نقطة الدخول
        self.emit("")
        self.emit('if __name__ == "__main__":')
        self.indent()
        self.emit("byan_run(__main__)")
        self.dedent()
        
        return self.get_output()

    def _emit_header(self):
        """يكتب رأس الملف"""
        self.emit("#!/usr/bin/env python3")
        self.emit("# -*- coding: utf-8 -*-")
        self.emit(f"# مولّد تلقائيًا من Byan — {self.program.name or 'برنامج'}")
        self.emit("")
        
        if self.mode == 'standalone':
            # ملف واحد — نضمّن كل الـ runtime
            # (لاحقًا)
            self.emit("# ⚠️ standalone mode — قيد التطوير")
            self.emit("from byan_rt import *")
        elif self.mode == 'split':
            # ملفان
            self.emit("from byan_rt import *")
            self.emit("import byan_rt")
        elif self.mode == 'library':
            # يعتمد على مكتبة byan
            self.emit("from byan.interpreter import stdlib as _stdlib")
            self.emit("from byan_rt import *")
        
        self.emit("")

    # ========================================================
    # الفئات
    # ========================================================
    def _compile_class(self, node):
        """class X:"""
        base = f"({node.extends})" if node.extends else ""
        self.emit(f"class {node.name}{base}:")
        self.indent()
        
        # الحقول كـ class attributes
        if not node.methods and not node.fields:
            self.emit("pass")
        else:
            # __init__ من الحقول
            if node.fields:
                self.emit("def __init__(self):")
                self.indent()
                for f in node.fields:
                    val = self._compile_expression(f.value) if f.value else "None"
                    self.emit(f"self.{f.name} = {val}")
                self.dedent()
                self.emit("")
            
            # الدوال
            for m in node.methods:
                # لو اسمها 'هيئ' → __init__
                name = '__init__' if m.name in ('هيئ', '__init__') else m.name
                params = ['self'] + list(m.params)
                self.emit(f"def {name}({', '.join(params)}):")
                self.indent()
                if not m.body:
                    self.emit("pass")
                else:
                    for stmt in m.body:
                        self._compile_statement(stmt)
                self.dedent()
                self.emit("")
        
        self.dedent()

    # ========================================================
    # الدوال
    # ========================================================
    def _compile_function(self, node):
        """def f():"""
        params = ', '.join(node.params)
        self.emit(f"def {node.name}({params}):")
        self.indent()
        if not node.body:
            self.emit("pass")
        else:
            for stmt in node.body:
                self._compile_statement(stmt)
        self.dedent()

    # ========================================================
    # الجمل (Statements)
    # ========================================================
    def _compile_statement(self, node):
        if node is None:
            return
        
        # متغير
        if isinstance(node, ast.VarDecl):
            val = self._compile_expression(node.value) if node.value else "None"
            self.emit(f"{node.name} = {val}")
            return
        
        # TypeDecl (متغير مع نوع)
        if isinstance(node, ast.TypeDecl):
            val = self._compile_expression(node.value) if node.value else "None"
            self.emit(f"{node.name} = {val}")
            return
        
        # ConstDecl (ثابت)
        if isinstance(node, ast.ConstDecl):
            val = self._compile_expression(node.value) if node.value else "None"
            self.emit(f"{node.name} = {val}")
            return
        
        # LocalDecl / GlobalDecl
        if isinstance(node, ast.LocalDecl):
            val = self._compile_expression(node.value) if node.value else "None"
            self.emit(f"{node.name} = {val}")
            return
        
        if isinstance(node, ast.GlobalDecl):
            self.emit(f"global {node.name}")
            if node.value is not None:
                val = self._compile_expression(node.value)
                self.emit(f"{node.name} = {val}")
            return
        
        if isinstance(node, ast.NonlocalDecl):
            self.emit(f"nonlocal {node.name}")
            return
        
        # إسناد
        if isinstance(node, ast.Assign):
            val = self._compile_expression(node.value)
            self.emit(f"{node.name} = {val}")
            return
        
        # إسناد مركب
        if isinstance(node, ast.CompoundAssign):
            val = self._compile_expression(node.value)
            self.emit(f"{node.name} {node.op} {val}")
            return
        
        if isinstance(node, ast.AddAssign):
            val = self._compile_expression(node.value)
            self.emit(f"{node.name} += {val}")
            return
        
        # نداء دالة
        if isinstance(node, ast.FunctionCall):
            self.emit(self._compile_expression(node))
            return
        
        if isinstance(node, ast.BuiltinCall):
            self.emit(self._compile_expression(node))
            return
        
        # شرط
        if isinstance(node, ast.If):
            cond = self._compile_expression(node.condition)
            self.emit(f"if {cond}:")
            self.indent()
            if not node.then_body:
                self.emit("pass")
            else:
                for s in node.then_body:
                    self._compile_statement(s)
            self.dedent()
            if node.else_body:
                self.emit("else:")
                self.indent()
                for s in node.else_body:
                    self._compile_statement(s)
                self.dedent()
            return
        
        # حلقة while
        if isinstance(node, ast.While):
            cond = self._compile_expression(node.condition)
            self.emit(f"while {cond}:")
            self.indent()
            if not node.body:
                self.emit("pass")
            else:
                for s in node.body:
                    self._compile_statement(s)
            self.dedent()
            return
        
        # حلقة for
        if isinstance(node, ast.ForIn):
            iterable = self._compile_expression(node.iterable)
            self.emit(f"for {node.var_name} in {iterable}:")
            self.indent()
            if not node.body:
                self.emit("pass")
            else:
                for s in node.body:
                    self._compile_statement(s)
            self.dedent()
            return
        
        if isinstance(node, ast.ForIndex):
            iterable = self._compile_expression(node.iterable)
            self.emit(f"for {node.idx_name}, {node.var_name} in enumerate({iterable}):")
            self.indent()
            if not node.body:
                self.emit("pass")
            else:
                for s in node.body:
                    self._compile_statement(s)
            self.dedent()
            return
        
        if isinstance(node, ast.ForDict):
            iterable = self._compile_expression(node.dict_expr)
            self.emit(f"for {node.key_name}, {node.val_name} in {iterable}.items():")
            self.indent()
            if not node.body:
                self.emit("pass")
            else:
                for s in node.body:
                    self._compile_statement(s)
            self.dedent()
            return
        
        # break / continue
        if isinstance(node, ast.Break):
            self.emit("break")
            return
        
        if isinstance(node, ast.Continue):
            self.emit("continue")
            return
        
        # return
        if isinstance(node, ast.Return):
            if node.value is not None:
                val = self._compile_expression(node.value)
                self.emit(f"return {val}")
            else:
                self.emit("return")
            return
        
        # حاول/التقط/أخيرًا
        if isinstance(node, ast.TryCatchFinally):
            self.emit("try:")
            self.indent()
            if not node.body:
                self.emit("pass")
            else:
                for s in node.body:
                    self._compile_statement(s)
            self.dedent()
            
            if node.catch_body:
                self.emit("except ByanThrow as __byan_err__:")
                self.indent()
                self.emit("خطأ = __byan_err__.message")
                for s in node.catch_body:
                    self._compile_statement(s)
                self.dedent()
            
            if node.finally_body:
                self.emit("finally:")
                self.indent()
                for s in node.finally_body:
                    self._compile_statement(s)
                self.dedent()
            return
        
        # ارمِ خطأ
        if isinstance(node, ast.ThrowError):
            if isinstance(node.message, str):
                self.emit(f'raise ByanThrow({node.message!r})')
            else:
                val = self._compile_expression(node.message)
                self.emit(f"raise ByanThrow({val})")
            return
        
        # إسناد لخاصية (هذا.اسم = ...)
        if isinstance(node, ast.MemberSet):
            obj = self._compile_expression(node.obj)
            val = self._compile_expression(node.value)
            self.emit(f'{obj}["__fields__"][{node.attr!r}] = {val}')
            return
        
        # نداء method كـ statement
        if isinstance(node, ast.MethodCall):
            self.emit(self._compile_expression(node))
            return
        
        # استيراد
        if isinstance(node, ast.Import):
            self.emit(f"# استورد {node.file_path}")
            # لو وحدة stdlib
            self.emit(f"# (وحدة stdlib: {node.file_path})")
            return
        
        # DictSet (قاموس[مفتاح] = قيمة)
        if isinstance(node, ast.DictSet):
            d = self._compile_expression(node.dict_expr)
            k = self._compile_expression(node.key)
            v = self._compile_expression(node.value)
            self.emit(f"{d}[{k}] = {v}")
            return
        
        # نداء builtin عادي
        self.emit(f"# ⚠️ عقدة غير مدعومة: {type(node).__name__}")

    # ========================================================
    # التعابير (Expressions)
    # ========================================================
    def _compile_expression(self, node):
        if node is None:
            return "None"
        
        # قيم حرفية
        if isinstance(node, ast.Number):
            return repr(node.value)
        
        if isinstance(node, ast.String):
            return repr(node.value)
        
        if isinstance(node, ast.Bool):
            return "True" if node.value else "False"
        
        if isinstance(node, ast.NullLit):
            return "None"
        
        # مرجع متغير
        if isinstance(node, ast.VarRef):
            return node.name
        
        # عملية ثنائية
        if isinstance(node, ast.BinOp):
            left = self._compile_expression(node.left)
            right = self._compile_expression(node.right)
            op = node.op
            # عمليات آمنة للقسمة
            if op == '/':
                return f"__safe_div__({left}, {right})"
            if op == '//':
                return f"__safe_floordiv__({left}, {right})"
            # منطقي
            if op in ('||', 'أو'):
                return f"({left} or {right})"
            if op in ('&&', 'و'):
                return f"({left} and {right})"
            # عادي
            py_op = op if op in '+-*/%**<>' else '+'
            return f"({left} {py_op} {right})"
        
        # مقارنة
        if isinstance(node, ast.Compare):
            left = self._compile_expression(node.left)
            right = self._compile_expression(node.right)
            op = node.op
            return f"({left} {op} {right})"
        
        # قائمة
        if isinstance(node, ast.ListLiteral):
            items = ', '.join(self._compile_expression(i) for i in node.items)
            return f"[{items}]"
        
        # قاموس
        if isinstance(node, ast.DictLiteral):
            if not node.pairs:
                return "{}"
            pairs = []
            for k, v in node.pairs:
                k_str = self._compile_expression(k)
                v_str = self._compile_expression(v)
                pairs.append(f"{k_str}: {v_str}")
            return "{" + ", ".join(pairs) + "}"
        
        # فهرسة
        if isinstance(node, ast.IndexAccess):
            target = self._compile_expression(node.target)
            index = self._compile_expression(node.index)
            return f"{target}[{index}]"
        
        # نداء دالة
        if isinstance(node, ast.FunctionCall):
            args = ', '.join(self._compile_expression(a) for a in node.args)
            return f"{node.name}({args})"
        
        if isinstance(node, ast.BuiltinCall):
            args = ', '.join(self._compile_expression(a) for a in node.args)
            return f"{node.name}({args})"
        
        # جديد صنف(...)
        if isinstance(node, ast.NewInstance):
            args = ', '.join(self._compile_expression(a) for a in node.args)
            return f"{node.class_name}({args})"
        
        # عضو
        if isinstance(node, ast.MemberAccess):
            obj = self._compile_expression(node.obj)
            return f'{obj}["__fields__"][{node.attr!r}]'
        
        # نداء method
        if isinstance(node, ast.MethodCall):
            obj = self._compile_expression(node.obj)
            args = ', '.join(self._compile_expression(a) for a in node.args)
            if node.method == 'أساس':
                # super call
                return f"super().{node.method}({args})"
            return f"{obj}.{node.method}({args})"
        
        # Lambda
        if isinstance(node, ast.Lambda):
            params = ', '.join(node.params)
            body = self._compile_expression(node.body)
            return f"lambda {params}: {body}"
        
        # افتراضي
        return f"None  # ⚠️ عقدة: {type(node).__name__}"


# ========================================================
# دالة مساعدة
# ========================================================
def compile_to_python(program, mode='split', rt_path='byan_rt'):
    """دالة سريعة لترجمة برنامج"""
    compiler = PythonCompiler(program, mode=mode, rt_path=rt_path)
    return compiler.compile()
