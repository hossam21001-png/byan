"""إصلاح النماذج"""
import ast as py_ast

print("═══════════════════════════════════")
print("🔧 إصلاح النماذج")
print("═══════════════════════════════════")

# ===== 1) tokens.py — نضيف FIELDS + ON_SUBMIT =====
with open('byan/tokens.py', 'r', encoding='utf-8') as f:
    c = f.read()

if 'FIELDS' not in c:
    c = c.replace('    ICON          = auto()',
                  '    ICON          = auto()\n    FIELDS        = auto()\n    ON_SUBMIT     = auto()', 1)
    with open('byan/tokens.py', 'w', encoding='utf-8') as f:
        f.write(c)
    print("✅ tokens.py: FIELDS + ON_SUBMIT أضيفوا")
else:
    print("ℹ️  tokens.py: موجود")

# ===== 2) lexer.py — نضيف الكلمات =====
with open('byan/lexer.py', 'r', encoding='utf-8') as f:
    c = f.read()

if "'الحقول': TokenType.FIELDS" not in c:
    c = c.replace("'أيقونة': TokenType.ICON,",
                  "'أيقونة': TokenType.ICON,\n    'الحقول': TokenType.FIELDS,\n    'عند_الإرسال': TokenType.ON_SUBMIT,")
    with open('byan/lexer.py', 'w', encoding='utf-8') as f:
        f.write(c)
    print("✅ lexer.py: الحقول + عند_الإرسال أضيفوا")
else:
    print("ℹ️  lexer.py: موجود")

# ===== 3) parser.py — نحدّث parse_form =====
with open('byan/parser.py', 'r', encoding='utf-8') as f:
    c = f.read()

import re
# استبدل parse_form
pattern = r'    def parse_form\(self\):.*?(?=\n    def )'
new_form = '''    def parse_form(self):
        """نموذج"""
        self.next()  # FORM
        if self.peek().type == TokenType.COLON:
            self.next()
        self.skip_newlines()
        if self.peek().type == TokenType.INDENT:
            self.next()

        props = {}
        fields = []
        actions = []

        while True:
            self.skip_newlines()
            t = self.peek()
            if t.type in (TokenType.DEDENT, TokenType.EOF, TokenType.END):
                break

            # عند_الإرسال
            if t.type == TokenType.ON_SUBMIT:
                self.next()
                if self.peek().type == TokenType.COLON:
                    self.next()
                self.skip_newlines()
                if self.peek().type == TokenType.INDENT:
                    self.next()
                while True:
                    self.skip_newlines()
                    tt = self.peek()
                    if tt.type in (TokenType.DEDENT, TokenType.EOF, TokenType.END):
                        break
                    if tt.type == TokenType.SHOW:
                        actions.append(self.parse_show())
                    elif tt.type == TokenType.VAR_KW:
                        actions.append(self.parse_var_decl())
                    else:
                        self.next()
                if self.peek().type == TokenType.DEDENT:
                    self.next()

            # الحقول
            elif t.type == TokenType.FIELDS:
                self.next()
                if self.peek().type == TokenType.COLON:
                    self.next()
                self.skip_newlines()
                if self.peek().type == TokenType.INDENT:
                    self.next()
                while True:
                    self.skip_newlines()
                    tt = self.peek()
                    if tt.type in (TokenType.DEDENT, TokenType.EOF, TokenType.END):
                        break
                    # تخطى -
                    if tt.type == TokenType.MINUS:
                        self.next()
                        tt = self.peek()
                    # اقرأ اسم الحقل
                    if tt.type in (TokenType.IDENTIFIER, TokenType.FILE_NAME,
                                    TokenType.NAME, TokenType.TEXT):
                        fname = str(self.next().value)
                        ftype = 'text'
                        if self.peek().type == TokenType.COLON:
                            self.next()
                            # اقرأ النوع (أي token)
                            type_tok = self.peek()
                            if type_tok.value:
                                ftype = str(type_tok.value)
                                self.next()
                        fields.append({'name': fname, 'type': ftype})
                    else:
                        self.next()
                if self.peek().type == TokenType.DEDENT:
                    self.next()

            # props
            elif t.type in (TokenType.TITLE_PROP, TokenType.IDENTIFIER,
                             TokenType.FILE_NAME, TokenType.SIZE,
                             TokenType.BG_COLOR, TokenType.NAME):
                key = str(self.next().value)
                if self.peek().type == TokenType.COLON:
                    self.next()
                if self.peek().type == TokenType.STRING:
                    val = str(self.next().value)
                else:
                    val = str(self.next().value)
                props[key] = val
            else:
                self.next()

        if self.peek().type == TokenType.DEDENT:
            self.next()

        return ast.CreateForm(props, fields, actions)

'''
c = re.sub(pattern, new_form, c, flags=re.DOTALL)
print("✅ parser.py: parse_form محدّث")

with open('byan/parser.py', 'w', encoding='utf-8') as f:
    f.write(c)

try:
    py_ast.parse(c)
    print("✅ parser.py صحيح")
except SyntaxError as e:
    print(f"❌ خطأ: {e}")

print()
print("═══════════════════════════════════")
print("✅ تم إصلاح النماذج")
print("═══════════════════════════════════")
