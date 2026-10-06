"""مولّد HTML/CSS/JS من عناصر بيان الوصفية"""


COLOR_MAP = {
    'أحمر': '#e74c3c',
    'أحمر_فاتح': '#ff6b6b',
    'أزرق': '#3498db',
    'أزرق_فاتح': '#5dade2',
    'أخضر': '#2ecc71',
    'أصفر': '#f1c40f',
    'رمادي': '#7f8c8d',
    'رمادي_فاتح': '#ecf0f1',
    'أسود': '#2c3e50',
    'أبيض': '#ffffff',
    'برتقالي': '#e67e22',
    'بنفسجي': '#9b59b6',
    'وردي': '#e91e63',
}


class HtmlGenerator:
    """يولّد HTML/CSS/JS كامل من عناصر بيان"""

    def __init__(self, program):
        self.program = program
        self.window_props = {}
        self.html_elements = []
        self.css_rules = []
        self.js_events = []

    def color(self, name):
        """يحوّل اسم اللون العربي لـ CSS"""
        if not name:
            return None
        name = str(name).strip()
        if name in COLOR_MAP:
            return COLOR_MAP[name]
        if name.startswith('#') or name.startswith('rgb'):
            return name
        return None

    def generate(self):
        """يولّد 3 ملفات: HTML + CSS + JS"""
        # اقرأ العناصر
        from .. import ast_nodes as ast

        # 1) الدوال أولاً (عشان تكون متاحة للأزرار)
        for el in self.program.elements:
            if isinstance(el, ast.FunctionDef):
                self._add_function(el)

        # 2) باقي العناصر
        for el in self.program.elements:
            if isinstance(el, ast.CreateWindow):
                self.window_props = el.props
            elif isinstance(el, ast.CreateTitle):
                self._add_title(el)
            elif isinstance(el, ast.CreateText):
                self._add_text(el)
            elif isinstance(el, ast.CreateButton):
                self._add_button(el)
            elif isinstance(el, ast.CreateInput):
                self._add_input(el)
            elif isinstance(el, ast.CreateImage):
                self._add_image(el)
            elif isinstance(el, ast.CreateVideo):
                self._add_video(el)
            elif isinstance(el, ast.CreateSelect):
                self._add_select(el)
            elif isinstance(el, ast.CreateGrid):
                self._add_grid(el)
            elif isinstance(el, ast.CreateTable):
                self._add_table(el)
            elif isinstance(el, ast.CreateChart):
                self._add_chart(el)
            elif isinstance(el, ast.CreateForm):
                self._add_form(el)
            elif isinstance(el, ast.CreateTabs):
                self._add_tabs(el)
            elif isinstance(el, ast.CreateIcon):
                self._add_icon(el)
            elif isinstance(el, ast.CreateModal):
                self._add_modal(el)
            elif isinstance(el, ast.AddTooltip):
                self._add_tooltip(el)
            elif isinstance(el, ast.CreateAccordion):
                self._add_accordion(el)
            elif isinstance(el, ast.CreateSidebar):
                self._add_sidebar(el)
            elif isinstance(el, ast.CreateNavbar):
                self._add_navbar(el)
            elif isinstance(el, ast.PayButton):
                self._add_pay_button(el)
            elif isinstance(el, ast.CodeEditor):
                self._add_code_editor(el)

        return {
            'html': self._build_html(),
            'css': self._build_css(),
            'js': self._build_js(),
        }

    def _add_title(self, el):
        text = self._escape(el.props.get('النص', 'عنوان'))
        font_size = el.props.get('الحجم', '28')
        color = self.color(el.props.get('اللون'))
        el_id = el.props.get('المعرف', f'title_{len(self.html_elements)}')

        style = f"font-size: {font_size}px;"
        if color:
            style += f" color: {color};"

        self.html_elements.append(
            f'<h1 id="{el_id}" style="{style}">{text}</h1>'
        )

    def _add_text(self, el):
        text = self._escape(el.props.get('النص', ''))
        font_size = el.props.get('الحجم', '16')
        color = self.color(el.props.get('اللون'))
        el_id = el.props.get('المعرف', f'text_{len(self.html_elements)}')

        style = f"font-size: {font_size}px;"
        if color:
            style += f" color: {color};"

        self.html_elements.append(
            f'<p id="{el_id}" style="{style}">{text}</p>'
        )

    def _add_button(self, el):
        text = self._escape(el.props.get('النص', 'زر'))
        bg = self.color(el.props.get('اللون')) or '#3498db'
        el_id = el.props.get('المعرف', f'btn_{len(self.html_elements)}')

        style = f"background: {bg};"
        self.html_elements.append(
            f'<button id="{el_id}" style="{style}">{text}</button>'
        )

        # ربط الأحداث
        if el.actions:
            js_lines = [
                f"document.getElementById('{el_id}').addEventListener('click', function() {{"
            ]
            for a in el.actions:
                js_lines.extend(self._action_to_js(a, "  "))
            js_lines.append("});")
            self.js_events.extend(js_lines)

    def _add_input(self, el):
        el_id = el.props.get('المعرف', f'input_{len(self.html_elements)}')
        placeholder = self._escape(el.props.get('النص', ''))
        self.html_elements.append(
            f'<input id="{el_id}" placeholder="{placeholder}" />'
        )

    def _add_icon(self, el):
        """أيقونة"""
        el_id = el.props.get('المعرف', f'icon_{len(self.html_elements)}')
        icon_type = el.props.get('النوع', 'star')
        icon_size = el.props.get('الحجم', 32)
        icon_color = self.color(el.props.get('اللون')) or '#2c3e50'
        # نستخدم emoji كأيقونة
        emoji_map = {
            'home': '🏠', 'user': '👤', 'settings': '⚙️',
            'star': '⭐', 'heart': '❤️', 'check': '✅',
            'search': '🔍', 'menu': '☰', 'close': '✖️',
            'add': '➕', 'delete': '🗑️', 'edit': '✏️',
            'download': '⬇️', 'upload': '⬆️', 'info': 'ℹ️',
        }
        emoji = emoji_map.get(icon_type, '⭐')
        self.html_elements.append(
            f'<span id="{el_id}" style="font-size: {icon_size}px; color: {icon_color};">{emoji}</span>'
        )

    def _add_modal(self, el):
        """نافذة منبثقة"""
        el_id = el.props.get('المعرف', f'modal_{len(self.html_elements)}')
        title = self._escape(el.props.get('العنوان', 'نافذة'))
        self.html_elements.append(
            f'<button onclick="document.getElementById(\'{el_id}\').style.display=\'flex\'" '
            f'style="background:#667eea;color:white;padding:10px 20px;border:none;border-radius:8px;cursor:pointer;margin:5px;">'
            f'{title}</button>'
        )
        self.html_elements.append(
            f'<div id="{el_id}" style="display:none;position:fixed;top:0;left:0;width:100%;height:100%;'
            f'background:rgba(0,0,0,0.5);align-items:center;justify-content:center;z-index:9999;">'
            f'<div style="background:white;padding:30px;border-radius:15px;max-width:500px;text-align:center;">'
            f'<h3>{title}</h3>'
            f'<button onclick="document.getElementById(\'{el_id}\').style.display=\'none\'" '
            f'style="background:#e74c3c;color:white;padding:10px 20px;border:none;border-radius:8px;cursor:pointer;">'
            f'إغلاق</button>'
            f'</div></div>'
        )

    def _add_tooltip(self, el):
        """تلميح"""
        text = self._escape(el.props.get('النص', 'تلميح'))
        self.html_elements.append(
            f'<span title="{text}" style="cursor:help;border-bottom:1px dotted #667eea;">{text}</span>'
        )

    def _add_accordion(self, el):
        """قائمة طي"""
        title = self._escape(el.props.get('العنوان', 'قسم'))
        content = self._escape(el.props.get('المحتوى', 'محتوى القسم'))
        self.html_elements.append(
            f'<details style="padding:10px;border:1px solid #ddd;border-radius:8px;margin:5px 0;">'
            f'<summary style="cursor:pointer;font-weight:bold;">{title}</summary>'
            f'<p style="margin-top:10px;">{content}</p>'
            f'</details>'
        )

    def _add_sidebar(self, el):
        """شريط جانبي"""
        el_id = el.props.get('المعرف', f'sidebar_{len(self.html_elements)}')
        self.html_elements.append(
            f'<div id="{el_id}" style="background:#2c3e50;color:white;padding:20px;border-radius:10px;margin:10px 0;">'
            f'<h3>القائمة الجانبية</h3>'
            f'<ul style="list-style:none;padding:0;">'
            f'<li style="padding:8px;">الرئيسية</li>'
            f'<li style="padding:8px;">الإعدادات</li>'
            f'<li style="padding:8px;">حول</li>'
            f'</ul></div>'
        )

    def _add_navbar(self, el):
        """شريط تنقل"""
        el_id = el.props.get('المعرف', f'nav_{len(self.html_elements)}')
        self.html_elements.append(
            f'<nav id="{el_id}" style="background:#2c3e50;color:white;padding:15px;border-radius:10px;margin:10px 0;display:flex;gap:20px;">'
            f'<a href="#" style="color:white;text-decoration:none;">الرئيسية</a>'
            f'<a href="#" style="color:white;text-decoration:none;">المنتجات</a>'
            f'<a href="#" style="color:white;text-decoration:none;">اتصل بنا</a>'
            f'</nav>'
        )

    def _add_grid(self, el):
        """شبكة"""
        el_id = el.props.get('المعرف', f'grid_{len(self.html_elements)}')
        cols = getattr(el, 'columns', 2)
        items = getattr(el, 'items', []) or []

        emoji_map = {
            'home': '🏠', 'user': '👤', 'settings': '⚙️',
            'star': '⭐', 'heart': '❤️', 'check': '✅',
            'search': '🔍', 'menu': '☰', 'close': '✖️',
            'add': '➕', 'delete': '🗑️', 'edit': '✏️',
        }

        items_html = ''
        for item in items:
            if item.get('type') == 'icon':
                emoji = emoji_map.get(item.get('value', ''), '⭐')
                items_html += f'<div style="padding:10px; text-align:center; font-size:32px;">{emoji}</div>'
            else:
                items_html += f'<div style="padding:10px; text-align:center;">{self._escape(item.get("value", ""))}</div>'

        self.html_elements.append(
            f'<div id="{el_id}" style="display:grid; grid-template-columns: repeat({cols}, 1fr); gap: 10px; padding: 15px;">'
            f'{items_html}'
            f'</div>'
        )


    def _add_table(self, el):
        """جدول"""
        el_id = el.props.get('المعرف', f'table_{len(self.html_elements)}')
        headers = getattr(el, 'headers', []) or []
        rows = getattr(el, 'rows', []) or []

        # Headers
        headers_html = ''
        if headers:
            headers_html = '<tr>' + ''.join(
                f'<th style="padding:10px; background:#667eea; color:white; border:1px solid #ddd;">{self._escape(h)}</th>'
                for h in headers
            ) + '</tr>'

        # Rows
        rows_html = ''
        for row in rows:
            rows_html += '<tr>' + ''.join(
                f'<td style="padding:10px; border:1px solid #ddd;">{self._escape(cell)}</td>'
                for cell in row
            ) + '</tr>'

        self.html_elements.append(
            f'<table id="{el_id}" style="width:100%; border-collapse:collapse; margin:10px 0; direction:rtl;">'
            f'<thead>{headers_html}</thead>'
            f'<tbody>{rows_html}</tbody>'
            f'</table>'
        )


    def _add_chart(self, el):
        el_id = el.props.get('المعرف', f'chart_{len(self.html_elements)}')
        self.html_elements.append(
            f'<canvas id="{el_id}" width="400" height="200"></canvas>'
        )

    def _add_form(self, el):
        """نموذج"""
        el_id = el.props.get('المعرف', f'form_{len(self.html_elements)}')
        fields = getattr(el, 'fields', []) or []
        fields_html = ''
        for f in fields:
            fname = f.get('name', 'field')
            ftype = f.get('type', 'text')
            if ftype in ('كلمة_سر', 'password'):
                input_type = 'password'
            elif ftype in ('رقم', 'number'):
                input_type = 'number'
            elif ftype in ('ايميل', 'email'):
                input_type = 'email'
            else:
                input_type = 'text'
            fields_html += f'<input type="{input_type}" name="{fname}" placeholder="{fname}" style="display:block; width:100%; padding:10px; margin:5px 0; border-radius:8px; border:1px solid #ddd;"><br>'

        self.html_elements.append(
            f'<form id="{el_id}" style="padding: 20px; text-align: right;">'
            f'{fields_html}'
            f'<button type="submit" style="background:#2ecc71; color:white; padding:10px 20px; border:none; border-radius:8px; cursor:pointer;">إرسال</button>'
            f'</form>'
        )

        # نضيف حدث submit
        if hasattr(el, 'actions') and el.actions:
            self.js_events.append(f"document.getElementById('{el_id}').addEventListener('submit', function(e) {{")
            self.js_events.append(f"  e.preventDefault();")
            for a in el.actions:
                self.js_events.extend(self._action_to_js(a, "  "))
            self.js_events.append(f"}});")


    def _add_tabs(self, el):
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


    def _add_image(self, el):
        src = self._escape(el.props.get('المسار', ''))
        alt = self._escape(el.props.get('النص', 'صورة'))
        width = el.props.get('العرض', el.props.get('الحجم', '300'))
        el_id = el.props.get('المعرف', f'img_{len(self.html_elements)}')
        self.html_elements.append(
            f'<img id="{el_id}" src="{src}" alt="{alt}" style="max-width: {width}px; border-radius: 10px;" />'
        )

    def _add_video(self, el):
        src = self._escape(el.props.get('المسار', ''))
        width = el.props.get('العرض', el.props.get('الحجم', '400'))
        el_id = el.props.get('المعرف', f'video_{len(self.html_elements)}')
        self.html_elements.append(
            f'<video id="{el_id}" src="{src}" controls style="max-width: {width}px; border-radius: 10px;"></video>'
        )

    def _add_select(self, el):
        el_id = el.props.get('المعرف', f'select_{len(self.html_elements)}')
        # اقرأ الخيارات من el.options
        options_html = '<option value="">اختر...</option>'
        if hasattr(el, 'options') and el.options:
            for opt in el.options:
                safe_opt = self._escape(opt)
                options_html += f'<option value="{safe_opt}">{safe_opt}</option>'
        self.html_elements.append(
            f'<select id="{el_id}">{options_html}</select>'
        )

    def _action_to_js(self, action, indent=""):
        from .. import ast_nodes as ast
        lines = []

        if isinstance(action, ast.ShowIn):
            target = str(action.target).strip()
            text = self._value_to_js(action.text)
            lines.append(f"{indent}var _el = document.querySelector('{target}');")
            lines.append(f"{indent}if (_el) _el.textContent = {text};")

        elif isinstance(action, ast.ClearIn):
            target = str(action.target).strip()
            lines.append(f"{indent}var _el = document.querySelector('{target}');")
            lines.append(f"{indent}if (_el) _el.textContent = '';")

        elif isinstance(action, ast.VarDecl):
            val = self._value_to_js(action.value)
            lines.append(f"{indent}var {action.name} = {val};")

        elif isinstance(action, ast.FunctionCall):
            # استدعاء دالة بدون إسناد
            val = self._value_to_js(action)
            lines.append(f"{indent}{val};")

        elif isinstance(action, ast.Assign):
            val = self._value_to_js(action.value)
            lines.append(f"{indent}{action.name} = {val};")

        elif isinstance(action, ast.CompoundAssign):
            val = self._value_to_js(action.value)
            lines.append(f"{indent}{action.name} {action.op}= {val};")

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

        elif isinstance(action, ast.ForIndex):
            it = self._value_to_js(action.iterable)
            lines.append(f"{indent}(function() {{")
            lines.append(f"{indent}  var _arr = {it} || [];")
            lines.append(f"{indent}  for (var {action.idx_name} = 0; {action.idx_name} < _arr.length; {action.idx_name}++) {{")
            lines.append(f"{indent}    var {action.var_name} = _arr[{action.idx_name}];")
            for a in action.body:
                lines.extend(self._action_to_js(a, indent + "    "))
            lines.append(f"{indent}  }}")
            lines.append(f"{indent}}})();")

        elif isinstance(action, ast.ForIn):
            it = self._value_to_js(action.iterable)
            lines.append(f"{indent}for (var {action.var_name} of {it}) {{")
            for a in action.body:
                lines.extend(self._action_to_js(a, indent + "  "))
            lines.append(f"{indent}}}")

        elif isinstance(action, ast.FunctionDef):
            # تعريف دالة في JS
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

        elif isinstance(action, ast.Break):
            lines.append(f"{indent}break;")

        elif isinstance(action, ast.Continue):
            lines.append(f"{indent}continue;")

        elif isinstance(action, ast.ArrayAdd):
            target = self._value_to_js(action.target)
            item = self._value_to_js(action.item)
            lines.append(f"{indent}{target}.push({item});")

        elif isinstance(action, ast.ArrayRemove):
            target = self._value_to_js(action.target)
            idx = self._value_to_js(action.index)
            lines.append(f"{indent}{target}.splice({idx}, 1);")

        elif isinstance(action, ast.AiAsk):
            prompt = self._escape_js(action.prompt)
            lines.append(f"{indent}console.log('🤖 AI:', '{prompt}');")

        elif isinstance(action, ast.CreateQr):
            content = self._escape_js(action.content)
            size = action.size
            lines.append(f"{indent}(function() {{")
            lines.append(f"{indent}  var q = document.createElement('div');")
            lines.append(f"{indent}  q.id = 'qr_' + Date.now();")
            lines.append(f"{indent}  q.style.cssText = 'margin: 20px auto; text-align: center;';")
            lines.append(f"{indent}  var app = document.querySelector('.byan-app');")
            lines.append(f"{indent}  if (app) app.appendChild(q);")
            lines.append(f"{indent}  if (typeof QRCode !== 'undefined') {{")
            lines.append(f"{indent}    new QRCode(q, {{text: '{content}', width: {size}, height: {size}}});")
            lines.append(f"{indent}  }} else {{")
            lines.append(f"{indent}    q.textContent = 'QR: {content}';")
            lines.append(f"{indent}  }}")
            lines.append(f"{indent}}})();")

        elif isinstance(action, ast.CreatePdf):
            title = self._escape_js(action.title)
            filename = self._escape_js(action.filename)
            lines.append(f"{indent}(function() {{")
            lines.append(f"{indent}  if (typeof window.jspdf !== 'undefined') {{")
            lines.append(f"{indent}    var doc = new window.jspdf.jsPDF();")
            lines.append(f"{indent}    doc.text('{title}', 10, 10);")
            lines.append(f"{indent}    doc.save('{filename}');")
            lines.append(f"{indent}    console.log('✅ PDF: {filename}');")
            lines.append(f"{indent}  }} else {{")
            lines.append(f"{indent}    console.log('PDF: {title} -> {filename}');")
            lines.append(f"{indent}  }}")
            lines.append(f"{indent}}})();")

        elif isinstance(action, ast.AuthAction):
            act = action.action
            if act == 'login':
                user = self._escape_js(action.username)
                lines.append(f"{indent}(function() {{")
                lines.append(f"{indent}  localStorage.setItem('byan_user', '{user}');")
                lines.append(f"{indent}  localStorage.setItem('byan_token', 'token_' + Date.now());")
                lines.append(f"{indent}  console.log('✅ تم تسجيل الدخول:', '{user}');")
                lines.append(f"{indent}}})();")
            elif act == 'logout':
                lines.append(f"{indent}localStorage.removeItem('byan_user');")
                lines.append(f"{indent}localStorage.removeItem('byan_token');")
                lines.append(f"{indent}console.log('✅ تم تسجيل الخروج');")
            elif act == 'register':
                user = self._escape_js(action.username)
                lines.append(f"{indent}localStorage.setItem('byan_user', '{user}');")
                lines.append(f"{indent}console.log('📝 حساب جديد:', '{user}');")

        elif isinstance(action, ast.WebSocketConnect):
            url = self._escape_js(action.url)
            lines.append(f"{indent}(function() {{")
            lines.append(f"{indent}  try {{")
            lines.append(f"{indent}    window._ws = new WebSocket('{url}');")
            lines.append(f"{indent}    window._ws.onopen = function() {{ console.log('✅ WebSocket متصل'); }};")
            lines.append(f"{indent}    window._ws.onmessage = function(e) {{ console.log('📨 رسالة:', e.data); }};")
            lines.append(f"{indent}    window._ws.onerror = function(e) {{ console.log('❌ WebSocket:', e.message || 'خطأ'); }};")
            lines.append(f"{indent}  }} catch(e) {{ console.log('❌ WebSocket:', e.message); }}")
            lines.append(f"{indent}}})();")

        elif isinstance(action, ast.CreateMap):
            lat = action.lat
            lng = action.lng
            zoom = action.zoom
            map_id = 'map_' + str(len(self.html_elements))
            self.html_elements.append(
                f'<div id="{map_id}" style="width:100%;height:300px;border-radius:10px;margin:10px 0;"></div>'
            )
            lines.append(f"{indent}(function() {{")
            lines.append(f"{indent}  setTimeout(function() {{")
            lines.append(f"{indent}    if (typeof L !== 'undefined') {{")
            lines.append(f"{indent}      var _m = L.map('{map_id}').setView([{lat}, {lng}], {zoom});")
            lines.append(f"{indent}      L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png').addTo(map);")
            lines.append(f"{indent}      L.marker([{lat}, {lng}]).addTo(_m);")
            lines.append(f"{indent}    }}")
            lines.append(f"{indent}  }}, 300);")
            lines.append(f"{indent}}})();")

        elif isinstance(action, ast.CreateChart):
            chart_type = getattr(action, 'chart_type', 'bar') or 'bar'
            chart_id = 'chart_' + str(len(self.html_elements))
            self.html_elements.append(
                f'<canvas id="{chart_id}" style="max-width: 100%; margin: 10px 0;"></canvas>'
            )
            lines.append(f"{indent}(function() {{")
            lines.append(f"{indent}  setTimeout(function() {{")
            lines.append(f"{indent}    var _ctx = document.getElementById('{chart_id}');")
            lines.append(f"{indent}    if (_ctx && typeof Chart !== 'undefined') {{")
            lines.append(f"{indent}      new Chart(_ctx, {{")
            lines.append(f"{indent}        type: '{chart_type}',")
            lines.append(f"{indent}        data: {{")
            lines.append(f"{indent}          labels: ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو'],")
            lines.append(f"{indent}          datasets: [{{")
            lines.append(f"{indent}            label: 'البيانات',")
            lines.append(f"{indent}            data: [12, 19, 3, 5, 2],")
            lines.append(f"{indent}            backgroundColor: ['#e74c3c', '#2ecc71', '#3498db', '#f39c12', '#9b59b6']")
            lines.append(f"{indent}          }}]")
            lines.append(f"{indent}        }},")
            lines.append(f"{indent}        options: {{responsive: true}}")
            lines.append(f"{indent}      }});")
            lines.append(f"{indent}    }}")
            lines.append(f"{indent}  }}, 300);")
            lines.append(f"{indent}}})();")

        elif isinstance(action, ast.Return):
            if action.value is not None:
                val = self._value_to_js(action.value)
                lines.append(f"{indent}return {val};")
            else:
                lines.append(f"{indent}return;")

        elif isinstance(action, ast.CreateIcon):
            icon_type = action.props.get('النوع', 'star')
            icon_size = action.props.get('الحجم', 32)
            emoji_map = {
                'home': '🏠', 'user': '👤', 'settings': '⚙️',
                'star': '⭐', 'heart': '❤️', 'check': '✅',
                'search': '🔍', 'menu': '☰', 'close': '✖️',
                'add': '➕', 'delete': '🗑️', 'edit': '✏️',
                'download': '⬇️', 'upload': '⬆️', 'info': 'ℹ️',
            }
            emoji = emoji_map.get(icon_type, '⭐')
            icon_id = 'icon_' + str(len(self.html_elements))
            lines.append(f"{indent}(function() {{")
            lines.append(f"{indent}  var _i = document.createElement('span');")
            lines.append(f"{indent}  _i.textContent = '{emoji}';")
            lines.append(f"{indent}  _i.style.fontSize = '{icon_size}px';")
            lines.append(f"{indent}  _i.style.display = 'inline-block';")
            lines.append(f"{indent}  _i.style.margin = '5px';")
            lines.append(f"{indent}  var _app = document.querySelector('.byan-app');")
            lines.append(f"{indent}  if (_app) _app.appendChild(_i);")
            lines.append(f"{indent}}})();")

        elif isinstance(action, ast.PlaySound):
            url = self._escape_js(action.url)
            lines.append(f"{indent}(function() {{")
            lines.append(f"{indent}  try {{")
            lines.append(f"{indent}    var _a = new Audio('{url}');")
            lines.append(f"{indent}    _a.play().catch(function(e) {{ console.log('🔊 خطأ الصوت:', e.message); }});")
            lines.append(f"{indent}  }} catch(e) {{ console.log('🔊', e.message); }}")
            lines.append(f"{indent}}})();")

        elif isinstance(action, ast.Notify):
            title = self._escape_js(action.title)
            body = self._escape_js(action.body or action.title)
            lines.append(f"{indent}(function() {{")
            lines.append(f"{indent}  if ('Notification' in window) {{")
            lines.append(f"{indent}    if (Notification.permission === 'granted') {{")
            lines.append(f"{indent}      new Notification('{title}', {{body: '{body}'}});")
            lines.append(f"{indent}    }} else if (Notification.permission !== 'denied') {{")
            lines.append(f"{indent}      Notification.requestPermission().then(function(p) {{")
            lines.append(f"{indent}        if (p === 'granted') new Notification('{title}', {{body: '{body}'}});")
            lines.append(f"{indent}      }});")
            lines.append(f"{indent}    }}")
            lines.append(f"{indent}  }} else {{ console.log('🔔 إشعار:', '{title}'); }}")
            lines.append(f"{indent}}})();")

        elif isinstance(action, ast.ClipboardCopy):
            text = self._escape_js(action.text)
            lines.append(f"{indent}(function() {{")
            lines.append(f"{indent}  if (navigator.clipboard) {{")
            lines.append(f"{indent}    navigator.clipboard.writeText('{text}').then(function() {{ console.log('📋 تم النسخ'); }});")
            lines.append(f"{indent}  }} else {{ console.log('📋 نسخ:', '{text}'); }}")
            lines.append(f"{indent}}})();")

        elif isinstance(action, ast.ClipboardPaste):
            lines.append(f"{indent}(function() {{")
            lines.append(f"{indent}  if (navigator.clipboard) {{")
            lines.append(f"{indent}    navigator.clipboard.readText().then(function(txt) {{ console.log('📋 لصق:', txt); }});")
            lines.append(f"{indent}  }}")
            lines.append(f"{indent}}})();")

        elif isinstance(action, ast.Download):
            url = self._escape_js(action.url)
            filename = self._escape_js(action.filename or 'download')
            lines.append(f"{indent}(function() {{")
            lines.append(f"{indent}  var _a = document.createElement('a');")
            lines.append(f"{indent}  _a.href = '{url}';")
            lines.append(f"{indent}  _a.download = '{filename}';")
            lines.append(f"{indent}  document.body.appendChild(_a);")
            lines.append(f"{indent}  _a.click();")
            lines.append(f"{indent}  document.body.removeChild(_a);")
            lines.append(f"{indent}  console.log('⬇️ جاري التحميل:', '{url}');")
            lines.append(f"{indent}}})();")

        elif isinstance(action, ast.EnableDrag):
            sel = self._escape_js(action.selector)
            lines.append(f"{indent}(function() {{")
            lines.append(f"{indent}  var _el = document.querySelector('{sel}');")
            lines.append(f"{indent}  if (_el) {{")
            lines.append(f"{indent}    _el.draggable = true;")
            lines.append(f"{indent}    _el.style.cursor = 'grab';")
            lines.append(f"{indent}    _el.addEventListener('dragstart', function(e) {{")
            lines.append(f"{indent}      e.dataTransfer.setData('text/plain', '{sel}');")
            lines.append(f"{indent}    }});")
            lines.append(f"{indent}  }}")
            lines.append(f"{indent}}})();")

        elif isinstance(action, ast.EnableResize):
            sel = self._escape_js(action.selector)
            lines.append(f"{indent}(function() {{")
            lines.append(f"{indent}  var _el = document.querySelector('{sel}');")
            lines.append(f"{indent}  if (_el) {{")
            lines.append(f"{indent}    _el.style.resize = 'both';")
            lines.append(f"{indent}    _el.style.overflow = 'auto';")
            lines.append(f"{indent}    _el.style.minWidth = '100px';")
            lines.append(f"{indent}    _el.style.minHeight = '50px';")
            lines.append(f"{indent}    _el.style.border = '2px dashed #667eea';")
            lines.append(f"{indent}  }}")
            lines.append(f"{indent}}})();")

        elif isinstance(action, ast.SecureLogin):
            user = self._escape_js(action.username)
            lines.append(f"{indent}(function() {{")
            lines.append(f"{indent}  console.log('🔐 تسجيل دخول آمن:', '{user}');")
            lines.append(f"{indent}  localStorage.setItem('byan_user', '{user}');")
            lines.append(f"{indent}  localStorage.setItem('byan_token', 'jwt_' + btoa('{user}:' + Date.now()));")
            lines.append(f"{indent}  console.log('✅ تم تسجيل الدخول الآمن');")
            lines.append(f"{indent}}})();")

        elif isinstance(action, ast.PayButton):
            amount = action.amount
            currency = action.currency
            el_id = action.props.get('المعرف', 'pay_btn')
            lines.append(f"{indent}(function() {{")
            lines.append(f"{indent}  var _btn = document.getElementById('{el_id}');")
            lines.append(f"{indent}  if (_btn) {{")
            lines.append(f"{indent}    _btn.addEventListener('click', function() {{")
            lines.append(f"{indent}      console.log('💳 دفع:', '{amount} {currency}');")
            lines.append(f"{indent}      alert('تم الدفع: {amount} {currency}');")
            for a in action.actions:
                lines.extend(self._action_to_js(a, indent + "      "))
            lines.append(f"{indent}    }});")
            lines.append(f"{indent}  }}")
            lines.append(f"{indent}}})();")

        elif isinstance(action, ast.VideoCall):
            room = self._escape_js(action.room)
            lines.append(f"{indent}(function() {{")
            lines.append(f"{indent}  console.log('📹 مكالمة فيديو في غرفة:', '{room}');")
            lines.append(f"{indent}  if (navigator.mediaDevices) {{")
            lines.append(f"{indent}    navigator.mediaDevices.getUserMedia({{video: true, audio: true}})")
            lines.append(f"{indent}      .then(function(s) {{ console.log('✅ الكاميرا متاحة'); }});")
            lines.append(f"{indent}  }}")
            lines.append(f"{indent}}})();")

        elif isinstance(action, ast.PushNotify):
            lines.append(f"{indent}(function() {{")
            lines.append(f"{indent}  if ('Notification' in window) {{")
            lines.append(f"{indent}    Notification.requestPermission().then(function(p) {{")
            lines.append(f"{indent}      console.log('🔔 صلاحية الإشعارات:', p);")
            lines.append(f"{indent}    }});")
            lines.append(f"{indent}  }}")
            lines.append(f"{indent}}})();")

        elif isinstance(action, ast.CodeEditor):
            el_id = action.props.get('المعرف', 'editor')
            lang = action.props.get('اللغة', 'javascript')
            lines.append(f"{indent}(function() {{")
            lines.append(f"{indent}  var _el = document.getElementById('{el_id}');")
            lines.append(f"{indent}  if (!_el) return;")
            lines.append(f"{indent}  _el.style.cssText = 'width:100%; height:300px; border:1px solid #ddd; border-radius:8px; padding:15px; font-family:monospace; direction:ltr; text-align:left; background:#1e1e1e; color:#d4d4d4;';")
            lines.append(f"{indent}  _el.contentEditable = 'true';")
            lines.append(f"{indent}  _el.textContent = '// {lang} code here';")
            lines.append(f"{indent}}})();")

        elif isinstance(action, ast.TemplateApply):
            tmpl = self._escape_js(action.template)
            target = self._escape_js(action.target)
            lines.append(f"{indent}(function() {{")
            lines.append(f"{indent}  var _t = document.querySelector('{target}');")
            lines.append(f"{indent}  if (!_t) return;")
            lines.append(f"{indent}  var templates = {{")
            lines.append(f"{indent}    'chat': '<div style=padding:15px;><h3>💬 محادثة</h3><div style=background:#f0f0f0; padding:10px; border-radius:8px;>مرحبا!</div></div>',")
            lines.append(f"{indent}    'login': '<div style=padding:15px;><h3>🔐 تسجيل دخول</h3><input placeholder=اسم><br><input type=password placeholder=كلمة_السر></div>',")
            lines.append(f"{indent}    'card': '<div style=padding:15px; background:white; border-radius:12px; box-shadow:0 4px 12px rgba(0,0,0,0.1);>بطاقة</div>'")
            lines.append(f"{indent}  }};")
            lines.append(f"{indent}  _t.innerHTML = templates['{tmpl}'] || 'قالب غير معروف';")
            lines.append(f"{indent}}})();")

        elif isinstance(action, ast.AiLocal):
            prompt = self._escape_js(action.prompt)
            target = self._escape_js(action.target or '#out')
            lines.append(f"{indent}(function() {{")
            lines.append(f"{indent}  var _p = document.querySelector('{target}');")
            lines.append(f"{indent}  if (_p) _p.textContent = '🤖 جاري التفكير...';")
            lines.append(f"{indent}  setTimeout(function() {{")
            lines.append(f"{indent}    var _resp = 'رد محلي على: {prompt}';")
            lines.append(f"{indent}    if (_p) _p.textContent = _resp;")
            lines.append(f"{indent}  }}, 1000);")
            lines.append(f"{indent}}})();")

        elif isinstance(action, ast.Web3Connect):
            network = self._escape_js(action.network or 'ethereum')
            lines.append(f"{indent}(function() {{")
            lines.append(f"{indent}  if (typeof window.ethereum !== 'undefined') {{")
            lines.append(f"{indent}    window.ethereum.request({{method: 'eth_requestAccounts'}})")
            lines.append(f"{indent}      .then(function(acc) {{ console.log('💰 محفظة:', acc); }});")
            lines.append(f"{indent}  }} else {{ console.log('Web3 غير متاح - {network}'); }}")
            lines.append(f"{indent}}})();")

        elif isinstance(action, ast.Scene3D):
            scene_id = 'scene_' + str(len(self.html_elements))
            self.html_elements.append(
                f'<div id="{scene_id}" style="width:100%; height:300px; background:#1e1e1e; border-radius:10px; display:flex; align-items:center; justify-content:center; color:white;">'
                f'<div>🎮 مشهد 3D - {scene_id}</div>'
                f'</div>'
            )
            lines.append(f"{indent}console.log('🎮 مشهد 3D:', '{scene_id}');")

        elif isinstance(action, ast.ArScene):
            ar_id = 'ar_' + str(len(self.html_elements))
            self.html_elements.append(
                f'<div id="{ar_id}" style="width:100%; height:300px; background:#0a0a0a; border-radius:10px; display:flex; align-items:center; justify-content:center; color:#4ecdc4;">'
                f'<div>🥽 AR/VR - {ar_id}</div>'
                f'</div>'
            )

        elif isinstance(action, ast.Generator):
            name = action.name or 'generator'
            lines.append(f"{indent}function* {name}() {{")
            for a in action.body:
                lines.extend(self._action_to_js(a, indent + "  "))
            lines.append(f"{indent}}}")

        elif isinstance(action, ast.YieldValue):
            if action.value is not None:
                val = self._value_to_js(action.value)
                lines.append(f"{indent}yield {val};")
            else:
                lines.append(f"{indent}yield;")

        elif isinstance(action, ast.FunctionDef):
            params = ', '.join(action.params)
            lines.append(f"{indent}function {action.name}({params}) {{")
            for a in action.body:
                lines.extend(self._action_to_js(a, indent + "  "))
            lines.append(f"{indent}}}")

        elif isinstance(action, ast.AsyncFunc):
            params = ', '.join(action.params)
            lines.append(f"{indent}async function {action.name}({params}) {{")
            for a in action.body:
                lines.extend(self._action_to_js(a, indent + "  "))
            lines.append(f"{indent}}}")

        elif isinstance(action, ast.AwaitExpr):
            val = self._value_to_js(action.expr)
            lines.append(f"{indent}await {val};")

        elif isinstance(action, ast.ClassDef):
            extends = f" extends {action.extends}" if action.extends else ""
            lines.append(f"{indent}class {action.name}{extends} {{")
            for m in action.methods:
                lines.extend(self._action_to_js(m, indent + "  "))
            lines.append(f"{indent}}}")

        elif isinstance(action, ast.Match):
            val = self._value_to_js(action.expr)
            lines.append(f"{indent}switch ({val}) {{")
            for case in action.cases:
                case_val = self._value_to_js(case.value)
                lines.append(f"{indent}  case {case_val}:")
                for a in case.body:
                    lines.extend(self._action_to_js(a, indent + "    "))
                lines.append(f"{indent}    break;")
            lines.append(f"{indent}}}")

        elif isinstance(action, ast.ThrowError):
            msg = self._escape_js(action.message)
            lines.append(f"{indent}throw new Error('{msg}');")

        elif isinstance(action, ast.ConstDecl):
            val = self._value_to_js(action.value)
            lines.append(f"{indent}const {action.name} = {val};")

        elif isinstance(action, ast.NullCoalesce):
            left = self._value_to_js(action.left)
            right = self._value_to_js(action.right)
            lines.append(f"{indent}({left} ?? {right})")

        elif isinstance(action, ast.Try):
            # نحوّل try/catch لـ .then/.catch عشان async
            lines.append(f"{indent}(async function() {{")
            lines.append(f"{indent}  try {{")
            for a in action.body:
                # نحوّل byanCall لـ await byanCall عشان catch يشتغل
                sub_lines = self._action_to_js(a, indent + "    ")
                for sl in sub_lines:
                    # استبدل byanCall بـ await byanCall
                    sl_fixed = sl.replace("byanCall(", "await byanCall(")
                    lines.append(sl_fixed)
            lines.append(f"{indent}  }} catch(e) {{")
            if action.catch_body:
                for a in action.catch_body:
                    lines.extend(self._action_to_js(a, indent + "    "))
            else:
                lines.append(f"{indent}    console.error('❌', e);")
            lines.append(f"{indent}  }}")
            lines.append(f"{indent}}})();")

        elif isinstance(action, ast.Await):
            # نستخدم async/await لتنفيذ متتابع
            lines.append(f"{indent}(async function() {{")
            for a in action.body:
                lines.extend(self._action_to_js(a, indent + "  "))
            lines.append(f"{indent}}})();")

        elif isinstance(action, ast.BuiltinCall):
            val = self._value_to_js(action)
            lines.append(f"{indent}{val};")

        elif isinstance(action, ast.DbCreate):
            lines.append(f"{indent}// DB: {action.name}")

        elif isinstance(action, ast.DbInsert):
            table = action.table
            keys = list(action.values.keys())
            vals = [f"'{v}'" if isinstance(v, str) else str(v) for v in action.values.values()]
            sql = f"INSERT INTO {table} ({', '.join(keys)}) VALUES ({', '.join(vals)})"
            lines.append(f"{indent}byanCall('/api/db/query', {{sql: \"{sql}\"}}, function(res) {{ console.log('✅ تم الحفظ'); }});")
        elif isinstance(action, ast.DbSelect):
            table = self._escape_js(action.table)
            target = self._escape_js(action.target)
            lines.append(f"{indent}byanCall('/api/db/query', {{sql: 'SELECT * FROM {table}'}}, function(res) {{")
            lines.append(f"{indent}  var el = document.querySelector('{target}');")
            lines.append(f"{indent}  if (el) el.textContent = JSON.stringify(res.rows || []);")
            lines.append(f"{indent}}});")
        elif isinstance(action, ast.Timer):
            secs = int(action.seconds * 1000)
            lines.append(f"{indent}setInterval(function() {{")
            for a in action.body:
                lines.extend(self._action_to_js(a, indent + "  "))
            lines.append(f"{indent}}}, {secs});")

        elif isinstance(action, ast.Animate):
            selector = self._escape_js(action.selector)
            dur = action.duration
            lines.append(f"{indent}(function() {{")
            lines.append(f"{indent}  var el = document.querySelector('{selector}');")
            lines.append(f"{indent}  if (el) {{")
            lines.append(f"{indent}    el.style.transition = 'transform {dur}s ease';")
            lines.append(f"{indent}    el.style.transform = 'translate({action.x}px, {action.y}px)';")
            lines.append(f"{indent}  }}")
            lines.append(f"{indent}}})();")

        elif isinstance(action, ast.CreateElement):
            tag = self._escape_js(action.tag)
            target = self._escape_js(action.target)
            lines.append(f"{indent}(function() {{")
            lines.append(f"{indent}  var el = document.createElement('{tag}');")
            lines.append(f"{indent}  el.textContent = '{self._escape_js(action.content)}';")
            lines.append(f"{indent}  var t = document.querySelector('{target}');")
            lines.append(f"{indent}  if (t) t.appendChild(el);")
            lines.append(f"{indent}}})();")

        elif isinstance(action, ast.RemoveElement):
            sel = self._escape_js(action.selector)
            lines.append(f"{indent}(function() {{")
            lines.append(f"{indent}  var el = document.querySelector('{sel}');")
            lines.append(f"{indent}  if (el) el.remove();")
            lines.append(f"{indent}}})();")

        elif isinstance(action, ast.HttpGet):
            url = self._escape_js(action.url)
            target = self._escape_js(action.target)
            lines.append(f"{indent}fetch('{url}')")
            lines.append(f"{indent}  .then(function(r) {{ return r.json(); }})")
            lines.append(f"{indent}  .then(function(data) {{")
            lines.append(f"{indent}    document.querySelector('{target}').textContent = JSON.stringify(data);")
            lines.append(f"{indent}  }})")
            lines.append(f"{indent}  .catch(function(err) {{ console.error(err); }});")

        elif isinstance(action, ast.HttpPost):
            url = self._escape_js(action.url)
            lines.append(f"{indent}fetch('{url}', {{method: 'POST'}});")

        elif isinstance(action, ast.Break):
            lines.append(f"{indent}break;")

        elif isinstance(action, ast.Continue):
            lines.append(f"{indent}continue;")

        elif isinstance(action, ast.FileOp):
            op = action.op
            source = self._escape_js(action.source)
            target = self._escape_js(action.target)
            content = self._escape_js(action.content)
            if op == 'write':
                lines.append(f"{indent}byanCall('/api/write', {{path: '{source}', content: '{content}'}});")
            elif op == 'read':
                lines.append(f"{indent}byanCall('/api/read', {{path: '{source}'}}, function(r) {{ if(r.status==='ok') document.querySelector('#{source.split('.')[0]}').textContent = r.content; }});")

        return lines

    def _value_to_js(self, val):
        from .. import ast_nodes as ast
        if val is None:
            return "''"
        if isinstance(val, ast.Number):
            return str(val.value)
        if isinstance(val, ast.String):
            return f"'{self._escape_js(val.value)}'"
        if isinstance(val, ast.TemplateString):
            # نص مع متغيرات: "أهلاً يا {اسم}"
            parts = []
            for p in val.parts:
                if isinstance(p, ast.String):
                    parts.append(f"'{self._escape_js(p.value)}'")
                elif isinstance(p, ast.VarRef):
                    # نتحقق من الوجود في JS
                    parts.append(f"(typeof {p.name} !== 'undefined' ? {p.name} : '')")
                else:
                    parts.append(self._value_to_js(p))
            if not parts:
                return "''"
            return " + ".join(parts)
        if isinstance(val, ast.VarRef):
            # لو اسم الدالة "اقرأ_قيمة" مش هتجي هنا لأنها FunctionCall
            return val.name
        if isinstance(val, ast.FunctionCall):
            # دعم اقرأ_قيمة و اكتب_قيمة
            if val.name == 'اقرأ_قيمة':
                if val.args:
                    target = self._value_to_js(val.args[0])
                    return f"parseFloat(document.querySelector({target}).value) || 0"
                return "0"
            if val.name == 'اقرأ_نص':
                if val.args:
                    target = self._value_to_js(val.args[0])
                    return f"document.querySelector({target}).value"
                return "''"
            if val.name == 'اقرأ_عنصر':
                if val.args:
                    target = self._value_to_js(val.args[0])
                    return f"document.querySelector({target}).textContent"
                return "''"
            if val.name == 'طول':
                if val.args:
                    target = self._value_to_js(val.args[0])
                    return f"{target}.length"
                return "0"
            # دالة عادية
            args = ', '.join(self._value_to_js(a) for a in val.args)
            return f"{val.name}({args})"
        if isinstance(val, ast.BinOp):
            if val.op == '' and hasattr(val.left, 'value') and str(val.left.value) == '!':
                inner = self._value_to_js(val.right)
                return f"!({inner})"
            return f"({self._value_to_js(val.left)} {val.op} {self._value_to_js(val.right)})"
        if isinstance(val, ast.Compare):
            return f"({self._value_to_js(val.left)} {val.op} {self._value_to_js(val.right)})"
        # Template string: "أهلاً يا {اسم}"
        if hasattr(ast, 'TemplateString') and isinstance(val, ast.TemplateString):
            parts = []
            for p in val.parts:
                if isinstance(p, ast.String):
                    parts.append(p.value.replace('`', '\\`'))
                elif isinstance(p, ast.VarRef):
                    parts.append('${' + p.name + '}')
                else:
                    # أي نوع تاني (DateCall, FunctionCall, إلخ)
                    try:
                        js = self._value_to_js(p)
                        parts.append('${' + js + '}')
                    except:
                        parts.append('')
            return '`' + ''.join(parts) + '`'

        # لا_شيء → null
        if hasattr(ast, 'NullLit') and isinstance(val, ast.NullLit):
            return "null"

        # BuiltinCall
        if hasattr(ast, 'BuiltinCall') and isinstance(val, ast.BuiltinCall):
            return self._builtin_to_js(val.name, val.args)

        # قائمة [1, 2, 3]
        if hasattr(ast, 'ListLiteral') and isinstance(val, ast.ListLiteral):
            items = ', '.join(self._value_to_js(i) for i in val.items)
            return f"[{items}]"
        # فهرسة مصفوفة[0] أو مصفوفة[0][1]
        if hasattr(ast, 'IndexAccess') and isinstance(val, ast.IndexAccess):
            target = self._value_to_js(val.target)
            index = self._value_to_js(val.index)
            return f"{target}[{index}]"
        # DateCall
        if hasattr(ast, 'DateCall') and isinstance(val, ast.DateCall):
            if val.func in ('الآن',):
                return "new Date().toISOString()"
            elif val.func in ('اليوم',):
                return "new Date().toLocaleDateString('ar-EG')"
            return "new Date()"

        # Lambda
        if hasattr(ast, 'Lambda') and isinstance(val, ast.Lambda):
            params = ', '.join(val.params)
            body = self._value_to_js(val.body)
            return f"(({params}) => {body})"
        # ArrayAdd داخل تعبير
        if hasattr(ast, 'ArrayAdd') and isinstance(val, ast.ArrayAdd):
            target = self._value_to_js(val.target)
            item = self._value_to_js(val.item)
            return f"({target}.push({item}))"
        # NOT (!): نستخدم String('!') كعلامة
        if isinstance(val, ast.BinOp) and val.op == '' and str(getattr(val.left, 'value', '')) == '!':
            inner = self._value_to_js(val.right)
            return f"!({inner})"
        if isinstance(val, (int, float)):
            return str(val)
        return f"'{val}'"


    def _builtin_to_js(self, name, args):
        """يحوّل الدوال المدمجة لـ JS"""
        if name in ('رتب', 'sort'):
            if args:
                a = self._value_to_js(args[0])
                return f"{a}.slice().sort((a,b)=>a-b)"
            return "[]"
        elif name in ('اعكس', 'reverse'):
            if args:
                return f"{self._value_to_js(args[0])}.slice().reverse()"
            return "[]"
        elif name in ('أول', 'first'):
            if args:
                return f"{self._value_to_js(args[0])}[0]"
            return "null"
        elif name in ('آخر', 'last'):
            if args:
                a = self._value_to_js(args[0])
                return f"{a}[{a}.length-1]"
            return "null"
        elif name in ('رقم', 'to_num'):
            if args:
                return f"parseFloat({self._value_to_js(args[0])})"
            return "0"
        elif name in ('نص', 'to_str'):
            if args:
                return f"String({self._value_to_js(args[0])})"
            return "''"
        elif name in ('قسم', 'split'):
            if len(args) >= 2:
                return f"{self._value_to_js(args[0])}.split({self._value_to_js(args[1])})"
            return "[]"
        elif name in ('استبدل', 'replace'):
            if len(args) >= 3:
                a = self._value_to_js(args[0])
                b = self._value_to_js(args[1])
                cc = self._value_to_js(args[2])
                return f"{a}.split({b}).join({cc})"
            return "''"
        elif name in ('اقتطع', 'substr'):
            if len(args) >= 3:
                a = self._value_to_js(args[0])
                return f"{a}.substring({self._value_to_js(args[1])}, {self._value_to_js(args[2])})"
            return "''"
        elif name in ('جذر', 'sqrt'):
            if args:
                return f"Math.sqrt({self._value_to_js(args[0])})"
            return "0"
        elif name in ('قوة', 'pow', 'power'):
            if len(args) >= 2:
                return f"Math.pow({self._value_to_js(args[0])}, {self._value_to_js(args[1])})"
            return "0"
        elif name in ('عشوائي', 'random'):
            if len(args) >= 2:
                a = self._value_to_js(args[0])
                b = self._value_to_js(args[1])
                return f"(Math.floor(Math.random() * ({b} - {a} + 1)) + {a})"
            return "Math.random()"
        elif name in ('تقريب', 'round'):
            if args:
                return f"Math.round({self._value_to_js(args[0])})"
            return "0"
        elif name in ('يحتوي', 'contains'):
            if len(args) >= 2:
                return f"{self._value_to_js(args[0])}.includes({self._value_to_js(args[1])})"
            return "false"
        elif name in ('يبدأ_بـ', 'startsWith'):
            if len(args) >= 2:
                return f"{self._value_to_js(args[0])}.startsWith({self._value_to_js(args[1])})"
            return "false"
        elif name in ('ينتهي_بـ', 'endsWith'):
            if len(args) >= 2:
                return f"{self._value_to_js(args[0])}.endsWith({self._value_to_js(args[1])})"
            return "false"
        elif name in ('شذّب', 'trim'):
            if args:
                return f"{self._value_to_js(args[0])}.trim()"
            return "''"
        elif name in ('ابحث', 'find'):
            if len(args) >= 2:
                return f"{self._value_to_js(args[0])}.find({self._value_to_js(args[1])})"
            return "-1"
        elif name in ('صفّي', 'filter'):
            if len(args) >= 2:
                return f"{self._value_to_js(args[0])}.filter({self._value_to_js(args[1])})"
            return "[]"
        elif name in ('حوّل', 'map'):
            if len(args) >= 2:
                return f"{self._value_to_js(args[0])}.map({self._value_to_js(args[1])})"
            return "[]"
        elif name in ('قلل', 'reduce'):
            if len(args) >= 3:
                return f"{self._value_to_js(args[0])}.reduce({self._value_to_js(args[1])}, {self._value_to_js(args[2])})"
            elif len(args) >= 2:
                return f"{self._value_to_js(args[0])}.reduce({self._value_to_js(args[1])})"
            return "null"
        elif name in ('طابق_نمط', 'regex'):
            if len(args) >= 2:
                a = self._value_to_js(args[0])
                b = self._value_to_js(args[1])
                return f"new RegExp({b}).test({a})"
            return "false"
        elif name in ('حوّل_JSON', 'stringify'):
            if args:
                return f"JSON.stringify({self._value_to_js(args[0])})"
            return "''"
        elif name in ('اقرأ_JSON', 'parse'):
            if args:
                return f"JSON.parse({self._value_to_js(args[0])})"
            return "null"
        else:
            args_js = ', '.join(self._value_to_js(a) for a in args)
            return f"{name}({args_js})"

    def _escape(self, s):
        if s is None:
            return ''
        return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

    def _escape_js(self, s):
        if s is None:
            return ''
        return str(s).replace('\\', '\\\\').replace("'", "\\'")

    def _build_html(self):
        # ابحث عن Dark Mode و Language
        dark_mode = False
        lang = 'ar'
        from .. import ast_nodes as ast
        for el in self.program.elements:
            if isinstance(el, ast.DarkMode):
                dark_mode = True
            elif isinstance(el, ast.Language):
                lang = el.lang or 'ar'

        title = self.window_props.get('العنوان', self.program.name or 'برنامج بيان')
        elements_html = chr(10) + '    ' + (chr(10) + '    ').join(self.html_elements) if self.html_elements else '<h1>مرحبًا بك في بيان</h1>'

        return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#667eea">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <link rel="manifest" href="manifest.json">
    <link rel="icon" href="icon.svg" type="image/svg+xml">
    <link rel="apple-touch-icon" href="icon.svg">
    <title>{self._escape(title)}</title>
    <link rel="stylesheet" href="style.css">
    <script src="https://cdn.jsdelivr.net/npm/qrcode@1.5.3/build/qrcode.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/jspdf@2.5.1/dist/jspdf.umd.min.js"></script>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
    <script src="https://cdn.jsdelivr.net/npm/three@0.150.0/build/three.min.js"></script>
