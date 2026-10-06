from .tokens import Token, TokenType


KEYWORDS = {
    'انا_برنامج': TokenType.PROGRAM,
    'اسمي': TokenType.NAME,
    'الاسم': TokenType.FILE_NAME,
    'المعرف': TokenType.FILE_NAME,
    'في': TokenType.IN,

    'متغير': TokenType.VAR_KW,
    'اجعل': TokenType.VAR_ASSIGN,
    'و': TokenType.AND,
    'أو': TokenType.OR,
    'ليس': TokenType.NOT,

    'وظيفتي': TokenType.PURPOSE,
    'واجهتي_الرسومية': TokenType.UI_FILE,
'أنظمة_التشغيل': TokenType.OS,
    'الكود': TokenType.CODE_START,
    'نهاية': TokenType.END,
    'أنشئ': TokenType.CREATE,
    'انشئ': TokenType.CREATE,
    'انشئ_ملفا': TokenType.NEW_FILE,
    'انشئ_مجلدا': TokenType.NEW_FOLDER,
    'نافذة': TokenType.WINDOW,
    'زرا': TokenType.BUTTON,
    'عنوانا': TokenType.TITLE,
    'نصا': TokenType.TEXT,
    'مدخلا': TokenType.INPUT,

    'نافذة': TokenType.WINDOW,
    'زر': TokenType.BUTTON,
    'عنوان': TokenType.TITLE,
'مدخل': TokenType.INPUT,
    'صورة': TokenType.IMAGE,
    'فيديو': TokenType.VIDEO,
    'ملف': TokenType.FILE,
    'مجلد': TokenType.FOLDER,
    'العنوان': TokenType.TITLE_PROP,
    'الحجم': TokenType.SIZE,
    'لون_الخلفية': TokenType.BG_COLOR,
    'لون_النص': TokenType.TEXT_COLOR,
    'حجم_الخط': TokenType.FONT_SIZE,
    'الموقع': TokenType.POSITION,
    'المسار': TokenType.PATH,
    'المحتوى': TokenType.CONTENT,
    'بامتداد': TokenType.EXTENSION,
    'عند_الضغط': TokenType.ON_CLICK,
    'عند_التغيير': TokenType.ON_CHANGE,
    'فعّل': TokenType.ACTIVATE,
    'اعرض_في': TokenType.SHOW,
    'امسح': TokenType.CLEAR,
    'اخفي': TokenType.HIDE,
    'اقرأ': TokenType.READ,
    'غيّر': TokenType.CHANGE,
    'أنشئ_ملفًا': TokenType.NEW_FILE,
    'أنشئ_مجلدًا': TokenType.NEW_FOLDER,
    'انسخ': TokenType.COPY,
    'انقل': TokenType.MOVE,
    'احذف': TokenType.DELETE,
    'احفظ': TokenType.SAVE,
    'افتح': TokenType.OPEN,
    'أضف_سطرًا': TokenType.ADD_LINE,
    'اربط': TokenType.LINK,
    'لو': TokenType.IF,
    'إذا': TokenType.IF,
    'اذا': TokenType.IF,
    'إن': TokenType.IF,
    'وإلا': TokenType.ELSE,
    'والا': TokenType.ELSE,
    'طالما': TokenType.WHILE,
    'لكل': TokenType.FOR,
    'لكل_بفهرس': TokenType.FOR_INDEX,
    'qr': TokenType.QR_KW,
    'ملف_PDF': TokenType.PDF_KW,
    'تسجيل_دخول': TokenType.LOGIN,
    'تسجيل_خروج': TokenType.LOGOUT,
    'حساب_جديد': TokenType.REGISTER,
    'اتصال_مباشر': TokenType.WS_KW,
    'خريطة': TokenType.MAP_KW,
    'أيقونة': TokenType.ICON,
    'الحقول': TokenType.FIELDS,
    'العناصر': TokenType.ELEMENTS,
    'التبويبات': TokenType.TABS_LIST,
    'الأعمدة': TokenType.COLUMNS,
    'شغل_صوت': TokenType.PLAY_SOUND,
    'فعّل_سحب': TokenType.ENABLE_DRAG,
    'زر_دفع': TokenType.PAY_BUTTON,
    'اسأل_ai_محلي': TokenType.AI_LOCAL,
    'غير_متزامن': TokenType.ASYNC_KW,
    'انتظر_وعد': TokenType.AWAIT_KW,
    'صنف': TokenType.CLASS_KW,
    'هذا': TokenType.SELF,
    'أساس': TokenType.SUPER,
    'الأساس': TokenType.SUPER,
    'الجد': TokenType.SUPER,
    'هذه': TokenType.SELF,
    'جديد': TokenType.NEW,
    'محلي': TokenType.LOCAL,
    'عالمي': TokenType.GLOBAL,
    'غير_محلي': TokenType.NONLOCAL,
    'في_الخارج': TokenType.GLOBAL,
    'في_الأب': TokenType.NONLOCAL,
    'فئة': TokenType.CLASS_KW,
    'فئه': TokenType.CLASS_KW,
    'ثابت': TokenType.CONST_KW,
    'الآن': TokenType.NOW,
    'جذر': TokenType.SQRT,
    'ابحث': TokenType.FIND,
    'افتح_نافذة_منبثقة': TokenType.MODAL,
    'شريط_تنقل': TokenType.NAVBAR,
    'شريط_جانبي': TokenType.SIDEBAR,
    'قائمة_طي': TokenType.ACCORDION,
    'نافذة_منبثقة': TokenType.MODAL,
    'تلميح': TokenType.TOOLTIP,

    'افتح_نافذة': TokenType.MODAL,
    'أضف_تلميح': TokenType.TOOLTIP,
    'انشئ_قائمة_طي': TokenType.ACCORDION,
    'انشئ_شريط_جانبي': TokenType.SIDEBAR,
    'انشئ_شريط_تنقل': TokenType.NAVBAR,

    'صفّي': TokenType.FILTER,
    'حوّل': TokenType.MAP_METHOD,
    'قلل': TokenType.REDUCE,
    'طابق_نمط': TokenType.REGEX_MATCH,
    'حوّل_JSON': TokenType.JSON_STRINGIFY,
    'اقرأ_JSON': TokenType.JSON_PARSE,
    'اختر_ملف': TokenType.UPLOAD,
    'انشئ_شريط_تقدم': TokenType.PROGRESS_BAR,

    'قوة': TokenType.POWER,
    'عشوائي': TokenType.RANDOM,
    'تقريب': TokenType.ROUND,
    'يحتوي': TokenType.CONTAINS,
    'يبدأ_بـ': TokenType.STARTS_WITH,
    'ينتهي_بـ': TokenType.ENDS_WITH,
    'شذّب': TokenType.TRIM,

    'اليوم': TokenType.TODAY,
    'يرث': TokenType.EXTENDS,
    'يمتد': TokenType.EXTENDS,
    'يمتد_من': TokenType.EXTENDS,
    'واجهة': TokenType.INTERFACE_KW,
    'عام': TokenType.GENERIC_KW,
    'طابق': TokenType.MATCH_KW,
    'حالة': TokenType.CASE_KW,
    'أخيراً': TokenType.FINALLY_KW,
    'أخيرًا': TokenType.FINALLY_KW,
    'اخيرا': TokenType.FINALLY_KW,
    'وأخيراً': TokenType.FINALLY_KW,
    'ارمِ': TokenType.THROW_KW,
    'ارمِ_خطأ': TokenType.THROW_KW,
    'ارمِ_غلطة': TokenType.THROW_KW,

    'محفظة': TokenType.WEB3,
    'اتصل_محفظة': TokenType.WEB3,
    'انشئ_مشهد_3d': TokenType.GAME_3D,
    'انشئ_ar': TokenType.AR_VR,
    'اصنع_جيل': TokenType.GENERATOR,
    'حاصل': TokenType.YIELD_KW,

    'اتصال_فيديو': TokenType.VIDEO_CALL,
    'اطلب_إشعارات_push': TokenType.PUSH_NOTIFY,
    'انشئ_محرر_كود': TokenType.CODE_EDITOR,
    'طبق_قالب': TokenType.TEMPLATE_APPLY,

    'فعّل_تحجيم': TokenType.ENABLE_RESIZE,
    'وضع_ليلي': TokenType.DARK_MODE,
    'اللغة': TokenType.LANGUAGE,
    'تسجيل_دخول_آمن': TokenType.SECURE_LOGIN,

    'صوت': TokenType.PLAY_SOUND,
    'أظهر_إشعار': TokenType.NOTIFY,
    'إشعار': TokenType.NOTIFY,
    'انسخ_للحافظة': TokenType.CLIPBOARD_COPY,
    'الصق': TokenType.CLIPBOARD_PASTE,
    'حمل': TokenType.DOWNLOAD,

    'البيانات': TokenType.DATA_ROWS,
    'عند_الإرسال': TokenType.ON_SUBMIT,
    'الموقع': TokenType.LAT,
    'العرض': TokenType.LNG,
    'التكبير': TokenType.ZOOM,
    'WebSocket': TokenType.WS_KW,
    'PDF': TokenType.PDF_KW,
    'QR': TokenType.QR_KW,
    'دالة': TokenType.FUNCTION,
    'توقف': TokenType.BREAK,
    'حاول': TokenType.TRY,
    'لو_فشل': TokenType.CATCH,
    'التقط': TokenType.CATCH,
    'التقط_خطأ': TokenType.CATCH,
    'لو_نجح': TokenType.TRY,
    'انتظر': TokenType.AWAIT,
    'لا_شيء': TokenType.NULL_LIT,
    'رتب': TokenType.SORT,
    'اعكس': TokenType.REVERSE,
    'أول': TokenType.FIRST,
    'آخر': TokenType.LAST,
    'رقم': TokenType.TO_NUM,
    'إلى_نص': TokenType.TO_STR,
    'حوّل_لنص': TokenType.TO_STR,
    # 'نص': TokenType.TO_STR,   # disabled — اسم شائع للمتغيرات
    'قسم': TokenType.SPLIT,
    'استبدل': TokenType.REPLACE,
    'اقتطع': TokenType.SUBSTR,
    'شبكة': TokenType.GRID,
    'جدول': TokenType.TABLE,
    'رسم_بياني': TokenType.CHART,
    'نموذج': TokenType.FORM,
    'تبويبات': TokenType.TABS,
    'استورد': TokenType.IMPORT,
    'اسأل_المستخدم': TokenType.INPUT_ASK,

    'قاعدة_بيانات': TokenType.DB_KW,
    'اضف_سجل': TokenType.INSERT_KW,
    'أضف_سجل': TokenType.INSERT_KW,
    'اضف': TokenType.INSERT_KW,
    'أضف_سجل': TokenType.INSERT_KW,
    'اضف_سجلا': TokenType.INSERT_KW,
    'انشئ_قاعدة': TokenType.DB_KW,
    'أنشئ_قاعدة': TokenType.DB_KW,
'اقرأ_سجلات': TokenType.SELECT_KW,
    'كل': TokenType.EVERY,
    'ثانية': TokenType.SECOND,
    'حرّك': TokenType.ANIMATE,
    'إلى': TokenType.IN,
    'ضيف_عنصر': TokenType.CREATE_ELEMENT,
    'امسح_عنصر': TokenType.REMOVE_ELEMENT,
    'اتصل': TokenType.HTTP_GET,
    'ارسل': TokenType.HTTP_POST,

    # 'أضف': TokenType.ADD_ITEM,   # disabled — يتعارض مع builtin
    'أضف_عنصر': TokenType.ADD_ITEM,
    'أضف_للواجهة': TokenType.ADD_ITEM,
    'احذف_عنصر': TokenType.REMOVE_ITEM,
    'قائمة_منسدلة': TokenType.SELECT,
    'خيار': TokenType.OPTION,
    'اسأل': TokenType.AI_ASK,
    'الذكاء_الاصطناعي': TokenType.AI_ASK,
    'صورة': TokenType.IMAGE,
    'فيديو': TokenType.VIDEO,

    'استمر': TokenType.CONTINUE,
    'بعدين': TokenType.ELSE_IF,
    'أكمل': TokenType.CONTINUE,
    'اخرج': TokenType.BREAK,

    'طول': TokenType.LENGTH,
    'عنوانا': TokenType.TITLE,
    'نصا': TokenType.TEXT,
    'مدخلا': TokenType.INPUT,
    'زرا': TokenType.BUTTON,
    'نافذة': TokenType.WINDOW,
    'النوع': TokenType.IDENTIFIER_PROP,
    'العرض': TokenType.SIZE,
    'الارتفاع': TokenType.SIZE,
    'أعلى': TokenType.POSITION,
    'أسفل': TokenType.POSITION,
    'منتصف': TokenType.POSITION,
'لون': TokenType.BG_COLOR,
    'الحدود': TokenType.IDENTIFIER_PROP,
    'ظل': TokenType.IDENTIFIER_PROP,
    'الحواف': TokenType.IDENTIFIER_PROP,

    'اكتب': TokenType.SAVE,
    'فيه': TokenType.IN,
    'بمحتوى': TokenType.CONTENT,
    # 'قائمة': TokenType.NEW_FOLDER,  # disabled — اسم شائع للمتغيرات
    'أنشئ_قائمة': TokenType.NEW_FOLDER,
    'نفّذ': TokenType.OPEN,
    'شغّل': TokenType.OPEN,
    'إلى': TokenType.IN,
    'الى': TokenType.IN,

    'ارجع': TokenType.RETURN,
}


