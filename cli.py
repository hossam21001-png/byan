# -*- coding: utf-8 -*-
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from byan.lexer import Lexer
from byan.parser import Parser
from byan.targets.python_app import PythonAppTarget


def cmd_install(package):
    """تنصيب مكتبة"""
    import urllib.request
    packages_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'packages')
    os.makedirs(packages_dir, exist_ok=True)

    # لو محلي
    if os.path.exists(package):
        import shutil
        name = os.path.basename(package).replace('.byan', '')
        dest = os.path.join(packages_dir, name + '.byan')
        shutil.copy(package, dest)
        print(f"✅ تم تنصيب {name} محليًا")
        return

    # لو من GitHub
    if package.startswith('http') or '/' in package:
        url = package if package.startswith('http') else f'https://raw.githubusercontent.com/{package}/main/lib.byan'
        try:
            name = package.split('/')[-1]
            dest = os.path.join(packages_dir, name + '.byan')
            urllib.request.urlretrieve(url, dest)
            print(f"✅ تم تنصيب {name} من الإنترنت")
        except Exception as e:
            print(f"❌ فشل التنصيب: {e}")
        return

    print(f"❌ لم أجد الحزمة: {package}")


def cmd_test(tests_dir):
    """تشغيل الاختبارات"""
    if not os.path.exists(tests_dir):
        print(f"❌ المجلد مش موجود: {tests_dir}")
        return

    test_files = [f for f in os.listdir(tests_dir) if f.endswith('.byan')]
    if not test_files:
        print("⚠️  مفيش ملفات اختبار")
        return

    passed = 0
    failed = 0

    for tf in test_files:
        path = os.path.join(tests_dir, tf)
        print(f"🧪 جاري اختبار: {tf}")
        try:
            with open(path, 'r', encoding='utf-8') as f:
                source = f.read()
            tokens = Lexer(source).tokenize()
            program = Parser(tokens).parse()
            # نفذ بسيط
            print(f"   ✅ نجح")
            passed += 1
        except Exception as e:
            print(f"   ❌ فشل: {e}")
            failed += 1

    print(f"\n📊 النتيجة: {passed} نجح، {failed} فشل")


