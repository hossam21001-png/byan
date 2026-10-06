from dataclasses import dataclass, field
from typing import Any, List


@dataclass
class Program:
    name: str = ""
    purpose: str = ""
    ui_file: str = ""
    database: str = ""
    os: str = "الكل"
    target: str = "تطبيق"
    elements: List[Any] = field(default_factory=list)


@dataclass
class CreateWindow:
    props: dict = field(default_factory=dict)


@dataclass
class CreateButton:
    props: dict = field(default_factory=dict)
    actions: List[Any] = field(default_factory=list)


@dataclass
class CreateTitle:
    props: dict = field(default_factory=dict)


@dataclass
class CreateText:
    props: dict = field(default_factory=dict)


@dataclass
class CreateInput:
    props: dict = field(default_factory=dict)


@dataclass
class CreateFile:
    name: str = ""
    path: str = "./"
    content: str = ""


@dataclass
class ActivateButton:
    selector: str = ""
    actions: List[Any] = field(default_factory=list)


@dataclass
class ShowIn:
    text: Any = ""      # ممكن نص أو تعبير
    target: str = ""


@dataclass
class ClearIn:
    target: str = ""


# ===== جديد: المتغيرات والمنطق =====

@dataclass
class VarDecl:
    """متغير س = 5"""
    name: str = ""
    value: Any = None


@dataclass
class LocalDecl:
    """محلي س = 5 — متغير محلي"""
    name: str = ""
    value: Any = None


@dataclass
class GlobalDecl:
    """عالمي س = 5 — متغير عام"""
    name: str = ""
    value: Any = None


@dataclass
class NonlocalDecl:
    """غير_محلي س — يشير لمتغير الأب"""
    name: str = ""


@dataclass
class BinOp:
    """عملية حسابية: 5 + 3"""
    left: Any = None
    op: str = ""
    right: Any = None


@dataclass
class Number:
    value: float = 0


@dataclass
class Bool:
    """صح / غلط"""
    value: bool = False

@dataclass
class String:
    value: str = ""


@dataclass
class VarRef:
    """الإشارة لمتغير"""
    name: str = ""


@dataclass
class If:
    """لو الشرط: ... وإلا: ..."""
    condition: Any = None
    then_body: List[Any] = field(default_factory=list)
    else_body: List[Any] = field(default_factory=list)


@dataclass
class Compare:
    """مقارنة: س > 5"""
    left: Any = None
    op: str = ""
    right: Any = None


# ===== الحلقات =====

@dataclass
class While:
    """طالما الشرط: ..."""
    condition: Any = None
    body: List[Any] = field(default_factory=list)


@dataclass
class ForIn:
    """لكل س في [1، 2، 3]: ..."""
    var_name: str = ""
    iterable: Any = None
    body: List[Any] = field(default_factory=list)


@dataclass
class ListLiteral:
    """[1، 2، 3، 4]"""
    items: List[Any] = field(default_factory=list)


@dataclass
class DictLiteral:
    """{اسم: علي، عمر: 25}"""
    pairs: List[Any] = field(default_factory=list)  # [(key, value), ...]


@dataclass
class DictAccess:
    """قاموس[مفتاح]"""
    dict_expr: Any = None
    key: Any = None


@dataclass
class DictSet:
    """قاموس[مفتاح] = قيمة"""
    dict_expr: Any = None
    key: Any = None
    value: Any = None


@dataclass
class ForDict:
    """لكل مفتاح, قيمة في قاموس: ..."""
    key_name: str = ""
    val_name: str = ""
    dict_expr: Any = None
    body: List[Any] = field(default_factory=list)


@dataclass
class CompoundAssign:
    """س += 1"""
    name: str = ""
    op: str = ""
    value: Any = None


@dataclass
class AddAssign:
    """زي CompoundAssign"""
    name: str = ""
    value: Any = None


@dataclass
class Assign:
    """س = 5 (إسناد بدون تعريف)"""
    name: str = ""
    value: Any = None


# ===== الدوال =====