class Lexer:
    def __init__(self, source):
        self.source = source
        self.pos = 0
        self.line = 1
        self.col = 1
        self.tokens = []

    def error(self, msg):
        raise SyntaxError(f"خطأ في السطر {self.line}: {msg}")

    def peek(self, offset=0):
        idx = self.pos + offset
        return self.source[idx] if idx < len(self.source) else '\0'

    def advance(self):
        c = self.source[self.pos]
        self.pos += 1
        if c == '\n':
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return c

    def add(self, type, value):
        self.tokens.append(Token(type, value, self.line, self.col))

    def tokenize(self):
        self.indent_stack = [0]
        at_line_start = True

        while self.pos < len(self.source):
            c = self.peek()

            # حساب الـ indent في بداية السطر (حتى لو مفيش مسافات)
            if at_line_start:
                # تجاهل السطور الفاضية
                if c == '\n':
                    self.add(TokenType.NEWLINE, '\n')
                    self.advance()
                    continue

                # لو تعليق، تجاهله
                if c == '#':
                    while self.pos < len(self.source) and self.peek() != '\n':
                        self.advance()
                    continue

                # احسب الـ indent
                indent = 0
                while self.pos < len(self.source) and self.peek() in ' \t':
                    if self.peek() == ' ':
                        indent += 1
                    else:
                        indent += 4
                    self.advance()

                # لو السطر فاضي أو تعليق بعد المسافات
                if self.peek() == '\n':
                    self.add(TokenType.NEWLINE, '\n')
                    self.advance()
                    continue

                if self.peek() == '#':
                    while self.pos < len(self.source) and self.peek() != '\n':
                        self.advance()
                    continue

                # قارن مع الـ indent السابق
                current = self.indent_stack[-1]
                if indent > current:
                    self.indent_stack.append(indent)
                    self.add(TokenType.INDENT, indent)
                elif indent < current:
                    while len(self.indent_stack) > 1 and indent < self.indent_stack[-1]:
                        self.indent_stack.pop()
                        self.add(TokenType.DEDENT, indent)

                at_line_start = False
                continue

            # بداية سطر جديد
            if c == '\n':
                self.add(TokenType.NEWLINE, '\n')
                self.advance()
                at_line_start = True
                continue

            at_line_start = False

            if c in ' \t\r':
                self.advance()
                continue

            if c == '#':
                while self.pos < len(self.source) and self.peek() != '\n':
                    self.advance()
                continue

            if c == '\n':
                self.add(TokenType.NEWLINE, '\n')
                self.advance()
                continue

            # نص مثلث """
            if self.source[self.pos:self.pos + 3] == '"""':
                self.advance(); self.advance(); self.advance()
                content = ''
                while self.pos < len(self.source):
                    if self.source[self.pos:self.pos + 3] == '"""':
                        self.advance(); self.advance(); self.advance()
                        break
                    content += self.advance()
                self.add(TokenType.STRING, content.strip())
                continue

            # نص عادي
            if c == '"':
                self.advance()
                content = ''
                while self.pos < len(self.source) and self.peek() != '"':
                    if self.peek() == '\\':
                        self.advance()
                        esc = self.advance()
                        content += {'n': '\n', 't': '\t', '"': '"'}.get(esc, esc)
                    else:
                        content += self.advance()
                if self.peek() != '"':
                    self.error("نص غير مغلق")
                self.advance()
                self.add(TokenType.STRING, content)
                continue

            # رقم (يدعم العشريات)
            if c.isdigit():
                num = ''
                has_dot = False
                while self.pos < len(self.source):
                    ch = self.peek()
                    if ch.isdigit():
                        num += self.advance()
                    elif ch == '.' and not has_dot and self.peek(1).isdigit():
                        num += self.advance()
                        has_dot = True
                    else:
                        break
                if has_dot:
                    self.add(TokenType.NUMBER, float(num))
                else:
                    self.add(TokenType.NUMBER, int(num))
                continue

            # كلمة (عربي أو إنجليزي)
            if c.isalpha() or c == '_' or '\u0600' <= c <= '\u06FF':
                word = ''
                while (self.pos < len(self.source) and
                       (self.peek().isalnum() or self.peek() == '_'
                        or ('\u0600' <= self.peek() <= '\u06FF'
                            and self.peek() not in '،؛؟'))):
                    word += self.advance()

                if word in ('صح', 'غلط'):
                    self.add(TokenType.BOOLEAN, word == 'صح')
                elif word in KEYWORDS:
                    self.add(KEYWORDS[word], word)
                else:
                    self.add(TokenType.IDENTIFIER, word)
                continue


            # مسار ملف (يبدأ بـ ./ ) — قبل الرموز عشان النقطة
            if c == '.' and self.peek(1) == '/':
                path = ''
                while self.pos < len(self.source) and self.peek() not in ' \t\n':
                    path += self.advance()
                self.add(TokenType.STRING, path)
                continue

            # رموز
            symbols = {
                ':': TokenType.COLON,
                '،': TokenType.COMMA,
                ',': TokenType.COMMA,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                '{': TokenType.LBRACE,
                '[': TokenType.LBRACKET,
                ']': TokenType.RBRACKET,
                '}': TokenType.RBRACE,
                '×': TokenType.MULTIPLY,
                '*': TokenType.MULTIPLY,
                '/': TokenType.DIVIDE,
                '%': TokenType.MODULO,
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '.': TokenType.DOT,
            }
            if c in symbols:
                self.add(symbols[c], c)
                self.advance()
                continue


            # ===== رموز مركبة (لازم تكون قبل البسيطة) =====
            if c == '>' and self.peek(1) == '=':
                self.advance(); self.advance()
                self.add(TokenType.GREATER_EQ, '>=')
                continue
            if c == '<' and self.peek(1) == '=':
                self.advance(); self.advance()
                self.add(TokenType.LESS_EQ, '<=')
                continue
            if c == '=' and self.peek(1) == '=':
                self.advance(); self.advance()
                self.add(TokenType.EQUAL_EQUAL, '==')
                continue
            if c == '|' and self.peek(1) == '|':
                self.advance(); self.advance()
                self.add(TokenType.OR, '||')
                continue
            if c == '!' and self.peek(1) == '=':
                self.advance(); self.advance()
                self.add(TokenType.NOT_EQUAL, '!=')
                continue
            if c == '+' and self.peek(1) == '=':
                self.advance(); self.advance()
                self.add(TokenType.PLUS_EQ, '+=')
                continue
            if c == '-' and self.peek(1) == '=':
                self.advance(); self.advance()
                self.add(TokenType.MINUS_EQ, '-=')
                continue

            # ===== رموز بسيطة =====
            if c == '>':
                self.advance()
                self.add(TokenType.GREATER, '>')
                continue
            if c == '<':
                self.advance()
                self.add(TokenType.LESS, '<')
                continue
            if c == '=':
                self.advance()
                self.add(TokenType.EQUALS, '=')
                continue

            self.error(f"رمز غير معروف: {c!r}")

        self.add(TokenType.EOF, None)
        return self.tokens