def cmd_debug(file_path):
    """تشغيل step by step"""
    if not os.path.exists(file_path):
        print(f"❌ الملف مش موجود: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        source = f.read()

    print("🐛 بدء التصحيح...")
    print()

    # قسّم لأسطر
    lines = source.split('\n')
    for i, line in enumerate(lines, 1):
        if not line.strip():
            continue
        print(f"[{i}] {line}")
        try:
            # حلل السطر
            tokens = Lexer(line + '\n').tokenize()
            print(f"     توكنز: {len(tokens)}")
        except Exception as e:
            print(f"     ❌ خطأ: {e}")

    print()
    print("✅ انتهى التصحيح")


def cmd_profile(file_path):
    """قياس الأداء"""
    import time
    if not os.path.exists(file_path):
        print(f"❌ الملف مش موجود: {file_path}")
        return

    print("📊 قياس الأداء...")
    print()

    with open(file_path, 'r', encoding='utf-8') as f:
        source = f.read()

    # قياس كل مرحلة
    t0 = time.time()
    tokens = Lexer(source).tokenize()
    t1 = time.time()
    print(f"🔤 التحليل اللغوي: {t1-t0:.4f}s ({len(tokens)} توكن)")

    program = Parser(tokens).parse()
    t2 = time.time()
    print(f"🌳 بناء الشجرة: {t2-t1:.4f}s ({len(program.elements)} عنصر)")

    target = PythonAppTarget(output_dir='./build_profile')
    result = target.generate(program)
    t3 = time.time()
    print(f"⚙️  توليد الكود: {t3-t2:.4f}s ({len(result['files'])} ملف)")

    print()
    print(f"⏱️  المجموع: {t3-t0:.4f}s")

    # نظف
    import shutil
    shutil.rmtree('./build_profile', ignore_errors=True)


def cmd_module(file_path):
    """تحليل المكتبات المستخدمة"""
    if not os.path.exists(file_path):
        print(f"❌ الملف مش موجود: {file_path}")
        return

    print("📦 تحليل المكتبات...")
    with open(file_path, 'r', encoding='utf-8') as f:
        source = f.read()

    # ابحث عن استورد
    import re
    imports = re.findall(r'استورد\s+"([^"]+)"', source)
    if imports:
        print(f"   المكتبات المستخدمة: {imports}")
    else:
        print("   مفيش مكتبات")


# =====================
# أوامر عربية (aliases)
# =====================
AR_ALIASES = {
    # أمر → إنجليزي
    'ولّد': 'gen',           # توليد
    'ولد': 'gen',
    'ابنِ': 'build_all',     # ← الجديد A+B+C
    'ابني': 'build_all',
    'شغّل': 'run',           # run
    'شغل': 'run',
    'نفّذ': 'exec',          # ← جديد: interpreter
    'نفذ': 'exec',
    'اختبر': 'test',         # test
    'تتبّع': 'debug',        # debug
    'تتبع': 'debug',
    'قِس': 'profile',        # profile
    'قس': 'profile',
    'مكتبة': 'stdlib',       # stdlib
    'تفاعل': 'repl',         # repl
    'راقب': 'watch',         # watch
    'وثّق': 'docs',          # docs
    'سيرفر': 'server',       # server
    'خادم': 'server',
    'استورد': 'install',     # install
    'ثبّت': 'install',
    'ثبت': 'install',
    'مساعده': 'help',
    'مساعدة': 'help',
}


def cmd_exec(file_path):
    """ينفذ ملف .byan بالinterpreter مباشرة"""
    if not os.path.exists(file_path):
        print(f"❌ الملف مش موجود: {file_path}")
        return

    try:
        from byan.interpreter import Interpreter
        from byan.interpreter.errors import ByanRuntimeError
    except ImportError as e:
        print(f"❌ فشل استيراد الinterpreter: {e}")
        print("   تأكد إن مجلد byan/interpreter موجود")
        return

    print("🔤 تحليل لغوي...")
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()

    tokens = Lexer(source).tokenize()
    print(f"   ✅ {len(tokens)} توكن")

    print("🌳 بناء الشجرة...")
    program = Parser(tokens).parse()
    print(f"   ✅ البرنامج: {program.name or '(بدون اسم)'}")

    print("📥 معالجة الاستيراد...")
    base_dir = os.path.dirname(os.path.abspath(file_path))
    program = _load_imports(program, base_dir)

    print()
    print("=" * 50)
    print("🎬 التنفيذ:")
    print("=" * 50)
    interp = Interpreter()
    try:
        interp.run(program)
    except ByanRuntimeError as e:
        print(f"❌ خطأ وقت التنفيذ: {e}")
        return
    print("=" * 50)
    print("✅ انتهى التنفيذ")


def _normalize_command(cmd):
    """يحوّل الأوامر العربية للإنجليزية"""
    if cmd in AR_ALIASES:
        return AR_ALIASES[cmd]
    return cmd


def _show_help():
    """يعرض المساعدة"""
    print("الاستخدام:")
    print()
    print("📌 توليد واجهات:")
    print("  python cli.py <ملف.byan>          # توليد HTML")
    print("  python cli.py ولّد <ملف.byan>     # نفس الحاجة بالعربي")
    print("  python cli.py build <ملف.byan>    # بناء EXE")
    print("  python cli.py ابنِ <ملف.byan>     # بالعربي")
    print()
    print("📌 تنفيذ مباشر:")
    print("  python cli.py نفّذ <ملف.byan>     # 🆕 interpreter مباشر")
    print("  python cli.py run <ملف.byan>      # توليد + تشغيل")
    print("  python cli.py شغّل <ملف.byan>     # بالعربي")
    print()
    print("📌 أدوات:")
    print("  python cli.py اختبر <folder>      # اختبارات")
    print("  python cli.py تتبّع <ملف>         # debug")
    print("  python cli.py قِس <ملف>           # profile")
    print("  python cli.py مكتبة               # stdlib")
    print("  python cli.py استورد <pkg>        # تنصيب")
    print("  python cli.py سيرفر               # API server")
    print("  python cli.py تفاعل               # REPL")
    print("  python cli.py راقب <ملف>          # watch")
    print("  python cli.py وثّق                # docs")


def cmd_build_all(file_path, mode='all', output_dir=None):
    """يبني كل المخرجات (HTML + Python + pyz)
    
    mode:
      'ويب' أو 'html' → A فقط
      'python' أو 'py' → B فقط
      'pyz' → C فقط
      'الكل' أو 'all' → A + B + C
    """
    import os
    from byan.lexer import Lexer
    from byan.parser import Parser
    from byan.targets.python_app import PythonAppTarget
    from byan.compilers import compile_to_python
    from byan.compilers.packagers import (
        StandaloneHtmlPackager,
        PythonBundlePackager,
        PyzPackager,
    )

    if not os.path.exists(file_path):
        print(f"❌ الملف مش موجود: {file_path}")
        return

    byan_root = os.path.dirname(os.path.abspath(__file__))
    base_name = os.path.splitext(os.path.basename(file_path))[0]

    print("=" * 60)
    print(f"🏗️  بناء: {file_path}")
    print(f"📦 الوضع: {mode}")
    print("=" * 60)
    print()

    # 1. Lexer + Parser
    print("🔤 تحليل لغوي...")
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()
    tokens = Lexer(source).tokenize()
    print(f"   ✅ {len(tokens)} توكن")

    print("🌳 بناء الشجرة...")
    program = Parser(tokens).parse()
    print(f"   ✅ {len(program.elements)} عنصر")
    print()

    # 2. build (HTML/JS)
    BUILD = os.path.join(byan_root, '_build_cache', base_name)
    if os.path.exists(BUILD):
        import shutil
        shutil.rmtree(BUILD)
    os.makedirs(BUILD)

    print("🔨 توليد HTML/JS...")
    target = PythonAppTarget(output_dir=BUILD)
    result = target.generate(program)
    print(f"   ✅ {len(result['files'])} ملف")
    print()

    # 3. Python Source
    print("🐍 توليد Python Source...")
    py_source = compile_to_python(program, mode='split')
    print(f"   ✅ {len(py_source)} حرف")
    print()

    # 4. المخرجات
    output_root = output_dir or os.path.join(byan_root, 'output')
    os.makedirs(output_root, exist_ok=True)

    modes_to_build = []
    if mode in ('الكل', 'all'):
        modes_to_build = ['html', 'python', 'pyz']
    elif mode in ('ويب', 'html'):
        modes_to_build = ['html']
    elif mode in ('python', 'py'):
        modes_to_build = ['python']
    elif mode == 'pyz':
        modes_to_build = ['pyz']
    else:
        print(f"⚠️ وضع غير معروف: {mode}")
        modes_to_build = ['html']

    results = {}

    # A: HTML
    if 'html' in modes_to_build:
        print("=" * 60)
        print("📦 A: Standalone HTML")
        print("=" * 60)
        A_OUT = os.path.join(output_root, f"{base_name}.html")
        packager = StandaloneHtmlPackager(BUILD)
        r = packager.package(output_path=A_OUT)
        results['html'] = r
        print(f"   ✅ {r['output']}")
        print(f"   📏 {r['size']:,} bytes")
        print()

    # B: Python Bundle
    if 'python' in modes_to_build:
        print("=" * 60)
        print("📦 B: Python Bundle")
        print("=" * 60)
        B_OUT = os.path.join(output_root, f"{base_name}_py")
        packager = PythonBundlePackager(BUILD, byan_root)
        r = packager.package(output_dir=B_OUT, program_source=py_source)
        results['python'] = r
        print(f"   ✅ {r['output']}")
        print(f"   📏 {r['size']:,} bytes")
        print()

    # C: .pyz
    if 'pyz' in modes_to_build:
        print("=" * 60)
        print("📦 C: .pyz")
        print("=" * 60)
        C_OUT = os.path.join(output_root, f"{base_name}.pyz")
        packager = PyzPackager(BUILD, byan_root)
        r = packager.package(output_path=C_OUT, program_source=py_source)
        results['pyz'] = r
        print(f"   ✅ {r['output']}")
        print(f"   📏 {r['size']:,} bytes")
        print()

    # ملخص
    print("=" * 60)
    print("🎉 تم البناء بنجاح!")
    print("=" * 60)
    print(f"   📁 المجلد: {output_root}")
    print()
    for k, v in results.items():
        print(f"   • {k}: {os.path.basename(v['output'])}")
    print()
    return results


def main():
    if len(sys.argv) < 2:
        _show_help()
        sys.exit(1)

    # ترجمة الأمر لو عربي
    raw_cmd = sys.argv[1]
    if raw_cmd in AR_ALIASES:
        sys.argv[1] = AR_ALIASES[raw_cmd]

    # مساعدة
    if raw_cmd in ('help', 'مساعدة', 'مساعده'):
        _show_help()
        return

    # أمر ابنِ (بناء متعدد)
    if sys.argv[1] in ('build_all', 'ابنِ', 'ابني'):
        if len(sys.argv) < 3:
            print("❌ محتاج ملف .byan")
            print("   python cli.py ابنِ <ملف.byan> [--وضع=ويب|python|pyz|الكل]")
            sys.exit(1)
        file_path = sys.argv[2]
        # استخرج الوضع
        mode = 'الكل'
        for arg in sys.argv[3:]:
            if arg.startswith('--وضع='):
                mode = arg.split('=', 1)[1]
        cmd_build_all(file_path, mode=mode)
        return

    # أمر نفّذ (interpreter)
    if sys.argv[1] == 'exec':
        if len(sys.argv) < 3:
            print("❌ محتاج ملف .byan")
            print("   python cli.py نفّذ <ملف.byan>")
            sys.exit(1)
        cmd_exec(sys.argv[2])
        return

    # أمر توليد (بعد الترجمة العربية)
    if sys.argv[1] == 'gen':
        if len(sys.argv) < 3:
            print("❌ محتاج ملف .byan")
            print("   python cli.py ولّد <ملف.byan>")
            sys.exit(1)
        fp = sys.argv[2]
        if not os.path.exists(fp):
            print(f"❌ الملف غير موجود: {fp}")
            sys.exit(1)
        _generate(fp)
        return


    # أوامر جديدة
    if sys.argv[1] == 'install':
        if len(sys.argv) < 3:
            print("❌ محتاج اسم الحزمة")
            sys.exit(1)
        cmd_install(sys.argv[2])
        return

    if sys.argv[1] == 'test':
        folder = sys.argv[2] if len(sys.argv) > 2 else './tests'
        cmd_test(folder)
        return

    if sys.argv[1] == 'debug':
        if len(sys.argv) < 3:
            print("❌ محتاج ملف .byan")
            sys.exit(1)
        cmd_debug(sys.argv[2])
        return

    if sys.argv[1] == 'profile':
        if len(sys.argv) < 3:
            print("❌ محتاج ملف .byan")
            sys.exit(1)
        cmd_profile(sys.argv[2])
        return

    if sys.argv[1] == 'stdlib':
        action = sys.argv[2] if len(sys.argv) > 2 else 'list'
        name = sys.argv[3] if len(sys.argv) > 3 else None
        cmd_stdlib(action, name)
        return

    if sys.argv[1] == 'repl':
        cmd_repl()
        return

    if sys.argv[1] == 'watch':
        if len(sys.argv) < 3:
            print("❌ محتاج ملف .byan")
            sys.exit(1)
        cmd_watch(sys.argv[2])
        return

    if sys.argv[1] == 'docs':
        folder = sys.argv[2] if len(sys.argv) > 2 else './examples'
        cmd_docs(folder)
        return

    # API Server
    if sys.argv[1] == 'server':
        from byan.runtime.api_server import start_server
        start_server()
        return

    # بناء EXE
    if sys.argv[1] == 'build':
        if len(sys.argv) < 3:
            print("❌ محتاج ملف .byan")
            sys.exit(1)
        file_path = sys.argv[2]
        name = os.path.splitext(os.path.basename(file_path))[0]

        # ولّد الأول
        _generate(file_path)

        # بعدين EXE
        from byan.targets.exe_packager import ExePackager
        packager = ExePackager(build_dir='./build', name=name)
        packager.package()
        return

    # تشغيل
    if sys.argv[1] == 'run':
        if len(sys.argv) < 3:
            print("❌ محتاج ملف .byan")
            sys.exit(1)
        _generate(sys.argv[2])
        os.system('cd build && python run.py')
        return

    # توليد عادي
    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"❌ الملف غير موجود: {file_path}")
        sys.exit(1)

    _generate(file_path)