@dataclass
class FunctionDef:
    """دالة اسم(معاملات): جسم"""
    name: str = ""
    params: List[str] = field(default_factory=list)
    body: List[Any] = field(default_factory=list)


@dataclass
class FunctionCall:
    """اسم(args)"""
    name: str = ""
    args: List[Any] = field(default_factory=list)


@dataclass
class Return:
    """ارجع قيمة"""
    value: Any = None


# ===== عمليات الملفات والنظام =====

@dataclass
class FileOp:
    """عملية على ملف: انسخ، انقل، احذف"""
    op: str = ""           # copy, move, delete, read, write, mkdir
    source: str = ""       # المصدر
    target: str = ""       # الهدف (لو موجود)
    content: str = ""      # المحتوى (للكتابة)


@dataclass
class SysCall:
    """استدعاء API/أمر خارجي"""
    api: str = ""          # نوع الـ API (file, system, http)
    method: str = ""       # العملية
    args: dict = field(default_factory=dict)
    result_var: str = ""   # متغير لحفظ الناتج


@dataclass
class Break:
    """توقف — يخرج من الحلقة"""
    pass


@dataclass
class Continue:
    """استمر — يتخطى الدورة الحالية"""
    pass


@dataclass
class Array2D:
    """مصفوفة متعددة الأبعاد [[1,2],[3,4]]"""
    rows: List[Any] = field(default_factory=list)


@dataclass
class IndexAccess:
    """مصفوفة[0] أو مصفوفة[0][1]"""
    target: Any = None
    index: Any = None


@dataclass
class Lambda:
    """دالة مجهولة: (س) => س * 2"""
    params: List[str] = field(default_factory=list)
    body: Any = None


@dataclass
class ArrayAdd:
    """أضف(قائمة, عنصر)"""
    target: Any = None
    item: Any = None


@dataclass
class ArrayRemove:
    """احذف(قائمة, فهرس)"""
    target: Any = None
    index: Any = None


@dataclass
class CreateImage:
    """صورة"""
    props: dict = field(default_factory=dict)


@dataclass
class CreateVideo:
    """فيديو"""
    props: dict = field(default_factory=dict)


@dataclass
class CreateSelect:
    """قائمة منسدلة"""
    props: dict = field(default_factory=dict)
    options: List[str] = field(default_factory=list)


@dataclass
class AiAsk:
    """اسأل الذكاء_الاصطناعي"""
    prompt: str = ""
    target: str = ""


@dataclass
class DbCreate:
    """انشئ قاعدة_بيانات "name.db" """
    name: str = ""


@dataclass
class DbTable:
    """جدول "users" فيه أعمدة: [name, age]"""
    name: str = ""
    columns: List[str] = field(default_factory=list)


@dataclass
class DbInsert:
    """أضف_سجل "users" فيه {name: "احمد"}"""
    table: str = ""
    values: dict = field(default_factory=dict)


@dataclass
class DbSelect:
    """اقرأ_سجلات "users" في: "#out" """
    table: str = ""
    target: str = ""


@dataclass
class Timer:
    """كل 2 ثانية: ..."""
    seconds: float = 1.0
    body: List[Any] = field(default_factory=list)


@dataclass
class Animate:
    """حرّك "#box" إلى (100, 200) في: 2 ثانية"""
    selector: str = ""
    x: int = 0
    y: int = 0
    duration: float = 1.0


@dataclass
class CreateElement:
    """ضيف_عنصر "div" في "#container" """
    tag: str = ""
    target: str = ""
    content: str = ""
    el_id: str = ""


@dataclass
class RemoveElement:
    """امسح_عنصر "#id" """
    selector: str = ""


@dataclass
class HttpGet:
    """اتصل "url" في: "#out" """
    url: str = ""
    target: str = ""


@dataclass
class HttpPost:
    """ارسل "url" ببيانات {...} """
    url: str = ""
    data: dict = field(default_factory=dict)


