# -*- coding: utf-8 -*-
"""بيان REPL — سطر أوامر تفاعلي"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from byan.lexer import Lexer
from byan.parser import Parser


def main():
    print("🎨 بيان REPL v0.1")
    print("اكتب 'خروج' للخروج")
    print()

    context = []

    while True:
        try:
            line = input("بيان> ")
            if line.strip() == 'خروج' or line.strip() == 'exit':
                break
            if not line.strip():
                continue

            # جرب تحليل السطر
            tokens = Lexer(line).tokenize()
            print(f"   توكنز: {[t.type.name for t in tokens if t.value]}")

            # جرب بناء جملة كاملة
            full = "انا_برنامج\n    اسمي: REPL\n\nالكود:\n    " + line
            tokens = Lexer(full).tokenize()
            program = Parser(tokens).parse()
            if program.elements:
                print(f"   ✅ عناصر: {[type(e).__name__ for e in program.elements]}")

        except Exception as e:
            print(f"   ❌ {e}")

    print("👋 مع السلامة!")


if __name__ == '__main__':
    main()