</head>
<body>
    <div class="byan-app">
    {elements_html}
    </div>
    <script src="script.js"></script>
    <script>
      if ('serviceWorker' in navigator) {{
        navigator.serviceWorker.register('sw.js')
          .then(function(reg) {{ console.log('OK PWA'); }})
          .catch(function(err) {{ console.error('PWA:', err); }});
      }}
    </script>
</body>
</html>"""


    def _build_css(self):
        bg = self.color(self.window_props.get('لون_الخلفية')) or '#667eea'

        return f'''body {{
    font-family: 'Cairo', 'Tahoma', sans-serif;
    background: {bg};
    color: #2c3e50;
    margin: 0;
    padding: 0;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.byan-app {{
    background: rgba(255, 255, 255, 0.95);
    padding: 40px;
    border-radius: 20px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    min-width: 320px;
    max-width: 700px;
    text-align: center;
}}

h1 {{
    margin: 0 0 20px 0;
    color: #2c3e50;
}}

p {{
    margin: 10px 0;
    color: #555;
}}

button {{
    padding: 12px 30px;
    font-size: 16px;
    font-weight: bold;
    border: none;
    border-radius: 10px;
    color: white;
    cursor: pointer;
    margin: 8px;
    transition: transform 0.2s, box-shadow 0.2s;
}}

button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.2);
}}

input {{
    padding: 12px 20px;
    font-size: 16px;
    border: 2px solid #ddd;
    border-radius: 10px;
    margin: 8px;
    width: 80%;
    max-width: 300px;
    font-family: inherit;
}}

input:focus {{
    outline: none;
    border-color: #667eea;
}}'''


    def _add_function(self, el):
        """يضيف تعريف دالة في JS"""
        from .. import ast_nodes as ast
        params = ', '.join(el.params)
        # نجمع السطور الأول
        lines_to_add = [f"function {el.name}({params}) {{"]
        for a in el.body:
            lines_to_add.extend(self._action_to_js(a, "  "))
        lines_to_add.append("}")
        lines_to_add.append("")
        # ضيفها كلها مرة واحدة في البداية
        for line in reversed(lines_to_add):
            self.js_events.insert(0, line)


    def _build_js(self):
        header = '''// ===== Byan Runtime (standalone) =====
var BYAN_DATA = {};
try { BYAN_DATA = JSON.parse(localStorage.getItem('byan_data') || '{}'); } catch(e) {}

function _byanSave() {
  try { localStorage.setItem('byan_data', JSON.stringify(BYAN_DATA)); } catch(e) {}
}

function byanReadFile(path) {
  return BYAN_DATA['file:' + path] || '';
}

function byanWriteFile(path, content) {
  BYAN_DATA['file:' + path] = String(content);
  _byanSave();
  return true;
}

function byanDbInsert(table, record) {
  if (!BYAN_DATA['db:' + table]) BYAN_DATA['db:' + table] = [];
  BYAN_DATA['db:' + table].push(record);
  _byanSave();
  return true;
}

function byanDbSelect(table, filter) {
  return BYAN_DATA['db:' + table] || [];
}

function byanLog() {
  console.log('[Byan]', Array.prototype.slice.call(arguments).join(' '));
}

function byanPath(p) { return p; }

function byanCall(endpoint, data, callback) {
  var res = {status: 'ok'};
  if (endpoint === '/api/read') {
    res.content = byanReadFile(data.path);
  } else if (endpoint === '/api/write') {
    byanWriteFile(data.path, data.content);
  } else {
    res.status = 'error';
    res.message = 'غير مدعوم في standalone';
  }
  if (callback) callback(res);
  return Promise.resolve(res);
}
'''

        events = '\n'.join(self.js_events) if self.js_events else '// لا توجد أحداث'

        return header + '\n' + events