@dataclass
class Try:
    """حاول: ... لو_فشل: ..."""
    body: List[Any] = field(default_factory=list)
    catch_body: List[Any] = field(default_factory=list)
    error_var: str = ""


@dataclass
class Await:
    """انتظر: ... (ينفذ بالترتيب)"""
    body: List[Any] = field(default_factory=list)


@dataclass
class NullLit:
    """لا_شيء"""
    pass


@dataclass
class TemplateString:
    """نص مع متغيرات: أهلاً يا {اسم}"""
    parts: List[Any] = field(default_factory=list)


@dataclass
class BuiltinCall:
    """دالة داخلية: رتب(قائمة), أول(قائمة)"""
    name: str = ""
    args: List[Any] = field(default_factory=list)


@dataclass
class CreateGrid:
    """شبكة"""
    props: dict = field(default_factory=dict)
    items: List[Any] = field(default_factory=list)
    columns: int = 2


@dataclass
class CreateTable:
    """جدول"""
    props: dict = field(default_factory=dict)
    headers: List[str] = field(default_factory=list)
    rows: List[Any] = field(default_factory=list)

@dataclass
class CreateChart:
    """رسم بياني"""
    props: dict = field(default_factory=dict)
    chart_type: str = "bar"
    data: List[Any] = field(default_factory=list)


@dataclass
class CreateForm:
    """نموذج"""
    props: dict = field(default_factory=dict)
    fields: List[dict] = field(default_factory=list)
    actions: List[Any] = field(default_factory=list)


@dataclass
class CreateTabs:
    """تبويبات"""
    props: dict = field(default_factory=dict)
    tabs: List[Any] = field(default_factory=list)

@dataclass
class Import:
    """استورد "file.byan" """
    file_path: str = ""


@dataclass
class InputAsk:
    """اسأل_المستخدم "..." """
    prompt: str = ""


@dataclass
class ForIndex:
    """لكل_بفهرس i, عنصر في القائمة: ..."""
    idx_name: str = ""
    var_name: str = ""
    iterable: Any = None
    body: List[Any] = field(default_factory=list)


@dataclass
class CreateQr:
    """qr "..." """
    content: str = ""
    size: int = 200


@dataclass
class CreatePdf:
    """ملف PDF"""
    title: str = ""
    content: Any = None
    filename: str = "document.pdf"


@dataclass
class AuthAction:
    """مصادقة: تسجيل دخول/خروج/حساب"""
    action: str = ""
    username: str = ""
    password: str = ""


@dataclass
class WebSocketConnect:
    """اتصال_مباشر "url" """
    url: str = ""


@dataclass
class CreateMap:
    """خريطة"""
    props: dict = field(default_factory=dict)
    lat: float = 0
    lng: float = 0
    zoom: int = 12


@dataclass
class CreateIcon:
    """أيقونة"""
    props: dict = field(default_factory=dict)


@dataclass
class PlaySound:
    """شغل صوت "url" """
    url: str = ""


@dataclass
class Notify:
    """أظهر إشعار "نص" """
    title: str = ""
    body: str = ""


@dataclass
class ClipboardCopy:
    """انسخ للحافظة "نص" """
    text: str = ""


@dataclass
class ClipboardPaste:
    """الصق"""
    target: str = ""


@dataclass
class Download:
    """حمل "url" """
    url: str = ""
    filename: str = ""


@dataclass
class EnableDrag:
    """فعّل سحب عنصر"""
    selector: str = ""


@dataclass
class EnableResize:
    """فعّل تحجيم عنصر"""
    selector: str = ""


@dataclass
class DarkMode:
    """وضع ليلي"""
    mode: str = "auto"


@dataclass
class Language:
    """اللغة"""
    lang: str = "ar"


@dataclass
class SecureLogin:
    """تسجيل دخول آمن"""
    username: str = ""
    password: str = ""


@dataclass
class PayButton:
    """زر دفع"""
    props: dict = field(default_factory=dict)
    amount: float = 0
    currency: str = "USD"
    actions: List[Any] = field(default_factory=list)


