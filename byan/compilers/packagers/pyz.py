# -*- coding: utf-8 -*-
"""C: .pyz — Python zipapp"""

import os
import shutil
import zipapp


class PyzPackager:
    """ينشئ ملف .pyz قابل للتنفيذ"""

    def __init__(self, build_dir, byan_root):
        self.build_dir = build_dir
        self.byan_root = byan_root

    def package(self, output_path=None, program_source=None):
        """ينشئ program.pyz"""
        if output_path is None:
            output_path = os.path.join(self.build_dir, '..', 'program.pyz')

        staging = os.path.join(self.build_dir, "_pyz_staging")
        if os.path.exists(staging):
            shutil.rmtree(staging)
        os.makedirs(staging)

        # 1. __main__.py
        if program_source:
            main_path = os.path.join(staging, "__main__.py")
            with open(main_path, "w", encoding="utf-8") as f:
                f.write(program_source)

        # 2. byan_rt.py
        rt_src = os.path.join(self.byan_root, "byan_rt.py")
        if os.path.exists(rt_src):
            shutil.copy2(rt_src, os.path.join(staging, "byan_rt.py"))

        # 3. إنشاء .pyz
        zipapp.create_archive(staging, output_path,
                              interpreter="/usr/bin/env python3",
                              compressed=True)
        os.chmod(output_path, 0o755)

        shutil.rmtree(staging, ignore_errors=True)
        return {"output": output_path, "size": os.path.getsize(output_path)}