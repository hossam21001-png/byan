"""تبسيط التبويبات"""
import ast as py_ast
import re

with open('byan/parser.py', 'r', encoding='utf-8') as f:
    c = f.read()

# استبدل parse_tabs_body بنسخة مبسطة
pattern = r'    def parse_tabs_body\(self\):.*?(?=\n    def parse_grid_body)'

new_tabs_body = '''    def parse_tabs_body(self):
        """يقرأ التبويبات - نسخة مبسطة"""
        tabs = []

        while True:
            self.skip_newlines()
            t = self.peek()
            if t.type in (TokenType.DEDENT, TokenType.EOF, TokenType.END):
                break

            # التبويبات
            if t.type == TokenType.TABS_LIST:
                self.next()
                if self.peek().type == TokenType.COLON:
                    self.next()
                self.skip_newlines()
                if self.peek().type == TokenType.INDENT:
                    self.next()
                # كل تبويب = سطر واحد
                while True:
                    self.skip_newlines()
                    tt = self.peek()
                    if tt.type in (TokenType.DEDENT, TokenType.EOF, TokenType.END):
                        break
                    # تخطى -
                    if tt.type == TokenType.MINUS:
                        self.next()
                        tt = self.peek()
                    # اسم التبويب (نص أو معرف)
                    if tt.value:
                        name = str(self.next().value)
                        # تجاهل أي : أو محتوى بعد الاسم
                        if self.peek().type == TokenType.COLON:
                            self.next()
                        # تجاهل باقي السطر
                        while self.peek().type not in (TokenType.NEWLINE,
                                                        TokenType.DEDENT, TokenType.EOF):
                            self.next()
                        tabs.append({'name': name, 'body': []})
                    else:
                        self.next()
                if self.peek().type == TokenType.DEDENT:
                    self.next()
            else:
                self.next()

        if self.peek().type == TokenType.DEDENT:
            self.next()

        return tabs

'''
c = re.sub(pattern, new_tabs_body, c, flags=re.DOTALL)
print("✅ parse_tabs_body مبسّط")

with open('byan/parser.py', 'w', encoding='utf-8') as f:
    f.write(c)

try:
    py_ast.parse(c)
    print("✅ parser.py صحيح")
except SyntaxError as e:
    print(f"❌ خطأ: {e}")

# في html_generator — ابسّط _add_tabs
with open('byan/targets/html_generator.py', 'r', encoding='utf-8') as f:
    c = f.read()

pattern = r'    def _add_tabs\(self, el\):.*?(?=\n    def )'
new_add_tabs = '''    def _add_tabs(self, el):
        """تبويبات - نسخة مبسطة"""
        el_id = el.props.get('المعرف', f'tabs_{len(self.html_elements)}')
        tabs = getattr(el, 'tabs', []) or []

        if not tabs:
            self.html_elements.append(f'<div id="{el_id}"></div>')
            return

        buttons_html = ''
        content_html = ''
        for i, tab in enumerate(tabs):
            name = self._escape(str(tab.get('name', f'Tab {i}')))
            active = 'background:#667eea; color:white;' if i == 0 else 'background:#eee; color:#333;'
            buttons_html += f'<button onclick="byanShowTab_{el_id}({i})" style="padding:10px 20px; margin:2px; border:none; border-radius:8px; cursor:pointer; {active}">{name}</button>'
            display = 'block' if i == 0 else 'none'
            content_html += f'<div id="{el_id}-content-{i}" style="display:{display}; padding:15px;">محتوى {name}</div>'

        self.html_elements.append(
            f'<div id="{el_id}" style="padding: 15px;">'
            f'<div style="margin-bottom:10px;">{buttons_html}</div>'
            f'{content_html}'
            f'</div>'
        )

        # JS للتبديل
        js_lines = []
        js_lines.append(f'function byanShowTab_{el_id}(idx) {{')
        js_lines.append(f'  var total = {len(tabs)};')
        js_lines.append(f'  for (var i = 0; i < total; i++) {{')
        js_lines.append(f'    var c = document.getElementById("{el_id}-content-" + i);')
        js_lines.append(f'    if (c) c.style.display = (i === idx) ? "block" : "none";')
        js_lines.append(f'  }}')
        js_lines.append(f'}}')

        for line in js_lines:
            self.js_events.insert(0, line)

'''
c = re.sub(pattern, new_add_tabs, c, flags=re.DOTALL)
print("✅ _add_tabs مبسّط")

with open('byan/targets/html_generator.py', 'w', encoding='utf-8') as f:
    f.write(c)

try:
    py_ast.parse(c)
    print("✅ html_generator.py صحيح")
except SyntaxError as e:
    print(f"❌ خطأ: {e}")
