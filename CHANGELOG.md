# سجل التغييرات — Changelog

كل التغييرات المهمة في لغة بيان موثّقة هنا.

الصيغة مستوحاة من [Keep a Changelog](https://keepachangelog.com/)
والمشروع يتبع [Semantic Versioning](https://semver.org/).

---

## [61.0.0] — 2026-10-06

### 🎉 الإصدار الأول الكامل

#### ✨ أُضيف

**المترجمات (Compilers):**
- Compiler → Python كامل
- Compiler → JavaScript (UI + Logic)
- Compiler → HTML/CSS/JS

**Packagers (3 أنماط):**
- A: Standalone HTML — ملف واحد يعمل في أي متصفح
- B: Python Bundle — program.py + run.sh + run.bat
- C: Python ZIPAPP — ملف .pyz قابل للتنفيذ

**المفسّر (Interpreter):**
- Interpreter كامل مع 6 ملفات
- Environment مع scope chain
- 41+ builtin
- JavaScript Runtime مستقل (localStorage)

**ميزات اللغة:**
- قواميس كاملة (literals, access, set, iterate)
- OOP كامل: فئات، وراثة، واجهات
- معالجة أخطاء: حاول/التقط/أخيرًا
- Bool (صح/غلط)
- Type Inference (أنواع اختيارية)
- Scope Management (محلي/عالمي/غير_محلي)
- Metaprogramming (انعكاس كامل)
- Memory Management (حجم، نسخ، تحرير)

**المكتبة القياسية (12 وحدة):**
- رياضيات، نصوص، قوائم، قواميس
- ملفات، شبكة، وقت، عشوائي
- JSON، CSV، تشفير، نظام

**الأوامر (CLI):**
- نفّذ، ولّد، ابنِ، شغّل، اختبر
- مكتبة، استورد، تفاعل، تتبّع
- قِس، راقب، وثّق، سيرفر

**التوثيق:**
- README.md شامل
- LICENSE (GPL-3.0)
- CHANGELOG.md
- CONTRIBUTING.md

#### 🔧 تغييرات

- إزالة API Server (127.0.0.1:5000)
- JavaScript standalone 100%
- دعم TemplateString في JS
- الدوال Byan → JavaScript functions

#### 🐛 إصلاحات

**تعارضات الكلمات المفتاحية:**
- اعرض → builtin، اعرض_في → keyword
- أضف → builtin، أضف_عنصر → keyword
- قائمة → متاح كمتغير
- نص → متاح كمتغير
- رقم → متاح كمتغير
- فئة → alias لـ صنف

**aliases جديدة:**
- إذا، اذا، إن، والا
- التقط، أخيرًا، اخيرا
- ارمِ_خطأ، ارمِ_غلطة

**إصلاحات Parser:**
- parse_function DEDENT
- else_body
- If في parse
- TABLE_KW
- _handle_function_call للـ nested functions

---

## [50.0.0] — 2026-10-06

### الأساس

- 74 ميزة UI
- Lexer + Parser + AST
- Targets: HTML، PWA، EXE
- Runtime APIs

---

## [10.0.0] — 2026-10-05

### الإصدارات الأولى

- نظام lexer/parser أساسي
- أول أمثلة UI

---

**حقوق النشر (C) 2026 حسام حسن محمد حسن عبيد**