@dataclass
class VideoCall:
    """مكالمة فيديو"""
    room: str = ""


@dataclass
class PushNotify:
    """طلب إشعارات push"""
    pass


@dataclass
class CodeEditor:
    """محرر أكواد"""
    props: dict = field(default_factory=dict)


@dataclass
class TemplateApply:
    """تطبيق قالب"""
    template: str = ""
    target: str = ""


@dataclass
class AiLocal:
    """اسأل AI محلي"""
    prompt: str = ""
    target: str = ""


@dataclass
class Web3Connect:
    """اتصل محفظة"""
    network: str = ""


@dataclass
class Scene3D:
    """مشهد 3D"""
    props: dict = field(default_factory=dict)


@dataclass
class ArScene:
    """مشهد AR"""
    props: dict = field(default_factory=dict)


@dataclass
class Generator:
    """مولد - Generator"""
    name: str = ""
    body: List[Any] = field(default_factory=list)


@dataclass
class YieldValue:
    """حاصل"""
    value: Any = None


@dataclass
class AsyncFunc:
    """دالة غير متزامنة"""
    name: str = ""
    params: List[str] = field(default_factory=list)
    body: List[Any] = field(default_factory=list)


@dataclass
class AwaitExpr:
    """انتظر_وعد"""
    expr: Any = None


@dataclass
class ClassDef:
    """صنف"""
    name: str = ""
    extends: str = ""
    methods: List[Any] = field(default_factory=list)
    fields: List[Any] = field(default_factory=list)


@dataclass
class NewInstance:
    """جديد صنف(وسائط)"""
    class_name: str = ""
    args: List[Any] = field(default_factory=list)


@dataclass
class MemberAccess:
    """هذا.اسم أو كائن.خاصية"""
    obj: Any = None
    attr: str = ""


@dataclass
class MemberSet:
    """هذا.اسم = قيمة"""
    obj: Any = None
    attr: str = ""
    value: Any = None


@dataclass
class MethodCall:
    """كائن.دالة(وسائط)"""
    obj: Any = None
    method: str = ""
    args: List[Any] = field(default_factory=list)


@dataclass
class InterfaceDef:
    """واجهة"""
    name: str = ""
    methods: List[str] = field(default_factory=list)


@dataclass
class MatchCase:
    """طابق / حالة"""
    value: Any = None
    body: List[Any] = field(default_factory=list)


@dataclass
class Match:
    """طابق ... مع"""
    expr: Any = None
    cases: List[Any] = field(default_factory=list)


@dataclass
class ThrowError:
    """ارمِ خطأ"""
    message: str = ""


@dataclass
class TryCatchFinally:
    """حاول/التقط/أخيراً"""
    body: List[Any] = field(default_factory=list)
    catch_body: List[Any] = field(default_factory=list)
    finally_body: List[Any] = field(default_factory=list)


@dataclass
class ConstDecl:
    """ثابت س = 5"""
    name: str = ""
    value: Any = None
    type_hint: str = ""


@dataclass
class TypeDecl:
    """متغير س: رقم = 5"""
    name: str = ""
    type_hint: str = ""
    value: Any = None


@dataclass
class NullCoalesce:
    """أ ؟؟ ب"""
    left: Any = None
    right: Any = None


@dataclass
class NullCheck:
    """فحص null"""
    expr: Any = None


@dataclass
class DateCall:
    """الآن() أو اليوم()"""
    func: str = ""


@dataclass
class CreateModal:
    """نافذة منبثقة"""
    props: dict = field(default_factory=dict)
    actions: List[Any] = field(default_factory=list)


@dataclass
class AddTooltip:
    """تلميح"""
    props: dict = field(default_factory=dict)


@dataclass
class CreateAccordion:
    """قائمة طي"""
    props: dict = field(default_factory=dict)


@dataclass
class CreateSidebar:
    """شريط جانبي"""
    props: dict = field(default_factory=dict)


@dataclass
class CreateNavbar:
    """شريط تنقل"""
    props: dict = field(default_factory=dict)
