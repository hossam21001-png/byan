# -*- coding: utf-8 -*-
"""الأساس لكل Compilers"""


class BaseCompiler:
    """مترجم أساسي"""

    def __init__(self, program):
        self.program = program
        self.indent_level = 0
        self.lines = []
        self.imports = set()
        self.functions = {}   # اسم → FunctionDef
        self.classes = {}     # اسم → ClassDef

    def emit(self, line):
        """يضيف سطر مع indent مناسب"""
        self.lines.append("    " * self.indent_level + line)

    def indent(self):
        self.indent_level += 1

    def dedent(self):
        self.indent_level = max(0, self.indent_level - 1)

    def compile(self):
        """يترجم البرنامج — يتجاوز في الـ subclass"""
        raise NotImplementedError

    def get_output(self):
        """يرجّع الناتج كنص"""
        return "\n".join(self.lines)