def _load_imports(program, base_dir):
    """يحمل ملفات الاستيراد ويدمجها"""
    import os
    from byan import ast_nodes as ast

    final_elements = []
    for el in program.elements:
        if isinstance(el, ast.Import):
            import_path = el.file_path
            if not os.path.isabs(import_path):
                import_path = os.path.join(base_dir, import_path)
            if not os.path.exists(import_path):
                print(f"   ⚠️  استيراد مفقود: {import_path}")
                continue
            print(f"   📥 استيراد: {os.path.basename(import_path)}")
            with open(import_path, 'r', encoding='utf-8') as f:
                imp_src = f.read()
            imp_tokens = Lexer(imp_src).tokenize()
            imp_program = Parser(imp_tokens).parse()
            # أضف عناصر الملف المستورد (ما عدا CreateWindow/Title)
            for imp_el in imp_program.elements:
                if isinstance(imp_el, (ast.CreateWindow, ast.CreateTitle,
                                        ast.Import)):
                    continue
                final_elements.append(imp_el)
        else:
            final_elements.append(el)

    program.elements = final_elements
    return program


def cmd_stdlib(action, name=None):
    """إدارة المكتبة القياسية"""
    stdlib_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stdlib')

    if action == 'list':
        print("📚 المكتبة القياسية:")
        if os.path.exists(stdlib_dir):
            for f in os.listdir(stdlib_dir):
                if f.endswith('.byan'):
                    print(f"   • {f}")
        else:
            print("   ⚠️  مجلد stdlib مش موجود")
        return

    if action == 'use':
        if not name:
            print("❌ محتاج اسم المكتبة")
            return
        file_path = os.path.join(stdlib_dir, name + '.byan')
        if not os.path.exists(file_path):
            print(f"❌ المكتبة مش موجودة: {name}")
            return
        print(f"✅ لاستخدام {name} في كودك:")
        print(f'   استورد "{file_path}"')
        return

    print(f"❌ أمر غير معروف: {action}")
    print("الأوامر المتاحة: list, use <name>")


