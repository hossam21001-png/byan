import os
from .. import ast_nodes as ast


class PythonAppTarget:
    def __init__(self, output_dir='./build'):
        self.output_dir = os.path.abspath(output_dir)

    def generate(self, program):
        """يولّد HTML/CSS/JS من الأوصاف تلقائيًا"""
        from .html_generator import HtmlGenerator
        from .. import ast_nodes as ast

        os.makedirs(self.output_dir, exist_ok=True)
        created = []

        # لو فيه ملفات يدوية، اكتبها الأول
        for el in program.elements:
            if isinstance(el, ast.CreateFile):
                full_path = self._write_file(el)
                if full_path:
                    created.append(full_path)

        # هل فيه واجهة HTML جاهزة؟
        if program.ui_file and os.path.exists(program.ui_file):
            print(f"   📄 استخدام HTML جاهز: {program.ui_file}")
            with open(program.ui_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            html_path = os.path.join(self.output_dir, 'index.html')
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            if html_path not in created:
                created.append(html_path)

            # ولّد JS فقط
            js_code = self._collect_js(program)
            script_path = os.path.join(self.output_dir, 'script.js')
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(js_code)
            if script_path not in created:
                created.append(script_path)
            print(f"   📄 script.js")

            # ولّد PWA
            try:
                from .pwa_generator import PwaGenerator
                pwa = PwaGenerator(program, self.output_dir)
                pwa_files = pwa.generate()
                created.extend(pwa_files)
            except Exception as e:
                print(f"   ⚠️  PWA: {e}")

            runner = self._write_runner(program)
            created.append(runner)
            return {'files': created, 'runner': runner, 'output': self.output_dir}

        # هل فيه عناصر وصفية (نافذة/زر/عنوان...)?
        has_visual = any(
            isinstance(el, (ast.CreateWindow, ast.CreateButton,
                            ast.CreateTitle, ast.CreateText,
                            ast.CreateInput))
            for el in program.elements
        )

        # ولّد HTML/CSS/JS من الأوصاف لو فيه عناصر
        if has_visual:
            gen = HtmlGenerator(program)
            result = gen.generate()

            # اكتب HTML (يستبدل الموجود أو ينشئ جديد)
            html_path = os.path.join(self.output_dir, 'index.html')
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(result['html'])
            if html_path not in created:
                created.append(html_path)
            print(f"   📄 index.html (مولّد من الأوصاف)")

            # اكتب CSS
            css_path = os.path.join(self.output_dir, 'style.css')
            with open(css_path, 'w', encoding='utf-8') as f:
                f.write(result['css'])
            if css_path not in created:
                created.append(css_path)
            print(f"   📄 style.css (مولّد من الأوصاف)")

            # اكتب JS
            js_path = os.path.join(self.output_dir, 'script.js')
            with open(js_path, 'w', encoding='utf-8') as f:
                f.write(result['js'])
            if js_path not in created:
                created.append(js_path)
            print(f"   📄 script.js (مولّد من الأوصاف)")

            # ===== PWA: manifest + service worker =====
            try:
                from .pwa_generator import PwaGenerator
                pwa = PwaGenerator(program, self.output_dir)
                pwa_files = pwa.generate()
                created.extend(pwa_files)
            except Exception as e:
                print(f"   ⚠️  PWA: {e}")
        else:
            # الطريقة القديمة: اكتب script.js من الأحداث
            js_code = self._collect_js(program)
            script_path = os.path.join(self.output_dir, 'script.js')
            if os.path.exists(script_path):
                with open(script_path, 'a', encoding='utf-8') as f:
                    f.write('\n\n' + js_code)

        # ولّد run.py
        runner = self._write_runner(program)
        created.append(runner)

        return {'files': created, 'runner': runner, 'output': self.output_dir}


    def _clean_path(self, path):
        if not path:
            return ''
        return path.strip().lstrip('./').lstrip('/').rstrip('/')

    def _write_file(self, el):
        name = (el.name or '').strip().strip('/')
        rel_path = self._clean_path(el.path)
        if not name:
            return None
        folder = os.path.join(self.output_dir, rel_path) if rel_path else self.output_dir
        os.makedirs(folder, exist_ok=True)
        full_path = os.path.join(folder, name)

        content = el.content or ''

        # لو HTML، أضف script tag لو مش موجود
        if name.endswith('.html'):
            if 'script.js' not in content:
                if '</body>' in content:
                    content = content.replace(
                        '</body>',
                        '  <script src="script.js"></script>\n</body>'
                    )
                else:
                    content += '\n<script src="script.js"></script>'

        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"   📄 {os.path.relpath(full_path, self.output_dir)}")
        return full_path

    def _write_runner(self, program):
        title = program.name or 'برنامج بيان'
        html_file = None
        for el in program.elements:
            if isinstance(el, ast.CreateFile):
                name = (el.name or '').strip()
                if name.endswith('.html'):
                    rel_path = self._clean_path(el.path)
                    html_file = os.path.join(self.output_dir, rel_path, name) if rel_path else os.path.join(self.output_dir, name)
                    break
        if not html_file:
            html_file = os.path.join(self.output_dir, 'index.html')

        runner_path = os.path.join(self.output_dir, 'run.py')
        code = f'''import os
HTML_PATH = r"{html_file}"
def main():
    try:
        import webview
    except ImportError:
        print("افتح في المتصفح:")
        print("file://" + os.path.abspath(HTML_PATH))
        return
    webview.create_window(title="{title}", url="file://" + os.path.abspath(HTML_PATH), width=900, height=600)
    webview.start()
if __name__ == "__main__":
    main()
'''
        with open(runner_path, 'w', encoding='utf-8') as f:
            f.write(code)
        return runner_path

    def _collect_js(self, program):
        js_lines = ["// مولّد تلقائيا من بيان", ""]

        # ===== JavaScript Runtime مستقل (بدون سيرفر) =====
        js_lines.append("// ===== Byan Runtime (standalone) =====")
        js_lines.append("var BYAN_DATA = {};")
        js_lines.append("try { BYAN_DATA = JSON.parse(localStorage.getItem('byan_data') || '{}'); } catch(e) {}")
        js_lines.append("")
        js_lines.append("function _byanSave() {")
        js_lines.append("  try { localStorage.setItem('byan_data', JSON.stringify(BYAN_DATA)); } catch(e) {}")
        js_lines.append("}")
        js_lines.append("")
        js_lines.append("// قراءة/كتابة ملفات افتراضية (localStorage)")
        js_lines.append("function byanReadFile(path) {")
        js_lines.append("  return BYAN_DATA['file:' + path] || '';")
        js_lines.append("}")
        js_lines.append("")
        js_lines.append("function byanWriteFile(path, content) {")
        js_lines.append("  BYAN_DATA['file:' + path] = String(content);")
        js_lines.append("  _byanSave();")
        js_lines.append("  return true;")
        js_lines.append("}")
        js_lines.append("")
        js_lines.append("// قاعدة بيانات بسيطة (localStorage)")
        js_lines.append("function byanDbInsert(table, record) {")
        js_lines.append("  if (!BYAN_DATA['db:' + table]) BYAN_DATA['db:' + table] = [];")
        js_lines.append("  BYAN_DATA['db:' + table].push(record);")
        js_lines.append("  _byanSave();")
        js_lines.append("  return true;")
        js_lines.append("}")
        js_lines.append("")
        js_lines.append("function byanDbSelect(table, filter) {")
        js_lines.append("  var rows = BYAN_DATA['db:' + table] || [];")
        js_lines.append("  return rows;")
        js_lines.append("}")
        js_lines.append("")
        js_lines.append("// Alert بديل لـ console")
        js_lines.append("function byanLog() {")
        js_lines.append("  console.log('[Byan]', Array.prototype.slice.call(arguments).join(' '));")
        js_lines.append("}")
        js_lines.append("")
        js_lines.append("// byanCall compat (standalone)")
        js_lines.append("function byanCall(endpoint, data, callback) {")
        js_lines.append("  var res = {status: 'ok'};")
        js_lines.append("  if (endpoint === '/api/read') {")
        js_lines.append("    res.content = byanReadFile(data.path);")
        js_lines.append("  } else if (endpoint === '/api/write') {")
        js_lines.append("    byanWriteFile(data.path, data.content);")
        js_lines.append("  } else {")
        js_lines.append("    res.status = 'error';")
        js_lines.append("    res.message = 'غير مدعوم في standalone';")
        js_lines.append("  }")
        js_lines.append("  if (callback) callback(res);")
        js_lines.append("  return Promise.resolve(res);")
        js_lines.append("}")
        js_lines.append("")

        has_events = False

        # أول حاجة: كل تعريفات الدوال
        for el in program.elements:
            if isinstance(el, ast.FunctionDef):
                js_lines.extend(self._action_to_js(el))
                js_lines.append("")
                has_events = True

        # بعدين: أحداث الأزرار
        for el in program.elements:
            if isinstance(el, ast.CreateButton):
                btn_id = None
                for key in ('المعرف', 'معرف', 'id', 'ID'):
                    if key in el.props:
                        btn_id = str(el.props[key]).strip()
                        break
                if not btn_id or not el.actions:
                    continue
                has_events = True
                js_lines.append(
                    f"document.getElementById('{btn_id}')"
                    f".addEventListener('click', function() {{"
                )
                for a in el.actions:
                    js_lines.extend(self._action_to_js(a, indent="  "))
                js_lines.append("});")
                js_lines.append("")

        if not has_events:
            js_lines.append("console.log('لا توجد أحداث');")

        return '\n'.join(js_lines)


    def _action_to_js(self, action, indent=""):
        """يحوّل action إلى كود JS"""
        lines = []

        if isinstance(action, ast.ShowIn):
            target = str(action.target).strip()
            text = self._value_to_js(action.text)
            lines.append(f"{indent}document.querySelector('{target}').textContent = {text};")

        elif isinstance(action, ast.ClearIn):
            target = str(action.target).strip()
            lines.append(f"{indent}document.querySelector('{target}').textContent = '';")

        elif isinstance(action, ast.VarDecl):
            name = action.name
            value = self._value_to_js(action.value)
            lines.append(f"{indent}var {name} = {value};")

        elif isinstance(action, ast.Assign):
            name = action.name
            value = self._value_to_js(action.value)
            lines.append(f"{indent}{name} = {value};")

        elif isinstance(action, ast.CompoundAssign):
            name = action.name
            value = self._value_to_js(action.value)
            lines.append(f"{indent}{name} {action.op}= {value};")

        elif isinstance(action, ast.If):
            cond = self._value_to_js(action.condition)
            lines.append(f"{indent}if ({cond}) {{")
            for a in action.then_body:
                lines.extend(self._action_to_js(a, indent + "  "))
            lines.append(f"{indent}}}")
            if action.else_body:
                lines.append(f"{indent}else {{")
                for a in action.else_body:
                    lines.extend(self._action_to_js(a, indent + "  "))
                lines.append(f"{indent}}}")

        elif isinstance(action, ast.While):
            cond = self._value_to_js(action.condition)
            lines.append(f"{indent}while ({cond}) {{")
            for a in action.body:
                lines.extend(self._action_to_js(a, indent + "  "))
            lines.append(f"{indent}}}")

        elif isinstance(action, ast.FunctionDef):
            params = ', '.join(action.params)
            lines.append(f"{indent}function {action.name}({params}) {{")
            for a in action.body:
                lines.extend(self._action_to_js(a, indent + "  "))
            lines.append(f"{indent}}}")

        elif isinstance(action, ast.Return):
            if action.value is not None:
                val = self._value_to_js(action.value)
                lines.append(f"{indent}return {val};")
            else:
                lines.append(f"{indent}return;")

        elif isinstance(action, ast.FileOp):
            op = action.op
            source = self._escape_js(action.source)
            target = self._escape_js(action.target)
            content = self._escape_js(action.content)

            if op == 'delete':
                lines.append(f"{indent}byanCall('/api/delete', {{path: byanPath('{source}')}}, function(res) {{")
                lines.append(f"{indent}  console.log('🗑️', res);")
                lines.append(f"{indent}}});")
            elif op == 'read':
                lines.append(f"{indent}byanCall('/api/read', {{path: byanPath('{source}')}}, function(res) {{")
                lines.append(f"{indent}  if (res.status === 'ok') {{")
                lines.append(f"{indent}    window._byan_last = res.content;")
                lines.append(f"{indent}    window._byan_files = window._byan_files || {{}};")
                lines.append(f"{indent}    window._byan_files['{source}'] = res.content;")
                lines.append(f"{indent}    console.log('📖 محتوى {source}:', res.content);")
                lines.append(f"{indent}    // اعرض في كل عنصر output موجود")
                lines.append(f"{indent}    var outs = document.querySelectorAll('#output, .byan-output');")
                lines.append(f"{indent}    outs.forEach(function(el) {{ el.textContent = res.content; }});")
                lines.append(f"{indent}  }} else {{")
                lines.append(f"{indent}    console.error('❌ فشل القراءة:', res.message);")
                lines.append(f"{indent}  }}")
                lines.append(f"{indent}}});")
            elif op == 'write':
                lines.append(f"{indent}byanCall('/api/write', {{path: byanPath('{source}'), content: '{content}'}}, function(res) {{")
                lines.append(f"{indent}  console.log('✍️', res);")
                lines.append(f"{indent}}});")
            elif op == 'copy':
                lines.append(f"{indent}byanCall('/api/copy', {{source: byanPath('{source}'), target: byanPath('{target}')}}, function(res) {{")
                lines.append(f"{indent}  console.log('📋', res);")
                lines.append(f"{indent}}});")
            elif op == 'move':
                lines.append(f"{indent}byanCall('/api/move', {{source: byanPath('{source}'), target: byanPath('{target}')}}, function(res) {{")
                lines.append(f"{indent}  console.log('📦', res);")
                lines.append(f"{indent}}});")
            elif op == 'mkdir':
                lines.append(f"{indent}byanCall('/api/mkdir', {{path: '{source}'}}, function(res) {{")
                lines.append(f"{indent}  console.log('📁', res);")
                lines.append(f"{indent}}});")
            elif op == 'exec':
                lines.append(f"{indent}byanCall('/api/exec', {{command: '{source}'}}, function(res) {{")
                lines.append(f"{indent}  console.log('⚙️', res);")
                lines.append(f"{indent}}});")


        elif isinstance(action, ast.ForIn):
            var_name = action.var_name
            iterable = self._value_to_js(action.iterable)
            lines.append(f"{indent}for (var {var_name} of {iterable}) {{")
            for a in action.body:
                lines.extend(self._action_to_js(a, indent + "  "))
            lines.append(f"{indent}}}")

        return lines

    def _value_to_js_iterable(self, val):
        """يحوّل قائمة أو متغير إلى JS iterable"""
        if isinstance(val, ast.ListLiteral):
            items = ', '.join(self._value_to_js(i) for i in val.items)
            return f"[{items}]"
        if isinstance(val, ast.FunctionCall):
            args = ', '.join(self._value_to_js(a) for a in val.args)
            return f"{val.name}({args})"
        return self._value_to_js(val)

    def _value_to_js(self, val):
        """يحوّل قيمة AST إلى كود JS"""
        if val is None:
            return "''"
        if isinstance(val, ast.Number):
            return str(val.value)
        if isinstance(val, ast.String):
            v = str(val.value)
            return f"'{v}'"
        if isinstance(val, ast.VarRef):
            return val.name
        if isinstance(val, ast.BinOp):
            left = val.left
            right = val.right
            # لو اليسار string أو اليمين string → concat عادي
            left_js = self._value_to_js(left)
            right_js = self._value_to_js(right)
            if val.op == '+':
                # افحص لو أي حد string
                if self._is_string(left) or self._is_string(right):
                    return f"({left_js} + {right_js})"
                else:
                    return f"({left_js} + {right_js})"
            return f"({left_js} {val.op} {right_js})"
        if isinstance(val, ast.Compare):
            left = self._value_to_js(val.left)
            right = self._value_to_js(val.right)
            op = val.op
            if op == '=':
                op = '=='
            return f"({left} {op} {right})"
        if isinstance(val, ast.ListLiteral):
            items = ', '.join(self._value_to_js(i) for i in val.items)
            return f"[{items}]"
        if isinstance(val, ast.FunctionCall):
            args = ', '.join(self._value_to_js(a) for a in val.args)
            return f"{val.name}({args})"
        if isinstance(val, str):
            return f"'{val}'"
        if isinstance(val, (int, float)):
            return str(val)
        return f"'{val}'"

    def _is_string(self, val):
        """يفحص لو القيمة نص"""
        if isinstance(val, ast.String):
            return True
        if isinstance(val, ast.BinOp):
            return self._is_string(val.left) or self._is_string(val.right)
        return False
