# -*- coding: utf-8 -*-
"""مولّد توثيق لملفات بيان"""
import os
import re

def generate_docs(folder, output='docs.html'):
    """يولّد HTML من ملفات .byan"""
    html = ["""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>توثيق بيان</title>
    <style>
        body { font-family: 'Cairo', sans-serif; padding: 20px; background: #f5f5f5; }
        h1 { color: #667eea; }
        .file { background: white; padding: 20px; margin: 15px 0; border-radius: 10px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        pre { background: #1e1e1e; color: #d4d4d4; padding: 15px; border-radius: 8px;
              overflow-x: auto; direction: rtl; }
    </style>
</head>
<body>
    <h1>📚 توثيق بيان</h1>
"""]

    for root, dirs, files in os.walk(folder):
        for f in files:
            if f.endswith('.byan'):
                path = os.path.join(root, f)
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()

                # استخرج التعليقات
                comments = re.findall(r'#\s*(.+)', content)

                html.append(f'<div class="file">')
                html.append(f'<h2>📄 {f}</h2>')
                if comments:
                    html.append('<h3>التعليقات:</h3><ul>')
                    for c in comments:
                        html.append(f'<li>{c}</li>')
                    html.append('</ul>')
                html.append(f'<h3>الكود:</h3><pre>{content.replace("<", "&lt;")}</pre>')
                html.append('</div>')

    html.append('</body></html>')

    with open(output, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html))

    print(f"✅ تم إنشاء التوثيق: {output}")

if __name__ == '__main__':
    import sys
    folder = sys.argv[1] if len(sys.argv) > 1 else './examples'
    generate_docs(folder)