def cmd_repl():
    """تشغيل REPL"""
    os.system('python repl.py')


def cmd_watch(file_path):
    """مراقبة الملف"""
    os.system(f'python watch.py {file_path}')


def cmd_docs(folder='./examples'):
    """توليد التوثيق"""
    os.system(f'python docs_gen.py {folder}')


def _generate(file_path):
    """يولّد ملفات HTML/CSS/JS من ملف .byan"""
    import os

    with open(file_path, 'r', encoding='utf-8') as f:
        source = f.read()

    print("🔤 تحليل لغوي...")
    tokens = Lexer(source).tokenize()
    print(f"   ✅ {len(tokens)} توكن")

    print("🌳 بناء الشجرة...")
    program = Parser(tokens).parse()
    print(f"   ✅ البرنامج: {program.name}")

    print("📥 معالجة الاستيراد...")
    base_dir = os.path.dirname(os.path.abspath(file_path))
    program = _load_imports(program, base_dir)

    print("⚙️  توليد الكود...")
    target = PythonAppTarget(output_dir='./build')
    result = target.generate(program)

    valid_files = [f for f in result['files'] if f]
    print(f"   ✅ تم إنشاء {len(valid_files)} ملف")
    print()
    print(f"📁 المجلد: {result['output']}")
    for f in valid_files:
        if f:
            print(f"   • {os.path.basename(f)}")
    print()
    print("▶️  للتشغيل:")
    print(f"   cd {result['output']}")
    print(f"   python run.py")


if __name__ == "__main__":
    main()
