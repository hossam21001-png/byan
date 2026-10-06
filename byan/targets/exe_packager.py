"""يولّد ملف تنفيذي مستقل من مشروع بيان"""
import os
import subprocess
import sys


class ExePackager:
    """يحوّل مشروع بيان لملف تنفيذي"""

    def __init__(self, build_dir='./build', name='byan_app'):
        self.build_dir = os.path.abspath(build_dir)
        self.name = name

    def package(self):
        """يبني ملف تنفيذي بـ pyinstaller"""
        print(f"📦 جاري بناء ملف تنفيذي: {self.name}")

        # ولّد ملف main.py مؤقت
        main_py = os.path.join(self.build_dir, 'main.py')
        with open(main_py, 'w', encoding='utf-8') as f:
            f.write('''import os
import sys
import threading
import time
import webbrowser

HTML_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")

def start_api():
    """يشغّل API server في thread منفصل"""
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from byan.runtime.api_server import start_server
        start_server(port=5000)
    except Exception as e:
        print(f"⚠️ API server: {e}")

def main():
    # شغّل API في الخلفية
    api_thread = threading.Thread(target=start_api, daemon=True)
    api_thread.start()

    time.sleep(1)  # استنى السيرفر يبدأ

    try:
        import webview
        webview.create_window(
            title="بيان",
            url="file://" + HTML_PATH,
            width=1000,
            height=700,
        )
        webview.start()
    except ImportError:
        print("فتح المتصفح...")
        webbrowser.open("file://" + HTML_PATH)
        input("اضغط Enter للإغلاق...")

if __name__ == "__main__":
    main()
''')

        # شغّل pyinstaller
        try:
            result = subprocess.run([
                'pyinstaller', '--onefile', '--windowed',
                '--name', self.name,
                '--add-data', f'{self.build_dir}:.',
                main_py
            ], capture_output=True, text=True)

            if result.returncode == 0:
                print(f"✅ تم إنشاء ملف تنفيذي: dist/{self.name}")
                return True
            else:
                print(f"❌ خطأ في البناء:")
                print(result.stderr)
                return False
        except FileNotFoundError:
            print("❌ pyinstaller مش مثبت")
            print("ثبّته بـ: pip install pyinstaller")
            return False
