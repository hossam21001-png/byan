# -*- coding: utf-8 -*-
"""B: Python Bundle — program.py + byan_rt.py + run.sh"""

import os
import shutil


class PythonBundlePackager:
    """ينشئ حزمة Python قابلة للتشغيل"""

    def __init__(self, build_dir, byan_root):
        self.build_dir = build_dir
        self.byan_root = byan_root

    def package(self, output_dir=None, program_source=None):
        """ينسخ كل حاجة لمجلد output"""
        if output_dir is None:
            output_dir = os.path.join(self.build_dir, '..', 'program_py')
        os.makedirs(output_dir, exist_ok=True)
        files = []

        # 1. program.py
        if program_source:
            py_path = os.path.join(output_dir, "program.py")
            with open(py_path, "w", encoding="utf-8") as f:
                f.write(program_source)
            files.append(py_path)

        # 2. byan_rt.py
        rt_src = os.path.join(self.byan_root, "byan_rt.py")
        if os.path.exists(rt_src):
            rt_dst = os.path.join(output_dir, "byan_rt.py")
            shutil.copy2(rt_src, rt_dst)
            files.append(rt_dst)

        # 3. run.sh
        sh_path = os.path.join(output_dir, "run.sh")
        with open(sh_path, "w", encoding="utf-8") as f:
            f.write("#!/usr/bin/env bash\n")
            f.write('cd "$(dirname "$0")"\n')
            f.write('exec python3 program.py "$@"\n')
        os.chmod(sh_path, 0o755)
        files.append(sh_path)

        # 4. run.bat
        bat_path = os.path.join(output_dir, "run.bat")
        with open(bat_path, "w", encoding="utf-8") as f:
            f.write("@echo off\n")
            f.write('cd /d "%~dp0"\n')
            f.write("python program.py %*\n")
        files.append(bat_path)

        # 5. requirements.txt
        req_path = os.path.join(output_dir, "requirements.txt")
        with open(req_path, "w", encoding="utf-8") as f:
            f.write("# لا توجد اعتماديات خارجية\n")
        files.append(req_path)

        # 6. README
        readme_path = os.path.join(output_dir, "README.md")
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write("# Byan Program\n\n")
            f.write("## التشغيل\n\n")
            f.write("### Linux/Mac: `./run.sh`\n\n")
            f.write("### Windows: `run.bat`\n\n")
            f.write("### يدوي: `python3 program.py`\n")
        files.append(readme_path)

        total_size = sum(os.path.getsize(f) for f in files)
        return {"output": output_dir, "files": files, "size": total_size}