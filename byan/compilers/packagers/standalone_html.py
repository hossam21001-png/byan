# -*- coding: utf-8 -*-
"""A: HTML standalone — ملف واحد فيه كل حاجة"""

import os
import base64


class StandaloneHtmlPackager:
    """يدمج HTML + CSS + JS + PWA في ملف واحد"""

    def __init__(self, build_dir):
        self.build_dir = build_dir

    def package(self, output_path=None):
        """يدمج كل الملفات في ملف HTML واحد"""
        if output_path is None:
            output_path = os.path.join(self.build_dir, '..', 'program_standalone.html')

        html = self._read("index.html") or self._default_html()
        css = self._read("style.css") or ""
        js = self._read("script.js") or ""
        icon = self._read("icon.svg") or self._default_icon()

        # CSS inline
        html = html.replace(
            '<link rel="stylesheet" href="style.css">',
            "<style>\n" + css + "\n</style>"
        )
        # JS inline
        html = html.replace(
            '<script src="script.js"></script>',
            "<script>\n" + js + "\n</script>"
        )
        # Icon inline
        if "icon.svg" in html:
            icon_b64 = base64.b64encode(icon.encode("utf-8")).decode("ascii")
            html = html.replace(
                'href="icon.svg"',
                'href="data:image/svg+xml;base64,' + icon_b64 + '"'
            )
        # ازيل PWA
        html = html.replace('<link rel="manifest" href="manifest.json">', "")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

        return {"output": output_path, "size": os.path.getsize(output_path)}

    def _read(self, name):
        p = os.path.join(self.build_dir, name)
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                return f.read()
        return None

    def _default_html(self):
        return "<!DOCTYPE html>\n<html lang=\"ar\" dir=\"rtl\">\n<head><meta charset=\"UTF-8\"><title>Byan</title></head>\n<body><h1>Byan</h1></body></html>"

    def _default_icon(self):
        return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="40" fill="#667eea"/></svg>'