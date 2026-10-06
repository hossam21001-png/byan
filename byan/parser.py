from .tokens import TokenType
from . import ast_nodes as ast


PROP_TOKENS = {
    TokenType.TITLE_PROP, TokenType.SIZE, TokenType.BG_COLOR,
    TokenType.TEXT_COLOR, TokenType.FONT_SIZE, TokenType.POSITION,
    TokenType.PATH, TokenType.CONTENT, TokenType.EXTENSION,
    TokenType.NAME, TokenType.FILE_NAME, TokenType.TEXT,
    TokenType.TITLE, TokenType.IDENTIFIER, TokenType.IDENTIFIER_PROP,
    TokenType.WINDOW, TokenType.BUTTON, TokenType.INPUT,
}


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self, offset=0):
        idx = self.pos + offset
        if idx < len(self.tokens):
            return self.tokens[idx]
        return self.tokens[-1]

    def next(self):
        t = self.tokens[self.pos]
        self.pos += 1
        return t

    def expect(self, type_):
        t = self.next()
        if t.type != type_:
            raise SyntaxError(
                f"السطر {t.line}: متوقع {type_.name}، وجد {t.type.name} ({t.value!r})"
            )
        return t

    def skip_newlines(self):
        while self.peek().type == TokenType.NEWLINE:
            self.next()

    def parse(self):
        program = ast.Program()
        self.skip_newlines()
        self.expect(TokenType.PROGRAM)
        self.skip_newlines()

        while self.peek().type != TokenType.CODE_START:
            t = self.peek()
            if t.type == TokenType.EOF:
                raise SyntaxError("لم أجد كلمة 'الكود'")
            if t.type == TokenType.NEWLINE:
                self.next()
                continue
            if t.type in (TokenType.NAME, TokenType.PURPOSE,
                          TokenType.UI_FILE, TokenType.DB, TokenType.OS):
                key = self.next()
                self.expect(TokenType.COLON)
                value = self.read_value()
                self.skip_newlines()
                if key.type == TokenType.NAME:
                    program.name = value
                elif key.type == TokenType.PURPOSE:
                    program.purpose = value
                elif key.type == TokenType.UI_FILE:
                    program.ui_file = value
                elif key.type == TokenType.DB:
                    program.database = value
                elif key.type == TokenType.OS:
                    program.os = value
            else:
                self.next()

        self.expect(TokenType.CODE_START)
        # استهلك النقطتين (:) لو موجودة
        if self.peek().type == TokenType.COLON:
            self.next()
        self.skip_newlines()

        # استهلك INDENT لو موجود
        if self.peek().type == TokenType.INDENT:
            self.next()

        # اقرأ كل العناصر لحد END
        elements = []
        while True:
            self.skip_newlines()
            t = self.peek()

            if t.type in (TokenType.END, TokenType.EOF):
                break

            if t.type == TokenType.NEW_FILE:
                elements.append(self.parse_new_file())
            elif t.type == TokenType.IMPORT:
                elements.append(self.parse_import())
            elif t.type == TokenType.CREATE:
                elements.append(self.parse_create())
            elif t.type == TokenType.FUNCTION:
                elements.append(self.parse_function())
            elif t.type == TokenType.RETURN:
                elements.append(self.parse_return())
            elif t.type == TokenType.SHOW:
                elements.append(self.parse_show())
            elif t.type == TokenType.CLEAR:
                elements.append(self.parse_clear())
            elif t.type == TokenType.VAR_KW:
                elements.append(self.parse_var_decl())
            elif t.type == TokenType.IF:
                elements.append(self.parse_if())
            elif t.type == TokenType.WHILE:
                elements.append(self.parse_while())
            elif t.type == TokenType.FOR:
                elements.append(self.parse_for())
            elif t.type == TokenType.FOR_INDEX:
                elements.append(self.parse_for_index())
            elif t.type == TokenType.QR_KW:
                elements.append(self.parse_qr())
            elif t.type == TokenType.PDF_KW:
                elements.append(self.parse_pdf())
            elif t.type == TokenType.LOGIN:
                elements.append(self.parse_auth_login())
            elif t.type == TokenType.LOGOUT:
                elements.append(self.parse_auth_logout())
            elif t.type == TokenType.REGISTER:
                elements.append(self.parse_auth_register())
            elif t.type == TokenType.WS_KW:
                elements.append(self.parse_websocket())
            elif t.type == TokenType.MAP_KW:
                elements.append(self.parse_map())
            elif t.type == TokenType.ICON:
                elements.append(self.parse_icon())
            elif t.type == TokenType.PLAY_SOUND:
                elements.append(self.parse_play_sound())
            elif t.type == TokenType.NOTIFY:
                elements.append(self.parse_notify())
            elif t.type == TokenType.CLIPBOARD_COPY:
                elements.append(self.parse_clipboard_copy())
            elif t.type == TokenType.CLIPBOARD_PASTE:
                elements.append(self.parse_clipboard_paste())
            elif t.type == TokenType.DOWNLOAD:
                elements.append(self.parse_download())
            elif t.type == TokenType.ENABLE_DRAG:
                elements.append(self.parse_enable_drag())
            elif t.type == TokenType.ENABLE_RESIZE:
                elements.append(self.parse_enable_resize())
            elif t.type == TokenType.SECURE_LOGIN:
                elements.append(self.parse_secure_login())
            elif t.type == TokenType.DARK_MODE:
                elements.append(self.parse_dark_mode())
            elif t.type == TokenType.LANGUAGE:
                elements.append(self.parse_language())
            elif t.type == TokenType.PAY_BUTTON:
                elements.append(self.parse_pay_button())
            elif t.type == TokenType.VIDEO_CALL:
                elements.append(self.parse_video_call())
            elif t.type == TokenType.PUSH_NOTIFY:
                elements.append(self.parse_push_notify())
            elif t.type == TokenType.CODE_EDITOR:
                elements.append(self.parse_code_editor())
            elif t.type == TokenType.TEMPLATE_APPLY:
                elements.append(self.parse_template_apply())
            elif t.type == TokenType.AI_LOCAL:
                elements.append(self.parse_ai_local())
            elif t.type == TokenType.WEB3:
                elements.append(self.parse_web3())
            elif t.type == TokenType.GAME_3D:
                elements.append(self.parse_scene_3d())
            elif t.type == TokenType.AR_VR:
                elements.append(self.parse_ar_scene())
            elif t.type == TokenType.GENERATOR:
                elements.append(self.parse_generator())
            elif t.type == TokenType.MODAL:
                elements.append(self.parse_modal())
            elif t.type == TokenType.TOOLTIP:
                elements.append(self.parse_tooltip())
            elif t.type == TokenType.ACCORDION:
                elements.append(self.parse_accordion())
            elif t.type == TokenType.SIDEBAR:
                elements.append(self.parse_sidebar())
            elif t.type == TokenType.NAVBAR:
                elements.append(self.parse_navbar())
            elif t.type == TokenType.CLASS_KW:
                elements.append(self.parse_class())
            elif t.type == TokenType.ASYNC_KW:
                elements.append(self.parse_async())
            elif t.type == TokenType.MATCH_KW:
                elements.append(self.parse_match())
            elif t.type == TokenType.TRY:
                elements.append(self.parse_try())
            elif t.type == TokenType.THROW_KW:
                elements.append(self.parse_throw())
            elif t.type == TokenType.CONST_KW:
                elements.append(self.parse_const())
            elif t.type in (TokenType.IDENTIFIER, TokenType.FILE_NAME,
                            TokenType.IDENTIFIER_PROP, TokenType.SELF):
                self._parse_identifier_statement(elements)
            elif t.type == TokenType.DEDENT:
                self.next()
            else:
                self.next()

        program.elements = elements
        return program

    def read_value(self):
        """يقرأ قيمة عادية"""
        while self.peek().type == TokenType.NEWLINE:
            self.next()
        t = self.peek()
        if t.type == TokenType.STRING:
            return self.next().value
        parts = []
        while self.peek().type not in (TokenType.NEWLINE, TokenType.EOF):
            parts.append(str(self.next().value))
        if not parts:
            return ''
        return ' '.join(parts) if len(parts) > 1 else parts[0]

    def read_name_value(self):
        """يقرأ اسم/مسار — بيدمج بدون مسافات"""
        while self.peek().type == TokenType.NEWLINE:
            self.next()
        t = self.peek()
        if t.type == TokenType.STRING:
            return str(self.next().value)
        parts = []
        while self.peek().type not in (TokenType.NEWLINE, TokenType.EOF):
            parts.append(str(self.next().value))
        return ''.join(parts)

    def parse_block(self):
        """يقرأ بلوك — بين INDENT و DEDENT"""
        elements = []

        # لو بدأ بـ INDENT، خده
        has_indent = False
        if self.peek().type == TokenType.INDENT:
            self.next()  # INDENT
            has_indent = True

        while True:
            self.skip_newlines()

            t = self.peek()

            # نهاية البلوك: DEDENT أو END أو EOF أو ELSE
            if t.type in (TokenType.DEDENT, TokenType.END, TokenType.EOF,
                          TokenType.ELSE):
                break

            # لو مفيش indent، اقف عند CREATE/NEW_FILE الجديدة
            # (عشان ما نتعداش حدود البلوك)
            if not has_indent and t.type in (TokenType.NEW_FILE,
                                                TokenType.CREATE):
                break

            # لو فيه indent، استمر
            if t.type == TokenType.NEW_FILE:
                elements.append(self.parse_new_file())
            elif t.type == TokenType.CREATE:
                elements.append(self.parse_create())
            elif t.type == TokenType.SHOW:
                elements.append(self.parse_show())
            elif t.type == TokenType.CLEAR:
                elements.append(self.parse_clear())
            elif t.type == TokenType.VAR_KW:
                elements.append(self.parse_var_decl())
            elif t.type == TokenType.IF:
                elements.append(self.parse_if())
            elif t.type == TokenType.WHILE:
                elements.append(self.parse_while())
            elif t.type == TokenType.FOR:
                elements.append(self.parse_for())
            elif t.type == TokenType.FOR_INDEX:
                elements.append(self.parse_for_index())
            elif t.type == TokenType.TRY:
                elements.append(self.parse_try())
            elif t.type == TokenType.AWAIT:
                elements.append(self.parse_await())
            elif t.type == TokenType.IMPORT:
                elements.append(self.parse_import())
            elif t.type == TokenType.INPUT_ASK:
                elements.append(self.parse_input_ask())
            elif t.type == TokenType.GRID:
                elements.append(self.parse_grid())
            elif t.type == TokenType.TABLE:
                elements.append(self.parse_table())
            elif t.type == TokenType.CHART:
                elements.append(self.parse_chart())
            elif t.type == TokenType.FORM:
                elements.append(self.parse_form())
            elif t.type == TokenType.TABS:
                elements.append(self.parse_tabs())
            elif t.type == TokenType.DB_KW:
                elements.append(self.parse_db_create())
            # elif t.type == TokenType.TABLE_KW:  # disabled: TokenType مش موجود
            #     elements.append(self.parse_db_table())
            elif t.type == TokenType.INSERT_KW:
                elements.append(self.parse_db_insert())
            elif t.type == TokenType.SELECT_KW:
                elements.append(self.parse_db_select())
            elif t.type == TokenType.EVERY:
                elements.append(self.parse_timer())
            elif t.type == TokenType.ANIMATE:
                elements.append(self.parse_animate())
            elif t.type == TokenType.CREATE_ELEMENT:
                elements.append(self.parse_create_element())
            elif t.type == TokenType.REMOVE_ELEMENT:
                elements.append(self.parse_remove_element())
            elif t.type == TokenType.HTTP_GET:
                elements.append(self.parse_http_get())
            elif t.type == TokenType.HTTP_POST:
                elements.append(self.parse_http_post())
            elif t.type == TokenType.ADD_ITEM:
                elements.append(self.parse_add_item())
            elif t.type == TokenType.REMOVE_ITEM:
                elements.append(self.parse_remove_item())
            elif t.type == TokenType.AI_ASK:
                elements.append(self.parse_ai_ask())
            elif t.type == TokenType.BREAK:
                self.next()
                elements.append(ast.Break())
            elif t.type == TokenType.CONTINUE:
                self.next()
                elements.append(ast.Continue())
            elif t.type == TokenType.FUNCTION:
                elements.append(self.parse_function())
            elif t.type == TokenType.RETURN:
                elements.append(self.parse_return())
            elif t.type in (TokenType.COPY, TokenType.MOVE,
                            TokenType.DELETE, TokenType.READ,
                            TokenType.SAVE, TokenType.NEW_FOLDER,
                            TokenType.OPEN):
                elements.append(self.parse_file_op())
            elif t.type in (TokenType.IDENTIFIER, TokenType.FILE_NAME,
                            TokenType.IDENTIFIER_PROP, TokenType.SELF):
                self._parse_identifier_statement(elements)
            else:
                self.next()

        # استهلك DEDENT لو موجود
        if self.peek().type == TokenType.DEDENT:
            self.next()

        return elements


    def _parse_identifier_statement(self, target_list):
        """يقرأ statement بسيط يبدأ بـ IDENTIFIER أو SELF
        
        target_list: القائمة اللي نضيف فيها النتيجة
        """
        nxt = self.peek(1)
        nxt2 = self.peek(2)
        
        if nxt.type in (TokenType.EQUALS, TokenType.PLUS_EQ, TokenType.MINUS_EQ):
            target_list.append(self.parse_assign())
        elif nxt.type == TokenType.LPAREN:
            name = str(self.next().value)
            target_list.append(self.parse_call(name))
        elif nxt.type == TokenType.LBRACKET:
            result = self.parse_index_or_set()
            if result is not None:
                target_list.append(result)
        elif nxt.type == TokenType.DOT:
            # هذا.اسم = قيمة أو هذا.اسم
            obj_tok = self.next()  # IDENTIFIER أو SELF
            if obj_tok.type == TokenType.SELF:
                obj = ast.VarRef('هذا')
            else:
                obj = ast.VarRef(str(obj_tok.value))
            
            while self.peek().type == TokenType.DOT:
                self.next()
                attr = str(self.next().value)
                
                if self.peek().type == TokenType.EQUALS:
                    self.next()
                    value = self.parse_expression()
                    target_list.append(ast.MemberSet(obj, attr, value))
                    return
                elif self.peek().type == TokenType.LPAREN:
                    # method call
                    self.next()
                    args = []
                    while self.peek().type != TokenType.RPAREN:
                        self.skip_newlines()
                        if self.peek().type == TokenType.RPAREN:
                            break
                        args.append(self.parse_term())
                        if self.peek().type == TokenType.COMMA:
                            self.next()
                        else:
                            break
                    if self.peek().type == TokenType.RPAREN:
                        self.next()
                    target_list.append(ast.MethodCall(obj, attr, args))
                    return
                else:
                    obj = ast.MemberAccess(obj, attr)
            
            # expression وحيد
            target_list.append(obj)
        else:
            self.next()

    def parse_assign(self):
        """س = 5 أو س += 1"""
        name = str(self.next().value)
        op_tok = self.next()

        if op_tok.type == TokenType.EQUALS:
            value = self.parse_expression()
            return ast.Assign(name, value)
        elif op_tok.type == TokenType.PLUS_EQ:
            value = self.parse_expression()
            return ast.CompoundAssign(name, '+', value)
        elif op_tok.type == TokenType.MINUS_EQ:
            value = self.parse_expression()
            return ast.CompoundAssign(name, '-', value)
        else:
            raise SyntaxError(f"عامل غير متوقع: {op_tok.value}")

    def parse_index_or_set(self):
        """يقرأ: قاموس[مفتاح] = قيمة أو متجاهل لو expression"""
        name = str(self.next().value)
        target = ast.VarRef(name)

        # اقرأ كل الفهارس [..][..]
        while self.peek().type == TokenType.LBRACKET:
            self.next()
            key = self.parse_term()
            if self.peek().type == TokenType.RBRACKET:
                self.next()
            target = ast.IndexAccess(target, key)

        # لو بعده = → DictSet
        if self.peek().type == TokenType.EQUALS:
            self.next()
            value = self.parse_expression()
            if isinstance(target, ast.IndexAccess):
                return ast.DictSet(target.target, target.index, value)
            raise SyntaxError("هدف غير صالح للإسناد")

        # expression وحيد — نتجاهله
        return None

    def parse_function(self):
        """دالة اسم(معاملات): جسم"""
        self.next()  # FUNCTION
        name = str(self.next().value)

        # اقرأ المعاملات
        params = []
        if self.peek().type == TokenType.LPAREN:
            self.next()  # (
            while self.peek().type != TokenType.RPAREN:
                self.skip_newlines()
                if self.peek().type == TokenType.RPAREN:
                    break
                if self.peek().type in (TokenType.IDENTIFIER, TokenType.FILE_NAME):
                    params.append(str(self.next().value))
                else:
                    self.next()
                if self.peek().type == TokenType.COMMA:
                    self.next()
            if self.peek().type == TokenType.RPAREN:
                self.next()  # )

        # :
        if self.peek().type == TokenType.COLON:
            self.next()

        self.skip_newlines()

        # استهلك INDENT
        if self.peek().type == TokenType.INDENT:
            self.next()

        # جسم الدالة
        body = []
        while True:
            self.skip_newlines()
            t = self.peek()

            if t.type in (TokenType.DEDENT, TokenType.EOF, TokenType.END):
                break

            if t.type == TokenType.RETURN:
                body.append(self.parse_return())
            elif t.type == TokenType.FUNCTION:
                body.append(self.parse_function())
            elif t.type == TokenType.VAR_KW:
                body.append(self.parse_var_decl())
            elif t.type == TokenType.SHOW:
                body.append(self.parse_show())
            elif t.type == TokenType.IF:
                body.append(self.parse_if())
            elif t.type == TokenType.WHILE:
                body.append(self.parse_while())
            elif t.type == TokenType.FOR:
                body.append(self.parse_for())
            elif t.type == TokenType.SUPER:
                # أساس(...) كـ statement
                result = self.parse_term()
                if result is not None:
                    body.append(result)
            elif t.type == TokenType.LOCAL:
                body.append(self.parse_local_decl())
            elif t.type == TokenType.GLOBAL:
                body.append(self.parse_global_decl())
            elif t.type == TokenType.NONLOCAL:
                body.append(self.parse_nonlocal_decl())
            elif t.type in (TokenType.IDENTIFIER, TokenType.FILE_NAME,
                            TokenType.IDENTIFIER_PROP, TokenType.SELF):
                self._parse_identifier_statement(body)
            else:
                self.next()

        # استهلك DEDENT واحد فقط (الأب مسؤول عن الباقي)
        if self.peek().type == TokenType.DEDENT:
            self.next()

        return ast.FunctionDef(name=name, params=params, body=body)

    def parse_return(self):
        """ارجع قيمة"""
        self.next()  # RETURN
        if self.peek().type in (TokenType.NEWLINE, TokenType.EOF,
                                 TokenType.DEDENT):
            return ast.Return(None)
        value = self.parse_expression()
        return ast.Return(value)


    def parse_file_op(self):
        """انسخ/انقل/احذف/اقرأ/اكتب/انشئ_مجلد/نفّذ"""
        op_token = self.next()
        op_map = {
            TokenType.COPY: 'copy',
            TokenType.MOVE: 'move',
            TokenType.DELETE: 'delete',
            TokenType.READ: 'read',
            TokenType.SAVE: 'write',
            TokenType.NEW_FOLDER: 'mkdir',
            TokenType.OPEN: 'exec',
        }
        op = op_map.get(op_token.type, 'copy')

        # اقرأ المصدر
        source = ''
        if self.peek().type == TokenType.STRING:
            source = str(self.next().value)
        elif self.peek().type in (TokenType.IDENTIFIER, TokenType.FILE_NAME):
            source = str(self.next().value)
        else:
            # لو مش معروف، تجاهل
            return ast.FileOp(op='noop')

        # الهدف (إلى / فيه / في / بمحتوى)
        target = ''
        content = ''

        # شوف الكلمة اللي بعدها
        if self.peek().type in (TokenType.IN, TokenType.CONTENT):
            marker = str(self.next().value)
            if self.peek().type == TokenType.COLON:
                self.next()
            if self.peek().type == TokenType.STRING:
                val = str(self.next().value)
            elif self.peek().type in (TokenType.IDENTIFIER, TokenType.FILE_NAME):
                val = str(self.next().value)
            else:
                val = ''
            if marker in ('بمحتوى', 'فيه'):
                content = val
            else:
                target = val

        return ast.FileOp(op=op, source=source, target=target, content=content)

    def parse_var_decl_from_call(self):
        """متغير س = اقرأ "file.txt" """
        self.next()  # VAR_KW
        name = str(self.next().value)
        if self.peek().type == TokenType.EQUALS:
            self.next()
        # اقرأ الاستدعاء
        return name, self.parse_expression()


    def parse_add_item(self):
        """أضف(قائمة, عنصر)"""
        self.next()  # ADD_ITEM
        if self.peek().type == TokenType.LPAREN:
            self.next()
        target = self.parse_term()
        if self.peek().type == TokenType.COMMA:
            self.next()
        item = self.parse_term()
        if self.peek().type == TokenType.RPAREN:
            self.next()
        return ast.ArrayAdd(target, item)

    def parse_remove_item(self):
        """احذف_عنصر(قائمة, فهرس)"""
        self.next()  # REMOVE_ITEM
        if self.peek().type == TokenType.LPAREN:
            self.next()
        target = self.parse_term()
        if self.peek().type == TokenType.COMMA:
            self.next()
        index = self.parse_term()
        if self.peek().type == TokenType.RPAREN:
            self.next()
        return ast.ArrayRemove(target, index)

    def parse_ai_ask(self):
        """اسأل الذكاء_الاصطناعي "..." """
        self.next()  # AI_ASK
        # اقرأ الـ prompt
        if self.peek().type == TokenType.STRING:
            prompt = str(self.next().value)
        else:
            prompt = self.read_value()
        return ast.AiAsk(prompt, "")


    def parse_db_create(self):
        """قاعدة_بيانات "name.db" """
        self.next()
        name = 'byan_data.db'
        if self.peek().type == TokenType.STRING:
            name = str(self.next().value)
        return ast.DbCreate(name)

    def parse_db_table(self):
        """جدول "users" """
        self.next()
        name = ''
        if self.peek().type == TokenType.STRING:
            name = str(self.next().value)
        columns = []
        # اقرأ الأعمدة
        self.skip_newlines()
        if self.peek().type == TokenType.COLON:
            self.next()
        self.skip_newlines()
        if self.peek().type == TokenType.INDENT:
            self.next()
        while True:
            self.skip_newlines()
            t = self.peek()
            if t.type in (TokenType.DEDENT, TokenType.EOF, TokenType.END):
                break
            if t.type in (TokenType.IDENTIFIER, TokenType.FILE_NAME):
                columns.append(str(self.next().value))
                if self.peek().type == TokenType.COLON:
                    self.next()
                    # اقرأ النوع
                    while self.peek().type not in (TokenType.NEWLINE,
                                                     TokenType.DEDENT, TokenType.EOF):
                        self.next()
            else:
                self.next()
        while self.peek().type == TokenType.DEDENT:
            self.next()
        return ast.DbTable(name, columns)

    def parse_db_insert(self):
        """أضف_سجل "users" فيه {name: "احمد"}"""
        self.next()
        table = ''
        if self.peek().type == TokenType.STRING:
            table = str(self.next().value)
        values = {}
        # تجاهل الكلمات لحد {
        while self.peek().type not in (TokenType.LBRACE, TokenType.NEWLINE,
                                         TokenType.EOF):
            self.next()
        if self.peek().type == TokenType.LBRACE:
            self.next()
            while self.peek().type != TokenType.RBRACE:
                if self.peek().type in (TokenType.IDENTIFIER, TokenType.FILE_NAME):
                    key = str(self.next().value)
                    if self.peek().type == TokenType.COLON:
                        self.next()
                    if self.peek().type == TokenType.STRING:
                        val = str(self.next().value)
                    elif self.peek().type == TokenType.NUMBER:
                        val = self.next().value
                    else:
                        val = str(self.next().value)
                    values[key] = val
                elif self.peek().type == TokenType.COMMA:
                    self.next()
                else:
                    self.next()
            if self.peek().type == TokenType.RBRACE:
                self.next()
        return ast.DbInsert(table, values)

    def parse_db_select(self):
        """اقرأ_سجلات "users" في: "#out" """
        self.next()
        table = ''
        if self.peek().type == TokenType.STRING:
            table = str(self.next().value)
        target = ''
        if self.peek().type == TokenType.IN:
            self.next()
        if self.peek().type == TokenType.COLON:
            self.next()
        if self.peek().type == TokenType.STRING:
            target = str(self.next().value)
        return ast.DbSelect(table, target)

    def parse_timer(self):
        """كل 2 ثانية: ..."""
        self.next()  # كل
        seconds = 1.0
        if self.peek().type == TokenType.NUMBER:
            seconds = float(self.next().value)
        # تخطى "ثانية"
        while self.peek().type not in (TokenType.COLON, TokenType.NEWLINE,
                                         TokenType.EOF):
            self.next()
        if self.peek().type == TokenType.COLON:
            self.next()
        self.skip_newlines()
        if self.peek().type == TokenType.INDENT:
            self.next()
        body = []
        while True:
            self.skip_newlines()
            t = self.peek()
            if t.type in (TokenType.DEDENT, TokenType.EOF, TokenType.END):
                break
            if t.type == TokenType.SHOW:
                body.append(self.parse_show())
            elif t.type == TokenType.VAR_KW:
                body.append(self.parse_var_decl())
            elif t.type in (TokenType.IDENTIFIER, TokenType.FILE_NAME,
                            TokenType.IDENTIFIER_PROP, TokenType.SELF):
                self._parse_identifier_statement(body)
            else:
                self.next()
        while self.peek().type == TokenType.DEDENT:
            self.next()
        return ast.Timer(seconds, body)

    def parse_animate(self):
        """حرّك "#box" إلى (100, 200) في: 2 ثانية"""
        self.next()
        selector = ''
        if self.peek().type == TokenType.STRING:
            selector = str(self.next().value)
        # تجاهل لحد (
        while self.peek().type not in (TokenType.LPAREN, TokenType.NEWLINE,
                                         TokenType.EOF):
            self.next()
        x, y = 0, 0
        if self.peek().type == TokenType.LPAREN:
            self.next()
            if self.peek().type == TokenType.NUMBER:
                x = int(self.next().value)
            if self.peek().type == TokenType.COMMA:
                self.next()
            if self.peek().type == TokenType.NUMBER:
                y = int(self.next().value)
            if self.peek().type == TokenType.RPAREN:
                self.next()
        duration = 1.0
        # تجاهل لحد رقم
        while self.peek().type not in (TokenType.NUMBER, TokenType.NEWLINE,
                                         TokenType.EOF):
            self.next()
        if self.peek().type == TokenType.NUMBER:
            duration = float(self.next().value)
        return ast.Animate(selector, x, y, duration)

    def parse_create_element(self):
        """ضيف_عنصر "div" في "#container" """
        self.next()
        tag = 'div'
        if self.peek().type == TokenType.STRING:
            tag = str(self.next().value)
        target = 'body'
        # تجاهل لحد STRING التاني
        while self.peek().type not in (TokenType.STRING, TokenType.NEWLINE,
                                         TokenType.EOF):
            self.next()
        if self.peek().type == TokenType.STRING:
            target = str(self.next().value)
        return ast.CreateElement(tag, target, '', '')

    def parse_remove_element(self):
        """امسح_عنصر "#id" """
        self.next()
        selector = ''
        if self.peek().type == TokenType.STRING:
            selector = str(self.next().value)
        return ast.RemoveElement(selector)

    def parse_http_get(self):
        """اتصل "url" في: "#out" """
        self.next()
        url = ''
        if self.peek().type == TokenType.STRING:
            url = str(self.next().value)
        target = ''
        # تجاهل لحد "في"
        while self.peek().type not in (TokenType.IN, TokenType.NEWLINE,
                                         TokenType.EOF):
            self.next()
        if self.peek().type == TokenType.IN:
            self.next()
        if self.peek().type == TokenType.COLON:
            self.next()
        if self.peek().type == TokenType.STRING:
            target = str(self.next().value)
        return ast.HttpGet(url, target)

    def parse_http_post(self):
        """ارسل "url" ببيانات {...}"""
        self.next()
        url = ''
        if self.peek().type == TokenType.STRING:
            url = str(self.next().value)
        # تجاهل الباقي
        while self.peek().type not in (TokenType.NEWLINE, TokenType.DEDENT,
                                         TokenType.EOF):
            self.next()
        return ast.HttpPost(url, {})


    def parse_try(self):
        """حاول: ... لو_فشل: ... أخيراً: ..."""
        self.next()  # TRY
        if self.peek().type == TokenType.COLON:
            self.next()
        self.skip_newlines()
        if self.peek().type == TokenType.INDENT:
            self.next()

        # ===== body =====
        body = []
        while True:
            self.skip_newlines()
            t = self.peek()
            if t.type in (TokenType.DEDENT, TokenType.EOF, TokenType.END,
                          TokenType.CATCH, TokenType.FINALLY_KW):
                break
            if t.type == TokenType.SHOW:
                body.append(self.parse_show())
            elif t.type == TokenType.VAR_KW:
                body.append(self.parse_var_decl())
            elif t.type == TokenType.RETURN:
                body.append(self.parse_return())
            elif t.type == TokenType.IF:
                body.append(self.parse_if())
            elif t.type == TokenType.WHILE:
                body.append(self.parse_while())
            elif t.type == TokenType.FOR:
                body.append(self.parse_for())
            elif t.type == TokenType.THROW_KW:
                body.append(self.parse_throw())
            elif t.type == TokenType.TRY:
                body.append(self.parse_try())
            elif t.type in (TokenType.READ, TokenType.SAVE, TokenType.DELETE):
                body.append(self.parse_file_op())
            elif t.type in (TokenType.IDENTIFIER, TokenType.FILE_NAME,
                            TokenType.IDENTIFIER_PROP, TokenType.SELF):
                self._parse_identifier_statement(body)
            else:
                self.next()

        # استهلك DEDENT واحد
        if self.peek().type == TokenType.DEDENT:
            self.next()

        # ===== catch (لو_فشل) =====
        catch_body = []
        self.skip_newlines()
        if self.peek().type == TokenType.CATCH:
            self.next()
            if self.peek().type == TokenType.COLON:
                self.next()
            self.skip_newlines()
            if self.peek().type == TokenType.INDENT:
                self.next()

            while True:
                self.skip_newlines()
                t = self.peek()
                if t.type in (TokenType.DEDENT, TokenType.EOF, TokenType.END,
                              TokenType.FINALLY_KW):
                    break
                if t.type == TokenType.SHOW:
                    catch_body.append(self.parse_show())
                elif t.type == TokenType.VAR_KW:
                    catch_body.append(self.parse_var_decl())
                elif t.type == TokenType.RETURN:
                    catch_body.append(self.parse_return())
                elif t.type == TokenType.IF:
                    catch_body.append(self.parse_if())
                elif t.type == TokenType.WHILE:
                    catch_body.append(self.parse_while())
                elif t.type == TokenType.FOR:
                    catch_body.append(self.parse_for())
                elif t.type == TokenType.THROW_KW:
                    catch_body.append(self.parse_throw())
                elif t.type in (TokenType.IDENTIFIER, TokenType.FILE_NAME,
                                TokenType.IDENTIFIER_PROP, TokenType.SELF):
                    self._parse_identifier_statement(catch_body)
                else:
                    self.next()

            if self.peek().type == TokenType.DEDENT:
                self.next()

        # ===== finally (أخيراً) =====
        finally_body = []
        self.skip_newlines()
        if self.peek().type == TokenType.FINALLY_KW:
            self.next()
            if self.peek().type == TokenType.COLON:
                self.next()
            self.skip_newlines()
            if self.peek().type == TokenType.INDENT:
                self.next()

            while True:
                self.skip_newlines()
                t = self.peek()
                if t.type in (TokenType.DEDENT, TokenType.EOF, TokenType.END):
                    break
                if t.type == TokenType.SHOW:
                    finally_body.append(self.parse_show())
                elif t.type == TokenType.VAR_KW:
                    finally_body.append(self.parse_var_decl())
                elif t.type == TokenType.RETURN:
                    finally_body.append(self.parse_return())
                elif t.type == TokenType.IF:
                    finally_body.append(self.parse_if())
                elif t.type == TokenType.WHILE:
                    finally_body.append(self.parse_while())
                elif t.type == TokenType.FOR:
                    finally_body.append(self.parse_for())
                elif t.type in (TokenType.IDENTIFIER, TokenType.FILE_NAME,
                                TokenType.IDENTIFIER_PROP, TokenType.SELF):
                    self._parse_identifier_statement(finally_body)
                else:
                    self.next()

            if self.peek().type == TokenType.DEDENT:
                self.next()

        return ast.TryCatchFinally(body, catch_body, finally_body)


    def parse_await(self):
        """انتظر: ... (ينفذ بالترتيب)"""
        self.next()
        if self.peek().type == TokenType.COLON:
            self.next()
        self.skip_newlines()
        if self.peek().type == TokenType.INDENT:
            self.next()

        body = []
        while True:
            self.skip_newlines()
            t = self.peek()
            # نوقف عند DEDENT أو CREATE أو NEW_FILE (عشان مانتعداش حدود الـ action)
            if t.type in (TokenType.DEDENT, TokenType.EOF, TokenType.END,
                          TokenType.CREATE, TokenType.NEW_FILE):
                break
            if t.type == TokenType.SHOW:
                body.append(self.parse_show())
            elif t.type == TokenType.VAR_KW:
                body.append(self.parse_var_decl())
            elif t.type == TokenType.INSERT_KW:
                body.append(self.parse_db_insert())
            elif t.type == TokenType.SELECT_KW:
                body.append(self.parse_db_select())
            elif t.type == TokenType.HTTP_GET:
                body.append(self.parse_http_get())
            elif t.type == TokenType.IF:
                body.append(self.parse_if())
            elif t.type in (TokenType.IDENTIFIER, TokenType.FILE_NAME,
                            TokenType.IDENTIFIER_PROP, TokenType.SELF):
                self._parse_identifier_statement(body)
            else:
                self.next()

        while self.peek().type == TokenType.DEDENT:
            self.next()
        return ast.Await(body)


    def parse_import(self):
        """استورد "file.byan" أو استورد رياضيات"""
        self.next()  # IMPORT
        path = ''
        if self.peek().type == TokenType.STRING:
            path = str(self.next().value)
        elif self.peek().type in (TokenType.IDENTIFIER, TokenType.FILE_NAME):
            path = str(self.next().value)
        return ast.Import(path)


    def parse_input_ask(self):
        """اسأل_المستخدم "..." """
        self.next()
        prompt = ''
        if self.peek().type == TokenType.STRING:
            prompt = str(self.next().value)
        return ast.InputAsk(prompt)


    def parse_icon(self):
        """أيقونة"""
        self.next()  # ICON
        if self.peek().type == TokenType.COLON:
            self.next()
        self.skip_newlines()
        if self.peek().type == TokenType.INDENT:
            self.next()
        props = self.parse_props()
        if self.peek().type == TokenType.DEDENT:
            self.next()
        return ast.CreateIcon(props)


    def parse_form_body(self):
        """يقرأ الحقول و actions من نموذج موجود في props"""
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
                    if tt.type == TokenType.MINUS:
                        self.next()
                        tt = self.peek()
                    if tt.type in (TokenType.IDENTIFIER, TokenType.FILE_NAME,
                                    TokenType.NAME, TokenType.TEXT):
                        fname = str(self.next().value)
                        ftype = 'text'
                        if self.peek().type == TokenType.COLON:
                            self.next()
                            type_tok = self.peek()
                            if type_tok.value:
                                ftype = str(type_tok.value)
                                self.next()
                        fields.append({'name': fname, 'type': ftype})
                    else:
                        self.next()
                if self.peek().type == TokenType.DEDENT:
                    self.next()
            else:
                self.next()

        if self.peek().type == TokenType.DEDENT:
            self.next()

        return fields, actions




    def parse_table_body(self):
        """يقرأ الجداول"""
        headers = []
        rows = []

        while True:
            self.skip_newlines()
            t = self.peek()
            if t.type in (TokenType.DEDENT, TokenType.EOF, TokenType.END):
                break

            # الأعمدة
            if t.type == TokenType.COLUMNS:
                self.next()
                if self.peek().type == TokenType.COLON:
                    self.next()
                self.skip_newlines()
                if self.peek().type == TokenType.INDENT:
                    self.next()
                while True:
                    self.skip_newlines()
                    tt = self.peek()
                    if tt.type in (TokenType.DEDENT, TokenType.EOF, TokenType.END,
                                    TokenType.DATA_ROWS):
                        break
                    if tt.type == TokenType.MINUS:
                        self.next()
                        tt = self.peek()
                    if tt.value:
                        headers.append(str(self.next().value))
                    else:
                        self.next()
                if self.peek().type == TokenType.DEDENT:
                    self.next()

            # البيانات
            elif t.type == TokenType.DATA_ROWS:
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
                    if tt.type == TokenType.MINUS:
                        self.next()
                        tt = self.peek()
                    # اقرأ سطر كامل كنص
                    row_parts = []
                    while self.peek().type not in (TokenType.NEWLINE,
                                                    TokenType.DEDENT, TokenType.EOF):
                        tv = self.peek()
                        if tv.value is not None:
                            row_parts.append(str(tv.value))
                        self.next()
                    if row_parts:
                        rows.append(row_parts)
                if self.peek().type == TokenType.DEDENT:
                    self.next()
            else:
                self.next()

        if self.peek().type == TokenType.DEDENT:
            self.next()

        return headers, rows

    def parse_tabs_body(self):
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


    def parse_grid_body(self):
        """يقرأ عناصر الشبكة"""
        items = []

        while True:
            self.skip_newlines()
            t = self.peek()
            if t.type in (TokenType.DEDENT, TokenType.EOF, TokenType.END):
                break

            # العناصر
            if t.type == TokenType.ELEMENTS:
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
                    # أيقونة
                    if tt.type == TokenType.ICON:
                        self.next()
                        if self.peek().type == TokenType.COLON:
                            self.next()
                        icon_type = ''
                        if self.peek().value:
                            icon_type = str(self.next().value)
                        items.append({'type': 'icon', 'value': icon_type})
                    # نص
                    elif tt.type == TokenType.STRING:
                        text = str(self.next().value)
                        items.append({'type': 'text', 'value': text})
                    elif tt.type in (TokenType.IDENTIFIER, TokenType.FILE_NAME):
                        text = str(self.next().value)
                        items.append({'type': 'text', 'value': text})
                    else:
                        self.next()
                if self.peek().type == TokenType.DEDENT:
                    self.next()
            else:
                self.next()

        if self.peek().type == TokenType.DEDENT:
            self.next()

        return items

    def parse_grid(self):
        """شبكة"""
        self.next()
        if self.peek().type == TokenType.COLON:
            self.next()
        self.skip_newlines()
        if self.peek().type == TokenType.INDENT:
            self.next()
        props = self.parse_props()
        columns = 2
        if 'الأعمدة' in props:
            try:
                columns = int(props['الأعمدة'])
            except:
                pass
        while self.peek().type == TokenType.DEDENT:
            self.next()
        return ast.CreateGrid(props, [], columns)

    def parse_table(self):
        """جدول"""
        self.next()
        if self.peek().type == TokenType.COLON:
            self.next()
        self.skip_newlines()
        if self.peek().type == TokenType.INDENT:
            self.next()
        props = self.parse_props()
        headers = []
        # اقرأ الأعمدة لو موجودة
        if 'الأعمدة' in props:
            h = props['الأعمدة']
            if isinstance(h, list):
                headers = [str(x) for x in h]
        while self.peek().type == TokenType.DEDENT:
            self.next()
        return ast.CreateTable(props, headers, '')

    def parse_chart(self):
        """رسم_بياني:"""
        if self.peek().type == TokenType.CREATE:
            self.next()
        if self.peek().type == TokenType.CHART:
            self.next()
        if self.peek().type == TokenType.COLON:
            self.next()
        self.skip_newlines()
        if self.peek().type == TokenType.INDENT:
            self.next()

        props = {}
        while True:
            self.skip_newlines()
            t = self.peek()
            if t.type in (TokenType.DEDENT, TokenType.EOF, TokenType.END,
                          TokenType.CREATE, TokenType.ON_CLICK):
                break
            if t.type in (TokenType.TITLE_PROP, TokenType.IDENTIFIER,
                          TokenType.IDENTIFIER_PROP,
                          TokenType.TEXT):
                key = str(self.next().value)
                if self.peek().type == TokenType.COLON:
                    self.next()
                if self.peek().type == TokenType.STRING:
                    val = str(self.next().value)
                elif self.peek().type == TokenType.NUMBER:
                    val = self.next().value
                else:
                    val = str(self.next().value)
                props[key] = val
            else:
                self.next()

        if self.peek().type == TokenType.DEDENT:
            self.next()

        chart_type = str(props.get('النوع', 'bar'))
        return ast.CreateChart(props, chart_type, [])



    def parse_play_sound(self):
        """شغل صوت "url" """
        self.next()
        url = ''
        while self.peek().type not in (TokenType.STRING, TokenType.NEWLINE,
                                         TokenType.DEDENT, TokenType.EOF):
            self.next()
        if self.peek().type == TokenType.STRING:
            url = str(self.next().value)
        return ast.PlaySound(url)

    def parse_notify(self):
        """أظهر إشعار "نص" """
        self.next()
        title = ''
        body = ''
        while self.peek().type not in (TokenType.STRING, TokenType.NEWLINE,
                                         TokenType.DEDENT, TokenType.EOF):
            self.next()
        if self.peek().type == TokenType.STRING:
            title = str(self.next().value)
        # لو فيه نص تاني
        while self.peek().type not in (TokenType.STRING, TokenType.NEWLINE,
                                         TokenType.DEDENT, TokenType.EOF):
            self.next()
        if self.peek().type == TokenType.STRING:
            body = str(self.next().value)
        return ast.Notify(title, body)

    def parse_clipboard_copy(self):
        """انسخ للحافظة "نص" """
        self.next()
        text = ''
        while self.peek().type not in (TokenType.STRING, TokenType.NEWLINE,
                                         TokenType.DEDENT, TokenType.EOF):
            self.next()
        if self.peek().type == TokenType.STRING:
            text = str(self.next().value)
        return ast.ClipboardCopy(text)

    def parse_clipboard_paste(self):
        """الصق"""
        self.next()
        return ast.ClipboardPaste('')

    def parse_download(self):
        """حمل "url" """
        self.next()
        url = ''
        filename = ''
        while self.peek().type not in (TokenType.STRING, TokenType.NEWLINE,
                                         TokenType.DEDENT, TokenType.EOF):
            self.next()
        if self.peek().type == TokenType.STRING:
            url = str(self.next().value)
        # شوف لو فيه اسم ملف
        while self.peek().type not in (TokenType.STRING, TokenType.NEWLINE,
                                         TokenType.DEDENT, TokenType.EOF):
            self.next()
        if self.peek().type == TokenType.STRING:
            filename = str(self.next().value)
        return ast.Download(url, filename)


    def parse_enable_drag(self):
        """فعّل_سحب "#id" """
        self.next()
        selector = ''
        while self.peek().type not in (TokenType.STRING, TokenType.NEWLINE,
                                         TokenType.DEDENT, TokenType.EOF):
            self.next()
        if self.peek().type == TokenType.STRING:
            selector = str(self.next().value)
        return ast.EnableDrag(selector)

    def parse_enable_resize(self):
        """فعّل_تحجيم "#id" """
        self.next()
        selector = ''
        while self.peek().type not in (TokenType.STRING, TokenType.NEWLINE,
                                         TokenType.DEDENT, TokenType.EOF):
            self.next()
        if self.peek().type == TokenType.STRING:
            selector = str(self.next().value)
        return ast.EnableResize(selector)

    def parse_dark_mode(self):
        """وضع_ليلي: تلقائي"""
        self.next()
        if self.peek().type == TokenType.COLON:
            self.next()
        mode = 'auto'
        if self.peek().value:
            mode = str(self.next().value)
        return ast.DarkMode(mode)

    def parse_language(self):
        """اللغة: عربي"""
        self.next()
        if self.peek().type == TokenType.COLON:
            self.next()
        lang = 'ar'
        if self.peek().value:
            lang = str(self.next().value)
        return ast.Language(lang)

    def parse_secure_login(self):
        """تسجيل_دخول_آمن "user" "pass" """
        self.next()
        username = ''
        password = ''
        while self.peek().type not in (TokenType.STRING, TokenType.NEWLINE,
                                         TokenType.DEDENT, TokenType.EOF):
            self.next()
        if self.peek().type == TokenType.STRING:
            username = str(self.next().value)
        while self.peek().type not in (TokenType.STRING, TokenType.NEWLINE,
                                         TokenType.DEDENT, TokenType.EOF):
            self.next()
        if self.peek().type == TokenType.STRING:
            password = str(self.next().value)
        return ast.SecureLogin(username, password)


    def parse_pay_button(self):
        """زر دفع"""
        self.next()
        if self.peek().type == TokenType.COLON:
            self.next()
        self.skip_newlines()
        if self.peek().type == TokenType.INDENT:
            self.next()
        props = self.parse_props()
        amount = 100
        currency = 'USD'
        if 'المبلغ' in props:
            try:
                amount = float(props['المبلغ'])
            except:
                pass
        if 'العملة' in props:
            currency = str(props['العملة'])
        # ابحث عن عند_النجاح
        actions = []
        self.skip_newlines()
        if self.peek().type == TokenType.ON_SUBMIT or self.peek().type == TokenType.ON_CLICK:
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
                else:
                    self.next()
            if self.peek().type == TokenType.DEDENT:
                self.next()
        if self.peek().type == TokenType.DEDENT:
            self.next()
        return ast.PayButton(props, amount, currency, actions)

    def parse_video_call(self):
        """اتصال_فيديو "room" """
        self.next()
        room = ''
        while self.peek().type not in (TokenType.STRING, TokenType.NEWLINE,
                                         TokenType.DEDENT, TokenType.EOF):
            self.next()
        if self.peek().type == TokenType.STRING:
            room = str(self.next().value)
        return ast.VideoCall(room)

    def parse_push_notify(self):
        """اطلب إشعارات push"""
        self.next()
        return ast.PushNotify()

    def parse_code_editor(self):
        """محرر كود"""
        self.next()
        if self.peek().type == TokenType.COLON:
            self.next()
        self.skip_newlines()
        if self.peek().type == TokenType.INDENT:
            self.next()
        props = self.parse_props()
        if self.peek().type == TokenType.DEDENT:
            self.next()
        return ast.CodeEditor(props)

    def parse_template_apply(self):
        """طبق_قالب "name" في: "#target" """
        self.next()
        template = ''
        target = ''
        while self.peek().type not in (TokenType.STRING, TokenType.NEWLINE,
                                         TokenType.DEDENT, TokenType.EOF):
            self.next()
        if self.peek().type == TokenType.STRING:
            template = str(self.next().value)
        # ابحث عن target
        while self.peek().type not in (TokenType.STRING, TokenType.NEWLINE,
                                         TokenType.DEDENT, TokenType.EOF):
            self.next()
        if self.peek().type == TokenType.STRING:
            target = str(self.next().value)
        return ast.TemplateApply(template, target)


    def parse_ai_local(self):
        """اسأل_ai_محلي "prompt" في: "#target" """
        self.next()
        prompt = ''
        target = ''
        while self.peek().type not in (TokenType.STRING, TokenType.NEWLINE,
                                         TokenType.DEDENT, TokenType.EOF):
            self.next()
        if self.peek().type == TokenType.STRING:
            prompt = str(self.next().value)
        # target
        while self.peek().type not in (TokenType.STRING, TokenType.NEWLINE,
                                         TokenType.DEDENT, TokenType.EOF):
            self.next()
        if self.peek().type == TokenType.STRING:
            target = str(self.next().value)
        return ast.AiLocal(prompt, target)

    def parse_web3(self):
        """اتصل_محفظة "network" """
        self.next()
        network = ''
        while self.peek().type not in (TokenType.STRING, TokenType.NEWLINE,
                                         TokenType.DEDENT, TokenType.EOF):
            self.next()
        if self.peek().type == TokenType.STRING:
            network = str(self.next().value)
        return ast.Web3Connect(network)

    def parse_scene_3d(self):
        """مشهد 3D"""
        self.next()
        if self.peek().type == TokenType.COLON:
            self.next()
        self.skip_newlines()
        if self.peek().type == TokenType.INDENT:
            self.next()
        props = self.parse_props()
        if self.peek().type == TokenType.DEDENT:
            self.next()
        return ast.Scene3D(props)

    def parse_ar_scene(self):
        """مشهد AR"""
        self.next()
        if self.peek().type == TokenType.COLON:
            self.next()
        self.skip_newlines()
        if self.peek().type == TokenType.INDENT:
            self.next()
        props = self.parse_props()
        if self.peek().type == TokenType.DEDENT:
            self.next()
        return ast.ArScene(props)

    def parse_generator(self):
        """دالة* - Generator"""
        self.next()  # GENERATOR
        name = ''
        if self.peek().value:
            name = str(self.next().value)
        # تجاهل ()
        while self.peek().type not in (TokenType.COLON, TokenType.NEWLINE,
                                         TokenType.DEDENT, TokenType.EOF):
            self.next()
        if self.peek().type == TokenType.COLON:
            self.next()
        self.skip_newlines()
        if self.peek().type == TokenType.INDENT:
            self.next()
        body = []
        while True:
            self.skip_newlines()
            t = self.peek()
            if t.type in (TokenType.DEDENT, TokenType.EOF, TokenType.END):
                break
            if t.type == TokenType.YIELD_KW:
                body.append(self.parse_yield())
            elif t.type == TokenType.VAR_KW:
                body.append(self.parse_var_decl())
            else:
                self.next()
        if self.peek().type == TokenType.DEDENT:
            self.next()
        return ast.Generator(name, body)

    def parse_yield(self):
        """حاصل قيمة"""
        self.next()
        value = None
        if self.peek().type not in (TokenType.NEWLINE, TokenType.DEDENT, TokenType.EOF):
            value = self.parse_expression()
        return ast.YieldValue(value)


    def parse_class(self):
        """فئة/صنف: ..."""
        self.next()  # CLASS_KW
        name = ''
        if self.peek().value:
            name = str(self.next().value)
        extends = ''
        if self.peek().type == TokenType.EXTENDS:
            self.next()
            if self.peek().value:
                extends = str(self.next().value)
        if self.peek().type == TokenType.COLON:
            self.next()
        self.skip_newlines()
        if self.peek().type == TokenType.INDENT:
            self.next()

        methods = []
        fields = []
        while True:
            self.skip_newlines()
            t = self.peek()

            # DEDENT يعني الفئة خلصت
            if t.type == TokenType.DEDENT:
                self.next()  # استهلك DEDENT بتاع الفئة
                break

            if t.type in (TokenType.EOF, TokenType.END):
                break

            # INDENT جديد يعني خرجنا من الفئة
            if t.type == TokenType.INDENT:
                break

            # الحاجات المسموحة جوّه الفئة
            if t.type == TokenType.FUNCTION:
                methods.append(self.parse_function())
            elif t.type == TokenType.VAR_KW:
                fields.append(self.parse_var_decl())
            else:
                # حاجة مش معروفة — وقف
                break

        return ast.ClassDef(name, extends, methods, fields)


    def parse_async(self):
        """غير_متزامن دالة"""
        self.next()
        if self.peek().type == TokenType.FUNCTION:
            func = self.parse_function()
            return ast.AsyncFunc(func.name, func.params, func.body)
        return ast.AsyncFunc()

    def parse_match(self):
        """طابق ... مع"""
        self.next()
        expr = self.parse_expression()
        if self.peek().type == TokenType.IN:
            self.next()
        if self.peek().type == TokenType.COLON:
            self.next()
        self.skip_newlines()
        if self.peek().type == TokenType.INDENT:
            self.next()
        cases = []
        while True:
            self.skip_newlines()
            t = self.peek()
            if t.type in (TokenType.DEDENT, TokenType.EOF, TokenType.END):
                break
            if t.type == TokenType.CASE_KW:
                self.next()
                val = self.parse_expression()
                if self.peek().type == TokenType.COLON:
                    self.next()
                self.skip_newlines()
                if self.peek().type == TokenType.INDENT:
                    self.next()
                body = []
                while True:
                    self.skip_newlines()
                    bt = self.peek()
                    if bt.type in (TokenType.DEDENT, TokenType.EOF, TokenType.END,
                                    TokenType.CASE_KW):
                        break
                    if bt.type == TokenType.SHOW:
                        body.append(self.parse_show())
                    else:
                        self.next()
                if self.peek().type == TokenType.DEDENT:
                    self.next()
                cases.append(ast.MatchCase(val, body))
            else:
                self.next()
        if self.peek().type == TokenType.DEDENT:
            self.next()
        return ast.Match(expr, cases)

    def parse_throw(self):
        """ارمِ خطأ"""
        self.next()
        msg = ''
        while self.peek().type not in (TokenType.STRING, TokenType.NEWLINE,
                                         TokenType.DEDENT, TokenType.EOF):
            self.next()
        if self.peek().type == TokenType.STRING:
            msg = str(self.next().value)
        return ast.ThrowError(msg)


    def parse_const(self):
        """ثابت س = 5"""
        self.next()  # CONST_KW
        name = ''
        if self.peek().value:
            name = str(self.next().value)
        # شوف لو فيه : نوع
        type_hint = ''
        if self.peek().type == TokenType.COLON:
            self.next()
            if self.peek().value:
                type_hint = str(self.next().value)
        if self.peek().type == TokenType.EQUALS:
            self.next()
        value = self.parse_expression()
        return ast.ConstDecl(name, value, type_hint)


    def parse_modal(self):
        """نافذة منبثقة"""
        self.next()
        if self.peek().type == TokenType.COLON:
            self.next()
        self.skip_newlines()
        if self.peek().type == TokenType.INDENT:
            self.next()
        props = self.parse_props()
        # ابحث عن عند_الضغط
        actions = []
        self.skip_newlines()
        if self.peek().type == TokenType.ON_CLICK:
            self.next()
            if self.peek().type == TokenType.COLON:
                self.next()
            self.skip_newlines()
            if self.peek().type == TokenType.INDENT:
                self.next()
            while True:
                self.skip_newlines()
                t = self.peek()
                if t.type in (TokenType.DEDENT, TokenType.EOF, TokenType.END):
                    break
                if t.type == TokenType.SHOW:
                    actions.append(self.parse_show())
                else:
                    self.next()
            if self.peek().type == TokenType.DEDENT:
                self.next()
        if self.peek().type == TokenType.DEDENT:
            self.next()
        return ast.CreateModal(props, actions)

    def parse_tooltip(self):
        """تلميح"""
        self.next()
        if self.peek().type == TokenType.COLON:
            self.next()
        self.skip_newlines()
        if self.peek().type == TokenType.INDENT:
            self.next()
        props = self.parse_props()
        if self.peek().type == TokenType.DEDENT:
            self.next()
        return ast.AddTooltip(props)

    def parse_accordion(self):
        """قائمة طي"""
        self.next()
        if self.peek().type == TokenType.COLON:
            self.next()
        self.skip_newlines()
        if self.peek().type == TokenType.INDENT:
            self.next()
        props = self.parse_props()
        if self.peek().type == TokenType.DEDENT:
            self.next()
        return ast.CreateAccordion(props)

    def parse_sidebar(self):
        """شريط جانبي"""
        self.next()
        if self.peek().type == TokenType.COLON:
            self.next()
        self.skip_newlines()
        if self.peek().type == TokenType.INDENT:
            self.next()
        props = self.parse_props()
        if self.peek().type == TokenType.DEDENT:
            self.next()
        return ast.CreateSidebar(props)

    def parse_navbar(self):
        """شريط تنقل"""
        self.next()
        if self.peek().type == TokenType.COLON:
            self.next()
        self.skip_newlines()
        if self.peek().type == TokenType.INDENT:
            self.next()
        props = self.parse_props()
        if self.peek().type == TokenType.DEDENT:
            self.next()
        return ast.CreateNavbar(props)

    def parse_form(self):
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


    def parse_tabs(self):
        """تبويبات"""
        self.next()
        if self.peek().type == TokenType.COLON:
            self.next()
        self.skip_newlines()
        if self.peek().type == TokenType.INDENT:
            self.next()
        props = self.parse_props()
        while self.peek().type == TokenType.DEDENT:
            self.next()
        return ast.CreateTabs(props, [])

    def parse_local_decl(self):
        """محلي س = 5"""
        self.next()  # LOCAL
        name = ''
        if self.peek().type in (TokenType.IDENTIFIER, TokenType.FILE_NAME):
            name = str(self.next().value)
        value = None
        if self.peek().type == TokenType.EQUALS:
            self.next()
            value = self.parse_expression()
        return ast.LocalDecl(name, value)

    def parse_global_decl(self):
        """عالمي س = 5 أو عالمي س"""
        self.next()  # GLOBAL
        name = ''
        if self.peek().type in (TokenType.IDENTIFIER, TokenType.FILE_NAME):
            name = str(self.next().value)
        value = None
        if self.peek().type == TokenType.EQUALS:
            self.next()
            value = self.parse_expression()
        return ast.GlobalDecl(name, value)

    def parse_nonlocal_decl(self):
        """غير_محلي س"""
        self.next()  # NONLOCAL
        name = ''
        if self.peek().type in (TokenType.IDENTIFIER, TokenType.FILE_NAME):
            name = str(self.next().value)
        return ast.NonlocalDecl(name)

    def parse_var_decl(self):
        """متغير س = 5 أو متغير س: عدد = 5"""
        self.next()  # VAR_KW
        name = ''
        if self.peek().type in (TokenType.IDENTIFIER, TokenType.FILE_NAME,
                                TokenType.IDENTIFIER_PROP):
            name = str(self.next().value)

        # نوع اختياري: متغير س: عدد
        type_hint = ''
        if self.peek().type == TokenType.COLON:
            self.next()  # :
            # النوع ممكن يكون IDENTIFIER أو keyword (رقم → TO_NUM، نص → TO_STR)
            if self.peek().type in (TokenType.IDENTIFIER, TokenType.FILE_NAME):
                type_hint = str(self.next().value)
            elif self.peek().value:
                # نوع من keyword
                type_hint = str(self.next().value)

        # القيمة
        value = None
        if self.peek().type == TokenType.EQUALS:
            self.next()
            value = self.parse_expression()

        # لو فيه نوع → TypeDecl، لو لأ → VarDecl
        if type_hint:
            return ast.TypeDecl(name, type_hint, value)
        return ast.VarDecl(name, value)

    def parse_map(self):
        """خريطة"""
        self.next()  # MAP_KW
        if self.peek().type == TokenType.COLON:
            self.next()
        self.skip_newlines()
        if self.peek().type == TokenType.INDENT:
            self.next()

        props = {}
        while True:
            self.skip_newlines()
            t = self.peek()
            if t.type in (TokenType.DEDENT, TokenType.EOF, TokenType.END):
                break
            if t.type in (TokenType.LAT, TokenType.LNG, TokenType.ZOOM,
                          TokenType.TITLE_PROP, TokenType.POSITION,
                          TokenType.IDENTIFIER, TokenType.SIZE):
                key = str(self.next().value)
                if self.peek().type == TokenType.COLON:
                    self.next()
                if self.peek().type == TokenType.NUMBER:
                    val = self.next().value
                else:
                    val = str(self.next().value)
                props[key] = val
            else:
                self.next()

        if self.peek().type == TokenType.DEDENT:
            self.next()

        try:
            lat = float(props.get('الموقع', 30.0444))
        except:
            lat = 30.0444
        try:
            lng = float(props.get('العرض', 31.2357))
        except:
            lng = 31.2357
        try:
            zoom = int(props.get('التكبير', 12))
        except:
            zoom = 12

        return ast.CreateMap(props, lat, lng, zoom)

    def parse_websocket(self):
        """اتصال_مباشر "url" """
        self.next()  # WS_KW
        url = ''
        while self.peek().type not in (TokenType.STRING, TokenType.NEWLINE,
                                         TokenType.EOF, TokenType.DEDENT):
            self.next()
        if self.peek().type == TokenType.STRING:
            url = str(self.next().value)
        return ast.WebSocketConnect(url)

    def parse_auth_login(self):
        """تسجيل_دخول "user" "pass" """
        self.next()  # LOGIN
        username = ''
        password = ''
        # اقرأ لحد STRING الأول
        while self.peek().type not in (TokenType.STRING, TokenType.NEWLINE,
                                         TokenType.EOF, TokenType.DEDENT):
            self.next()
        if self.peek().type == TokenType.STRING:
            username = str(self.next().value)
        # تجاهل لحد STRING التاني
        while self.peek().type not in (TokenType.STRING, TokenType.NEWLINE,
                                         TokenType.EOF, TokenType.DEDENT):
            self.next()
        if self.peek().type == TokenType.STRING:
            password = str(self.next().value)
        return ast.AuthAction('login', username, password)

    def parse_auth_logout(self):
        """تسجيل_خروج"""
        self.next()  # LOGOUT
        return ast.AuthAction('logout', '', '')

    def parse_auth_register(self):
        """حساب_جديد "user" "pass" """
        self.next()  # REGISTER
        username = ''
        password = ''
        while self.peek().type not in (TokenType.STRING, TokenType.NEWLINE,
                                         TokenType.EOF, TokenType.DEDENT):
            self.next()
        if self.peek().type == TokenType.STRING:
            username = str(self.next().value)
        while self.peek().type not in (TokenType.STRING, TokenType.NEWLINE,
                                         TokenType.EOF, TokenType.DEDENT):
            self.next()
        if self.peek().type == TokenType.STRING:
            password = str(self.next().value)
        return ast.AuthAction('register', username, password)

    def parse_pdf(self):
        """ملف_PDF"""
        self.next()  # ملف_PDF
        if self.peek().type == TokenType.COLON:
            self.next()
        self.skip_newlines()
        if self.peek().type == TokenType.INDENT:
            self.next()

        # اقرأ props
        props = {}
        while True:
            self.skip_newlines()
            t = self.peek()
            if t.type in (TokenType.DEDENT, TokenType.EOF, TokenType.END):
                break
            if t.type in (TokenType.TITLE_PROP, TokenType.TITLE,
                          TokenType.NAME, TokenType.FILE_NAME,
                          TokenType.IDENTIFIER, TokenType.IDENTIFIER_PROP):
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

        title = props.get('العنوان', 'تقرير')
        filename = props.get('الاسم', 'document.pdf')
        return ast.CreatePdf(title, None, filename)

    def parse_qr(self):
        """qr "..." """
        self.next()  # qr
        content = ''
        if self.peek().type == TokenType.STRING:
            content = str(self.next().value)
        return ast.CreateQr(content, 200)

    def parse_for_index(self):
        """لكل_بفهرس i, عنصر في القائمة: ..."""
        self.next()  # FOR_INDEX

        # اسم الفهرس
        idx_name = ''
        if self.peek().type in (TokenType.IDENTIFIER, TokenType.FILE_NAME):
            idx_name = str(self.next().value)
        elif self.peek().type in (TokenType.VAR_KW,):
            self.next()
            if self.peek().type in (TokenType.IDENTIFIER, TokenType.FILE_NAME):
                idx_name = str(self.next().value)

        # فاصلة
        if self.peek().type == TokenType.COMMA:
            self.next()

        # اسم المتغير
        var_name = ''
        if self.peek().type in (TokenType.IDENTIFIER, TokenType.FILE_NAME):
            var_name = str(self.next().value)

        # في
        if self.peek().type == TokenType.IN:
            self.next()

        # القائمة
        iterable = self.parse_term()

        # :
        if self.peek().type == TokenType.COLON:
            self.next()
        self.skip_newlines()

        # استهلك INDENT
        if self.peek().type == TokenType.INDENT:
            self.next()

        body = []
        while True:
            self.skip_newlines()
            t = self.peek()
            if t.type in (TokenType.DEDENT, TokenType.EOF, TokenType.END):
                break
            if t.type == TokenType.SHOW:
                body.append(self.parse_show())
            elif t.type == TokenType.VAR_KW:
                body.append(self.parse_var_decl())
            elif t.type == TokenType.IF:
                body.append(self.parse_if())
            elif t.type in (TokenType.IDENTIFIER, TokenType.FILE_NAME,
                            TokenType.IDENTIFIER_PROP, TokenType.SELF):
                self._parse_identifier_statement(body)
            else:
                self.next()

        # استهلك DEDENT واحد
        if self.peek().type == TokenType.DEDENT:
            self.next()

        return ast.ForIndex(idx_name, var_name, iterable, body)

    def parse_while(self):
        """طالما شرط: ..."""
        self.next()  # WHILE
        condition = self.parse_comparison()
        if self.peek().type == TokenType.COLON:
            self.next()
        self.skip_newlines()
        body = self.parse_block()
        return ast.While(condition, body)

    def parse_for(self):
        """لكل س في [1، 2، 3]: ... أو لكل مفتاح, قيمة في قاموس: ..."""
        self.next()  # FOR
        first_name = str(self.next().value)

        # هل فيه فاصلة؟ → ForDict
        if self.peek().type == TokenType.COMMA:
            self.next()  # ,
            second_name = ''
            if self.peek().type in (TokenType.IDENTIFIER, TokenType.FILE_NAME):
                second_name = str(self.next().value)
            if self.peek().type == TokenType.IN:
                self.next()
            iterable = self.parse_expression()
            if self.peek().type == TokenType.COLON:
                self.next()
            self.skip_newlines()
            body = self.parse_block()
            return ast.ForDict(first_name, second_name, iterable, body)

        # ForIn عادي
        if self.peek().type == TokenType.IN:
            self.next()
        iterable = self.parse_expression()
        if self.peek().type == TokenType.COLON:
            self.next()
        self.skip_newlines()
        body = self.parse_block()
        return ast.ForIn(first_name, iterable, body)

    def parse_expression(self):
        """تعبير حسابي كامل بأولويات: OR > AND > مقارنة > حساب"""
        return self.parse_or_expr()

    def parse_or_expr(self):
        """أو (OR)"""
        left = self.parse_and_expr()
        while self.peek().type == TokenType.OR:
            self.next()
            right = self.parse_and_expr()
            left = ast.BinOp(left, '||', right)
        return left

    def parse_and_expr(self):
        """و (AND)"""
        left = self.parse_comparison_only()
        while self.peek().type == TokenType.AND:
            self.next()
            right = self.parse_comparison_only()
            left = ast.BinOp(left, '&&', right)
        return left

    def parse_comparison_only(self):
        """مقارنة: > < >= <= == !="""
        left = self.parse_math_expr()
        if self.peek().type in (TokenType.GREATER, TokenType.LESS,
                                 TokenType.GREATER_EQ, TokenType.LESS_EQ,
                                 TokenType.EQUAL_EQUAL, TokenType.NOT_EQUAL):
            op = self.next()
            right = self.parse_math_expr()
            return ast.Compare(left, op.value, right)
        return left

    def parse_math_expr(self):
        """حساب: + - * / %"""
        left = self.parse_term()

        while self.peek().type in (TokenType.PLUS, TokenType.MINUS,
                                     TokenType.MULTIPLY, TokenType.DIVIDE,
                                     TokenType.MODULO):
            op = self.next()
            right = self.parse_term()
            op_str = {
                TokenType.PLUS: '+', TokenType.MINUS: '-',
                TokenType.MULTIPLY: '*', TokenType.DIVIDE: '/',
                TokenType.MODULO: '%'
            }.get(op.type, '+')
            left = ast.BinOp(left, op_str, right)

        return left



    def parse_call(self, name):
        """يقرأ استدعاء دالة: name(args)"""
        # استهلك (
        if self.peek().type == TokenType.LPAREN:
            self.next()
        args = []
        # اقرأ المعاملات
        while self.peek().type != TokenType.RPAREN:
            if self.peek().type == TokenType.EOF:
                break
            self.skip_newlines()
            if self.peek().type == TokenType.RPAREN:
                break
            args.append(self.parse_expression())
            if self.peek().type == TokenType.COMMA:
                self.next()
            else:
                break
        # استهلك )
        if self.peek().type == TokenType.RPAREN:
            self.next()
        return ast.FunctionCall(name, args)

    def parse_term(self):
        """أساسي: رقم أو نص أو متغير أو قائمة أو دالة مدمجة"""
        # Lambda: (س, ص) => تعبير
        if self.peek().type == TokenType.LPAREN:
            saved_pos = self.pos
            self.next()  # (
            params = []
            # اقرأ المعاملات
            while self.peek().type != TokenType.RPAREN:
                if self.peek().type in (TokenType.IDENTIFIER, TokenType.FILE_NAME):
                    params.append(str(self.next().value))
                else:
                    break
                if self.peek().type == TokenType.COMMA:
                    self.next()
                else:
                    break
            if self.peek().type == TokenType.RPAREN:
                self.next()  # )
                # هل التالي => ؟
                if (self.peek().type == TokenType.EQUALS and
                    self.peek(1).type == TokenType.GREATER):
                    self.next()  # =
                    self.next()  # >
                    body = self.parse_expression()
                    return ast.Lambda(params, body)
            # مش lambda
            self.pos = saved_pos

        t = self.peek()

        # ===== 0) جديد صنف(وسائط) =====
        if t.type == TokenType.NEW:
            self.next()  # جديد
            class_name = str(self.next().value)
            args = []
            if self.peek().type == TokenType.LPAREN:
                self.next()  # (
                while self.peek().type != TokenType.RPAREN:
                    self.skip_newlines()
                    if self.peek().type == TokenType.RPAREN:
                        break
                    args.append(self.parse_term())
                    if self.peek().type == TokenType.COMMA:
                        self.next()
                    else:
                        break
                if self.peek().type == TokenType.RPAREN:
                    self.next()  # )
            return ast.NewInstance(class_name, args)

        # ===== 0-ب) أساس(...) =====
        if t.type == TokenType.SUPER:
            self.next()
            args = []
            if self.peek().type == TokenType.LPAREN:
                self.next()
                while self.peek().type != TokenType.RPAREN:
                    self.skip_newlines()
                    if self.peek().type == TokenType.RPAREN:
                        break
                    args.append(self.parse_term())
                    if self.peek().type == TokenType.COMMA:
                        self.next()
                    else:
                        break
                if self.peek().type == TokenType.RPAREN:
                    self.next()
            return ast.MethodCall(ast.VarRef('هذا'), 'أساس', args)

        # ===== 0-ج) هذا =====
        if t.type == TokenType.SELF:
            self.next()
            result = ast.VarRef('هذا')
            # دعم النقطة: هذا.اسم
            while True:
                if self.peek().type == TokenType.DOT:
                    self.next()
                    attr = str(self.next().value)
                    if self.peek().type == TokenType.LPAREN:
                        self.next()
                        args = []
                        while self.peek().type != TokenType.RPAREN:
                            self.skip_newlines()
                            if self.peek().type == TokenType.RPAREN:
                                break
                            args.append(self.parse_term())
                            if self.peek().type == TokenType.COMMA:
                                self.next()
                            else:
                                break
                        if self.peek().type == TokenType.RPAREN:
                            self.next()
                        result = ast.MethodCall(result, attr, args)
                    else:
                        result = ast.MemberAccess(result, attr)
                elif self.peek().type == TokenType.LBRACKET:
                    self.next()
                    idx = self.parse_term()
                    if self.peek().type == TokenType.RBRACKET:
                        self.next()
                    result = ast.IndexAccess(result, idx)
                else:
                    break
            return result

        # ===== 1) دوال مدمجة (لازم قبل أي حاجة) =====
        if t.type in (TokenType.SORT, TokenType.REVERSE, TokenType.FIRST,
                      TokenType.LAST, TokenType.TO_NUM, TokenType.TO_STR,
                      TokenType.SPLIT, TokenType.REPLACE, TokenType.SUBSTR,
                      TokenType.SQRT, TokenType.POWER, TokenType.RANDOM,
                      TokenType.ROUND, TokenType.CONTAINS, TokenType.STARTS_WITH,
                      TokenType.ENDS_WITH, TokenType.TRIM,
                      TokenType.FIND, TokenType.FILTER, TokenType.MAP_METHOD,
                      TokenType.REDUCE, TokenType.REGEX_MATCH,
                      TokenType.JSON_STRINGIFY, TokenType.JSON_PARSE):
            func_name = str(t.value)
            self.next()
            args = []
            if self.peek().type == TokenType.LPAREN:
                self.next()
                while self.peek().type != TokenType.RPAREN:
                    self.skip_newlines()
                    if self.peek().type == TokenType.RPAREN:
                        break
                    args.append(self.parse_term())
                    if self.peek().type == TokenType.COMMA:
                        self.next()
                    else:
                        break
                if self.peek().type == TokenType.RPAREN:
                    self.next()
            return ast.BuiltinCall(func_name, args)

        # ===== 2) طول() =====
        if t.type == TokenType.LENGTH:
            self.next()
            if self.peek().type == TokenType.LPAREN:
                self.next()
            arg = self.parse_term()
            if self.peek().type == TokenType.RPAREN:
                self.next()
            return ast.FunctionCall('طول', [arg])

        # ===== 3) Lambda =====
        if t.type == TokenType.LPAREN:
            saved_pos = self.pos
            self.next()
            params = []
            while self.peek().type != TokenType.RPAREN:
                if self.peek().type in (TokenType.IDENTIFIER, TokenType.FILE_NAME):
                    params.append(str(self.next().value))
                else:
                    break
                if self.peek().type == TokenType.COMMA:
                    self.next()
                else:
                    break
            if self.peek().type == TokenType.RPAREN:
                self.next()
                if (self.peek().type == TokenType.EQUALS and
                    self.peek(1).type == TokenType.GREATER):
                    self.next()
                    self.next()
                    body = self.parse_term()
                    return ast.Lambda(params, body)
            self.pos = saved_pos

        # ===== 4) قائمة =====
        if t.type == TokenType.LBRACKET:
            return self.parse_list()

        # ===== 4-ب) قاموس {...} =====
        if t.type == TokenType.LBRACE:
            return self.parse_dict()

        # ===== 4-ج) صح/غلط =====
        if t.type == TokenType.BOOLEAN:
            self.next()
            return ast.Bool(bool(t.value))

        # ===== 5) رقم =====
        if t.type == TokenType.NUMBER:
            return ast.Number(self.next().value)

        # ===== 6) نص (مع TemplateString) =====
        if t.type == TokenType.STRING:
            val = str(self.next().value)
            if '{' in val and '}' in val:
                import re as regex
                parts = []
                last = 0
                for match in regex.finditer(r'\{([^}]+)\}', val):
                    if match.start() > last:
                        parts.append(ast.String(val[last:match.start()]))
                    parts.append(ast.VarRef(match.group(1).strip()))
                    last = match.end()
                if last < len(val):
                    parts.append(ast.String(val[last:]))
                return ast.TemplateString(parts)
            return ast.String(val)

        # ===== 7) لا_شيء =====
        if t.type == TokenType.NULL_LIT:
            self.next()
            return ast.NullLit()

        # ===== 8) متغير/دالة =====
        if t.type in (TokenType.IDENTIFIER, TokenType.FILE_NAME,
                       TokenType.IDENTIFIER_PROP):
            name = str(self.next().value)
            if self.peek().type == TokenType.LPAREN:
                result = self.parse_call(name)
            else:
                result = ast.VarRef(name)
            # فهرسة ونقطة
            while True:
                if self.peek().type == TokenType.LBRACKET:
                    self.next()
                    idx = self.parse_term()
                    if self.peek().type == TokenType.RBRACKET:
                        self.next()
                    result = ast.IndexAccess(result, idx)
                elif self.peek().type == TokenType.DOT:
                    self.next()  # .
                    if not self.peek().value:
                        break
                    attr = str(self.next().value)
                    if self.peek().type == TokenType.LPAREN:
                        # method call
                        self.next()
                        args = []
                        while self.peek().type != TokenType.RPAREN:
                            self.skip_newlines()
                            if self.peek().type == TokenType.RPAREN:
                                break
                            args.append(self.parse_term())
                            if self.peek().type == TokenType.COMMA:
                                self.next()
                            else:
                                break
                        if self.peek().type == TokenType.RPAREN:
                            self.next()
                        result = ast.MethodCall(result, attr, args)
                    else:
                        result = ast.MemberAccess(result, attr)
                else:
                    break
            return result

        # ===== 9) أي حاجة تانية =====
        return ast.String(str(self.next().value))


    def parse_list(self):
        """يقرأ [1, 2, 3] أو [[1,2],[3,4]]"""
        opener = self.next()

        if opener.type == TokenType.LBRACKET:
            closer = TokenType.RBRACKET
        else:
            closer = TokenType.RPAREN

        items = []

        while True:
            while self.peek().type == TokenType.NEWLINE:
                self.next()

            if self.peek().type == closer:
                self.next()
                break

            if self.peek().type == TokenType.EOF:
                break

            # اقرأ عنصر (ممكن يكون قائمة داخلية)
            if self.peek().type == TokenType.LBRACKET:
                item = self.parse_list()
            else:
                item = self.parse_term()
            items.append(item)

            while self.peek().type == TokenType.NEWLINE:
                self.next()

            if self.peek().type == TokenType.COMMA:
                self.next()
                continue
            elif self.peek().type == closer:
                self.next()
                break
            else:
                break

        return ast.ListLiteral(items)



    def parse_dict(self):
        """يقرأ قاموس {مفتاح: قيمة, ...}"""
        self.next()  # {
        pairs = []

        while True:
            self.skip_newlines()
            t = self.peek()

            if t.type == TokenType.RBRACE:
                self.next()
                break

            if t.type == TokenType.EOF:
                break

            # اقرأ المفتاح — IDENTIFIER → نص تلقائي
            if self.peek().type in (TokenType.IDENTIFIER, TokenType.FILE_NAME,
                                    TokenType.IDENTIFIER_PROP):
                # خد الاسم كنص
                key = ast.String(str(self.next().value))
            else:
                key = self.parse_term()

            # :
            if self.peek().type == TokenType.COLON:
                self.next()
            else:
                # مش قاموس — بس قوس؟ نتجاهل ونكمل
                if self.peek().type == TokenType.COMMA:
                    self.next()
                    continue
                else:
                    break

            # اقرأ القيمة
            value = self.parse_term()
            pairs.append((key, value))

            # , أو }
            if self.peek().type == TokenType.COMMA:
                self.next()
            elif self.peek().type == TokenType.RBRACE:
                self.next()
                break
            else:
                self.skip_newlines()
                if self.peek().type == TokenType.RBRACE:
                    self.next()
                    break

        return ast.DictLiteral(pairs)

    def parse_if(self):
        """لو شرط: ... وإلا لو شرط: ... وإلا: ..."""
        self.next()  # IF
        condition = self.parse_comparison()
        if self.peek().type == TokenType.COLON:
            self.next()
        self.skip_newlines()

        # استهلك INDENT
        if self.peek().type == TokenType.INDENT:
            self.next()

        # جسم الـ if
        then_body = []
        while True:
            self.skip_newlines()
            t = self.peek()
            if t.type in (TokenType.DEDENT, TokenType.EOF, TokenType.END,
                          TokenType.ELSE, TokenType.ELSE_IF):
                break
            # نفس كود parse_block
            if t.type == TokenType.VAR_KW:
                then_body.append(self.parse_var_decl())
            elif t.type == TokenType.SHOW:
                then_body.append(self.parse_show())
            elif t.type == TokenType.CLEAR:
                then_body.append(self.parse_clear())
            elif t.type == TokenType.IF:
                then_body.append(self.parse_if())
            elif t.type == TokenType.WHILE:
                then_body.append(self.parse_while())
            elif t.type == TokenType.FOR:
                then_body.append(self.parse_for())
            elif t.type == TokenType.RETURN:
                then_body.append(self.parse_return())
            elif t.type == TokenType.BREAK:
                self.next(); then_body.append(ast.Break())
            elif t.type == TokenType.CONTINUE:
                self.next(); then_body.append(ast.Continue())
            elif t.type in (TokenType.COPY, TokenType.MOVE,
                            TokenType.DELETE, TokenType.READ,
                            TokenType.SAVE, TokenType.NEW_FOLDER,
                            TokenType.OPEN):
                then_body.append(self.parse_file_op())
            elif t.type in (TokenType.IDENTIFIER, TokenType.FILE_NAME,
                            TokenType.IDENTIFIER_PROP, TokenType.SELF):
                self._parse_identifier_statement(then_body)
            else:
                self.next()

        # استهلك DEDENT
        while self.peek().type == TokenType.DEDENT:
            self.next()

        # وإلا لو / بعدين
        else_body = []
        self.skip_newlines()

        # ELSE_IF (وإلا لو / بعدين)
        if self.peek().type == TokenType.ELSE_IF:
            self.next()
            # إذا كان بعده "لو"، تخطاها
            if self.peek().type == TokenType.IF:
                self.next()
            # parse_if مرة تانية
            nested_if = self.parse_if_inner()
            else_body = [nested_if]

        # ELSE (وإلا)
        elif self.peek().type == TokenType.ELSE:
            self.next()
            if self.peek().type == TokenType.COLON:
                self.next()
            self.skip_newlines()

            if self.peek().type == TokenType.INDENT:
                self.next()

            while True:
                self.skip_newlines()
                t = self.peek()
                if t.type in (TokenType.DEDENT, TokenType.EOF, TokenType.END):
                    break
                if t.type == TokenType.VAR_KW:
                    else_body.append(self.parse_var_decl())
                elif t.type == TokenType.SHOW:
                    else_body.append(self.parse_show())
                elif t.type == TokenType.IF:
                    else_body.append(self.parse_if())
                elif t.type == TokenType.WHILE:
                    else_body.append(self.parse_while())
                elif t.type == TokenType.FOR:
                    else_body.append(self.parse_for())
                elif t.type == TokenType.RETURN:
                    else_body.append(self.parse_return())
                elif t.type == TokenType.BREAK:
                    self.next(); else_body.append(ast.Break())
                elif t.type == TokenType.CONTINUE:
                    self.next(); else_body.append(ast.Continue())
                elif t.type in (TokenType.IDENTIFIER, TokenType.FILE_NAME,
                                TokenType.IDENTIFIER_PROP, TokenType.SELF):
                    self._parse_identifier_statement(else_body)
                else:
                    self.next()

            while self.peek().type == TokenType.DEDENT:
                self.next()

        return ast.If(condition, then_body, else_body)

    def parse_if_inner(self):
        """يقرأ الشرط الداخلي بعد 'وإلا لو'"""
        # اقرأ الشرط بدون IF
        condition = self.parse_comparison()
        if self.peek().type == TokenType.COLON:
            self.next()
        self.skip_newlines()

        if self.peek().type == TokenType.INDENT:
            self.next()

        then_body = []
        while True:
            self.skip_newlines()
            t = self.peek()
            if t.type in (TokenType.DEDENT, TokenType.EOF, TokenType.END,
                          TokenType.ELSE, TokenType.ELSE_IF):
                break
            if t.type == TokenType.SHOW:
                then_body.append(self.parse_show())
            elif t.type == TokenType.VAR_KW:
                then_body.append(self.parse_var_decl())
            elif t.type == TokenType.IF:
                then_body.append(self.parse_if())
            elif t.type == TokenType.WHILE:
                then_body.append(self.parse_while())
            elif t.type == TokenType.FOR:
                then_body.append(self.parse_for())
            elif t.type == TokenType.BREAK:
                self.next(); then_body.append(ast.Break())
            elif t.type == TokenType.CONTINUE:
                self.next(); then_body.append(ast.Continue())
            elif t.type in (TokenType.IDENTIFIER, TokenType.FILE_NAME,
                            TokenType.IDENTIFIER_PROP, TokenType.SELF):
                self._parse_identifier_statement(then_body)
            else:
                self.next()

        while self.peek().type == TokenType.DEDENT:
            self.next()

        # وإلا لو / وإلا
        else_body = []
        self.skip_newlines()

        if self.peek().type == TokenType.ELSE_IF:
            self.next()
            if self.peek().type == TokenType.IF:
                self.next()
            else_body = [self.parse_if_inner()]
        elif self.peek().type == TokenType.ELSE:
            self.next()
            if self.peek().type == TokenType.COLON:
                self.next()
            self.skip_newlines()
            if self.peek().type == TokenType.INDENT:
                self.next()
            while True:
                self.skip_newlines()
                t = self.peek()
                if t.type in (TokenType.DEDENT, TokenType.EOF, TokenType.END):
                    break
                if t.type == TokenType.SHOW:
                    else_body.append(self.parse_show())
                elif t.type == TokenType.VAR_KW:
                    else_body.append(self.parse_var_decl())
                elif t.type in (TokenType.IDENTIFIER, TokenType.FILE_NAME):
                    nxt = self.peek(1)
                    if nxt.type in (TokenType.EQUALS, TokenType.PLUS_EQ):
                        else_body.append(self.parse_assign())
                    else:
                        self.next()
                else:
                    self.next()
            while self.peek().type == TokenType.DEDENT:
                self.next()

        return ast.If(condition, then_body, else_body)

    def parse_comparison(self):
        left = self.parse_expression()
        if self.peek().type in (TokenType.GREATER, TokenType.LESS,
                                 TokenType.GREATER_EQ, TokenType.LESS_EQ,
                                 TokenType.EQUAL_EQUAL, TokenType.NOT_EQUAL):
            op = self.next()
            right = self.parse_expression()
            return ast.Compare(left, op.value, right)
        return left

    def parse_show(self):
        """اعرض تعبير في: "#target" """
        self.next()  # SHOW

        # اقرأ النص/التعبير
        if self.peek().type == TokenType.STRING:
            val = str(self.next().value)
            # لو فيه {var} أو {func()} → TemplateString
            if '{' in val and '}' in val:
                import re as regex
                parts = []
                last = 0
                for match in regex.finditer(r'\{([^}]+)\}', val):
                    if match.start() > last:
                        parts.append(ast.String(val[last:match.start()]))
                    expr_str = match.group(1).strip()
                    # لو فيه () → استدعاء دالة
                    if '(' in expr_str and ')' in expr_str:
                        func_name = expr_str.split('(')[0].strip()
                        args_str = expr_str.split('(', 1)[1].rsplit(')', 1)[0].strip()
                        # فكك args
                        args_list = []
                        if args_str:
                            # قسّم على الفاصلة
                            for arg in args_str.split(','):
                                arg = arg.strip()
                                # لو رقم
                                if arg.isdigit():
                                    args_list.append(ast.Number(int(arg)))
                                # لو نص
                                elif arg.startswith('"') or arg.startswith("'"):
                                    args_list.append(ast.String(arg.strip('"\'')))
                                # لو متغير
                                else:
                                    args_list.append(ast.VarRef(arg))
                        # دالة تاريخ؟
                        if func_name in ('الآن', 'اليوم'):
                            parts.append(ast.DateCall(func_name))
                        else:
                            parts.append(ast.BuiltinCall(func_name, args_list))
                    else:
                        parts.append(ast.VarRef(expr_str))
                    last = match.end()
                if last < len(val):
                    parts.append(ast.String(val[last:]))
                text = ast.TemplateString(parts)
            else:
                text = ast.String(val)
        else:
            text = self.parse_expression_until_in()

        # IN
        if self.peek().type == TokenType.IN:
            self.next()
        if self.peek().type == TokenType.COLON:
            self.next()

        # الهدف
        if self.peek().type in (TokenType.STRING, TokenType.FILE_NAME,
                                 TokenType.IDENTIFIER, TokenType.IDENTIFIER_PROP):
            target = str(self.next().value)
        else:
            target = self.read_value()

        return ast.ShowIn(text, target)


    def parse_expression_until_in(self):
        """يقرأ تعبير لحد IN — يستخدم parse_term_until_in"""
        left = self.parse_term_until_in()

        while self.peek().type in (TokenType.PLUS, TokenType.MINUS,
                                     TokenType.MULTIPLY, TokenType.DIVIDE,
                                     TokenType.MODULO):
            op = self.next()
            right = self.parse_term_until_in()
            op_str = {
                TokenType.PLUS: '+', TokenType.MINUS: '-',
                TokenType.MULTIPLY: '*', TokenType.DIVIDE: '/',
                TokenType.MODULO: '%'
            }.get(op.type, '+')
            left = ast.BinOp(left, op_str, right)

        return left


    def parse_term_until_in(self):
        """يقرأ حد واحد بدون تعدي IN"""
        t = self.peek()

        # Date/Time
        if t.type in (TokenType.NOW, TokenType.TODAY):
            func = str(t.value)
            self.next()
            # تجاهل ()
            if self.peek().type == TokenType.LPAREN:
                self.next()
                if self.peek().type == TokenType.RPAREN:
                    self.next()
            return ast.DateCall(func)

        # طول() — لازم تكون قبل STRING
        if t.type == TokenType.LENGTH:
            self.next()
            if self.peek().type == TokenType.LPAREN:
                self.next()
            arg = self.parse_term_until_in()
            if self.peek().type == TokenType.RPAREN:
                self.next()
            return ast.FunctionCall('طول', [arg])

        # قائمة [1, 2, 3]
        if t.type == TokenType.LBRACKET:
            return self.parse_list()

        # قاموس {k: v}
        if t.type == TokenType.LBRACE:
            return self.parse_dict()

        if t.type == TokenType.BOOLEAN:
            self.next()
            return ast.Bool(bool(t.value))

        if t.type == TokenType.NUMBER:
            return ast.Number(self.next().value)

        if t.type == TokenType.STRING:
            return ast.String(str(self.next().value))

        # متغير (IDENTIFIER) → VarRef + دعم الفهرسة
        # دوال مدمجة: رتب، اعكس، أول، آخر، رقم، نص، قسم، استبدل، اقتطع
        if t.type in (TokenType.SORT, TokenType.REVERSE, TokenType.FIRST,
                      TokenType.LAST, TokenType.TO_NUM, TokenType.TO_STR,
                      TokenType.SPLIT, TokenType.REPLACE, TokenType.SUBSTR,
                      TokenType.SQRT, TokenType.POWER, TokenType.RANDOM,
                      TokenType.ROUND, TokenType.CONTAINS, TokenType.STARTS_WITH,
                      TokenType.ENDS_WITH, TokenType.TRIM):
            func_name = str(t.value)
            self.next()
            args = []
            if self.peek().type == TokenType.LPAREN:
                self.next()
                while self.peek().type != TokenType.RPAREN:
                    self.skip_newlines()
                    if self.peek().type == TokenType.RPAREN:
                        break
                    args.append(self.parse_term_until_in())
                    if self.peek().type == TokenType.COMMA:
                        self.next()
                    else:
                        break
                if self.peek().type == TokenType.RPAREN:
                    self.next()
            return ast.BuiltinCall(func_name, args)

        if t.type in (TokenType.IDENTIFIER, TokenType.FILE_NAME,
                       TokenType.IDENTIFIER_PROP):
            name = str(self.next().value)
            if self.peek().type == TokenType.LPAREN:
                result = self.parse_call(name)
            else:
                result = ast.VarRef(name)
            # دعم الفهرسة والنقطة
            while True:
                if self.peek().type == TokenType.LBRACKET:
                    self.next()
                    idx = self.parse_term_until_in()
                    if self.peek().type == TokenType.RBRACKET:
                        self.next()
                    result = ast.IndexAccess(result, idx)
                elif self.peek().type == TokenType.DOT:
                    self.next()
                    if not self.peek().value:
                        break
                    attr = str(self.next().value)
                    if self.peek().type == TokenType.LPAREN:
                        self.next()
                        args = []
                        while self.peek().type != TokenType.RPAREN:
                            self.skip_newlines()
                            if self.peek().type == TokenType.RPAREN:
                                break
                            args.append(self.parse_term_until_in())
                            if self.peek().type == TokenType.COMMA:
                                self.next()
                            else:
                                break
                        if self.peek().type == TokenType.RPAREN:
                            self.next()
                        result = ast.MethodCall(result, attr, args)
                    else:
                        result = ast.MemberAccess(result, attr)
                else:
                    break
            return result

        # مش معروف
        return ast.String(str(self.next().value))


    def parse_clear(self):
        self.next()
        while self.peek().type not in (TokenType.COLON, TokenType.NEWLINE,
                                        TokenType.EOF):
            self.next()
        if self.peek().type == TokenType.COLON:
            self.next()
        if self.peek().type in (TokenType.STRING, TokenType.FILE_NAME,
                                 TokenType.IDENTIFIER):
            target = str(self.next().value)
        else:
            target = self.read_value()
        return ast.ClearIn(target)

    def parse_new_file(self):
        """أنشئ_ملفًا: ..."""
        self.next()  # NEW_FILE
        if self.peek().type == TokenType.COLON:
            self.next()
        self.skip_newlines()

        # استهلك INDENT لو موجود
        if self.peek().type == TokenType.INDENT:
            self.next()

        name = ''
        path = './'
        content = ''

        while True:
            self.skip_newlines()
            t = self.peek()

            # نهاية البلوك
            if t.type in (TokenType.DEDENT, TokenType.NEW_FILE,
                          TokenType.CREATE, TokenType.EOF, TokenType.END):
                break

            if t.type not in PROP_TOKENS:
                break

            key_token = self.next()
            key_name = str(key_token.value)

            if self.peek().type != TokenType.COLON:
                self.pos -= 1
                break

            self.next()  # :

            if key_name == 'الاسم':
                name = self.read_name_value()
            elif key_name == 'المسار':
                path = self.read_name_value()
            elif key_name == 'المحتوى':
                # تخطى NEWLINE
                while self.peek().type == TokenType.NEWLINE:
                    self.next()
                # استهلك INDENT لو موجود
                if self.peek().type == TokenType.INDENT:
                    self.next()
                # اقرأ المحتوى
                if self.peek().type == TokenType.STRING:
                    content = str(self.next().value)
                else:
                    parts = []
                    while self.peek().type not in (TokenType.NEWLINE,
                                                    TokenType.EOF,
                                                    TokenType.DEDENT):
                        parts.append(str(self.next().value))
                    content = ' '.join(parts)
                # استهلك DEDENT اللي بعد المحتوى
                while self.peek().type == TokenType.DEDENT:
                    self.next()
            else:
                self.read_value()

        # استهلك DEDENT لو موجود
        while self.peek().type == TokenType.DEDENT:
            self.next()

        return ast.CreateFile(name=name, path=path, content=content)



    def parse_create(self):
        """انشئ زر/عنوان/نص/مدخل/نافذة"""
        self.next()  # CREATE
        kind = self.next()  # WINDOW/BUTTON/TITLE/TEXT/INPUT

        if self.peek().type == TokenType.COLON:
            self.next()

        self.skip_newlines()

        # استهلك INDENT
        if self.peek().type == TokenType.INDENT:
            self.next()

        props = self.parse_props()

        # ابحث عن ON_CLICK
        self.skip_newlines()
        actions = []
        if self.peek().type == TokenType.ON_CLICK:
            self.next()
            if self.peek().type == TokenType.COLON:
                self.next()
            self.skip_newlines()
            if self.peek().type == TokenType.INDENT:
                self.next()

            while True:
                self.skip_newlines()
                t = self.peek()
                if t.type in (TokenType.DEDENT, TokenType.EOF, TokenType.END):
                    break
                if t.type == TokenType.VAR_KW:
                    actions.append(self.parse_var_decl())
                elif t.type == TokenType.SHOW:
                    actions.append(self.parse_show())
                elif t.type == TokenType.CLEAR:
                    actions.append(self.parse_clear())
                elif t.type == TokenType.IF:
                    actions.append(self.parse_if())
                elif t.type == TokenType.WHILE:
                    actions.append(self.parse_while())
                elif t.type == TokenType.FOR:
                    actions.append(self.parse_for())
                elif t.type == TokenType.FOR_INDEX:
                    actions.append(self.parse_for_index())
                elif t.type == TokenType.QR_KW:
                    actions.append(self.parse_qr())
                elif t.type == TokenType.PDF_KW:
                    actions.append(self.parse_pdf())
                elif t.type == TokenType.LOGIN:
                    actions.append(self.parse_auth_login())
                elif t.type == TokenType.LOGOUT:
                    actions.append(self.parse_auth_logout())
                elif t.type == TokenType.REGISTER:
                    actions.append(self.parse_auth_register())
                elif t.type == TokenType.WS_KW:
                    actions.append(self.parse_websocket())
                elif t.type == TokenType.MAP_KW:
                    actions.append(self.parse_map())
                elif t.type == TokenType.CHART:
                    actions.append(self.parse_chart())
                elif t.type == TokenType.ICON:
                    actions.append(self.parse_icon())
                elif t.type == TokenType.PLAY_SOUND:
                    actions.append(self.parse_play_sound())
                elif t.type == TokenType.NOTIFY:
                    actions.append(self.parse_notify())
                elif t.type == TokenType.CLIPBOARD_COPY:
                    actions.append(self.parse_clipboard_copy())
                elif t.type == TokenType.CLIPBOARD_PASTE:
                    actions.append(self.parse_clipboard_paste())
                elif t.type == TokenType.DOWNLOAD:
                    actions.append(self.parse_download())
                elif t.type == TokenType.ENABLE_DRAG:
                    actions.append(self.parse_enable_drag())
                elif t.type == TokenType.ENABLE_RESIZE:
                    actions.append(self.parse_enable_resize())
                elif t.type == TokenType.SECURE_LOGIN:
                    actions.append(self.parse_secure_login())
                elif t.type == TokenType.VIDEO_CALL:
                    actions.append(self.parse_video_call())
                elif t.type == TokenType.PUSH_NOTIFY:
                    actions.append(self.parse_push_notify())
                elif t.type == TokenType.TEMPLATE_APPLY:
                    actions.append(self.parse_template_apply())
                elif t.type == TokenType.AI_LOCAL:
                    actions.append(self.parse_ai_local())
                elif t.type == TokenType.WEB3:
                    actions.append(self.parse_web3())
                elif t.type == TokenType.GAME_3D:
                    actions.append(self.parse_scene_3d())
                elif t.type == TokenType.AR_VR:
                    actions.append(self.parse_ar_scene())
                elif t.type == TokenType.ASYNC_KW:
                    actions.append(self.parse_async())
                elif t.type == TokenType.MATCH_KW:
                    actions.append(self.parse_match())
                elif t.type == TokenType.THROW_KW:
                    actions.append(self.parse_throw())
                elif t.type == TokenType.CLASS_KW:
                    actions.append(self.parse_class())
                elif t.type == TokenType.CONST_KW:
                    actions.append(self.parse_const())
                elif t.type == TokenType.CREATE:
                    nxt = self.peek(1)
                    if nxt.type == TokenType.CHART:
                        actions.append(self.parse_chart())
                    elif nxt.type == TokenType.MAP_KW:
                        actions.append(self.parse_map())
                    elif nxt.type == TokenType.QR_KW:
                        actions.append(self.parse_qr())
                    elif nxt.type == TokenType.PDF_KW:
                        actions.append(self.parse_pdf())
                    else:
                        self.next()
                elif t.type == TokenType.CREATE:
                    # نشوف اللي بعد CREATE عشان نعرف النوع
                    nxt = self.peek(1)
                    if nxt.type == TokenType.CHART:
                        actions.append(self.parse_chart())
                    elif nxt.type == TokenType.MAP_KW:
                        actions.append(self.parse_map())
                    elif nxt.type == TokenType.QR_KW:
                        actions.append(self.parse_qr())
                    elif nxt.type == TokenType.PDF_KW:
                        actions.append(self.parse_pdf())
                    else:
                        self.next()
                elif t.type == TokenType.CHART:
                    actions.append(self.parse_chart())
                elif t.type == TokenType.RETURN:
                    actions.append(self.parse_return())
                elif t.type == TokenType.TRY:
                    actions.append(self.parse_try())
                elif t.type == TokenType.AWAIT:
                    actions.append(self.parse_await())
                elif t.type == TokenType.EVERY:
                    actions.append(self.parse_timer())
                elif t.type == TokenType.ANIMATE:
                    actions.append(self.parse_animate())
                elif t.type == TokenType.CREATE_ELEMENT:
                    actions.append(self.parse_create_element())
                elif t.type == TokenType.REMOVE_ELEMENT:
                    actions.append(self.parse_remove_element())
                elif t.type == TokenType.HTTP_GET:
                    actions.append(self.parse_http_get())
                elif t.type == TokenType.HTTP_POST:
                    actions.append(self.parse_http_post())
                elif t.type == TokenType.DB_KW:
                    actions.append(self.parse_db_create())
                elif t.type == TokenType.INSERT_KW:
                    actions.append(self.parse_db_insert())
                elif t.type == TokenType.SELECT_KW:
                    actions.append(self.parse_db_select())
                elif t.type == TokenType.ADD_ITEM:
                    actions.append(self.parse_add_item())
                elif t.type == TokenType.REMOVE_ITEM:
                    actions.append(self.parse_remove_item())
                elif t.type == TokenType.AI_ASK:
                    actions.append(self.parse_ai_ask())
                elif t.type in (TokenType.COPY, TokenType.MOVE,
                                TokenType.DELETE, TokenType.READ,
                                TokenType.SAVE, TokenType.NEW_FOLDER,
                                TokenType.OPEN):
                    actions.append(self.parse_file_op())
                elif t.type == TokenType.CREATE:
                    nxt = self.peek(1)
                    if nxt.type == TokenType.CHART:
                        actions.append(self.parse_chart())
                    elif nxt.type == TokenType.MAP_KW:
                        actions.append(self.parse_map())
                    elif nxt.type == TokenType.QR_KW:
                        actions.append(self.parse_qr())
                    elif nxt.type == TokenType.PDF_KW:
                        actions.append(self.parse_pdf())
                    else:
                        self.next()
                elif t.type in (TokenType.IDENTIFIER, TokenType.FILE_NAME,
                                TokenType.IDENTIFIER_PROP):
                    nxt = self.peek(1)
                    if nxt.type in (TokenType.EQUALS, TokenType.PLUS_EQ,
                                    TokenType.MINUS_EQ):
                        actions.append(self.parse_assign())
                    else:
                        self.next()
                else:
                    self.next()

            while self.peek().type == TokenType.DEDENT:
                self.next()

        while self.peek().type == TokenType.DEDENT:
            self.next()

        if kind.type == TokenType.WINDOW:
            return ast.CreateWindow(props)
        elif kind.type == TokenType.BUTTON:
            return ast.CreateButton(props, actions)
        elif kind.type == TokenType.TITLE:
            return ast.CreateTitle(props)
        elif kind.type == TokenType.TEXT:
            return ast.CreateText(props)
        elif kind.type == TokenType.INPUT:
            return ast.CreateInput(props)
        elif kind.type == TokenType.IMAGE:
            return ast.CreateImage(props)
        elif kind.type == TokenType.VIDEO:
            return ast.CreateVideo(props)
        elif kind.type == TokenType.GRID:
            columns = 2
            if 'الأعمدة' in props:
                try:
                    columns = int(props['الأعمدة'])
                except:
                    pass
            items = self.parse_grid_body()
            return ast.CreateGrid(props, items, columns)
        elif kind.type == TokenType.TABLE:
            headers, rows = self.parse_table_body()
            return ast.CreateTable(props, headers, rows)
        elif kind.type == TokenType.CHART:
            return ast.CreateChart(props, 'bar', [])
        elif kind.type == TokenType.FORM:
            fields, actions = self.parse_form_body()
            return ast.CreateForm(props, fields, actions)
        elif kind.type == TokenType.TABS:
            tabs = self.parse_tabs_body()
            return ast.CreateTabs(props, tabs)
        elif kind.type == TokenType.ICON:
            return ast.CreateIcon(props)
        elif kind.type == TokenType.SELECT:
            # اقرأ الخيارات
            options = []
            self.skip_newlines()
            while self.peek().type == TokenType.OPTION:
                self.next()  # خيار
                if self.peek().type == TokenType.COLON:
                    self.next()
                if self.peek().type == TokenType.STRING:
                    options.append(str(self.next().value))
                else:
                    options.append(str(self.next().value))
                self.skip_newlines()
            return ast.CreateSelect(props, options)

        elif kind.type == TokenType.NAVBAR:
            return ast.CreateNavbar(props)
        elif kind.type == TokenType.SIDEBAR:
            return ast.CreateSidebar(props)
        elif kind.type == TokenType.ACCORDION:
            return ast.CreateAccordion(props)
        elif kind.type == TokenType.MODAL:
            return ast.CreateModal(props, [])
        elif kind.type == TokenType.TOOLTIP:
            return ast.AddTooltip(props)

        raise SyntaxError(f"نوع غير مدعوم: {kind.value}")

    def parse_props(self):
        """يقرأ خصائص — يتعامل مع INDENT/DEDENT"""
        props = {}
        self.skip_newlines()

        # استهلك INDENT لو موجود
        had_indent = False
        if self.peek().type == TokenType.INDENT:
            self.next()
            had_indent = True

        while True:
            self.skip_newlines()
            t = self.peek()

            # نهاية البلوك
            if t.type in (TokenType.DEDENT, TokenType.EOF, TokenType.END):
                break

            if t.type not in PROP_TOKENS:
                break

            key_token = self.next()
            key_name = str(key_token.value)

            if self.peek().type != TokenType.COLON:
                self.pos -= 1
                break

            self.next()  # :

            value = self.read_value()
            props[key_name] = value

        # استهلك DEDENT لو موجود
        while self.peek().type == TokenType.DEDENT:
            self.next()

        return props

