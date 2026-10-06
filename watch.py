# -*- coding: utf-8 -*-
"""بيان Watch — إعادة التوليد عند التغيير"""
import sys
import os
import time
import subprocess

def watch(file_path):
    print(f"👁️  مراقبة: {file_path}")
    last_mtime = 0

    while True:
        try:
            mtime = os.path.getmtime(file_path)
            if mtime != last_mtime:
                last_mtime = mtime
                print(f"\n🔄 تغيير في الملف، إعادة التوليد...")
                os.system(f"python cli.py {file_path}")
                print("✅ جاهز")
        except KeyboardInterrupt:
            print("\n👋 انتهى")
            break
        except Exception as e:
            print(f"❌ {e}")
        time.sleep(1)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("الاستخدام: python watch.py <file.byan>")
        sys.exit(1)
    watch(sys.argv[1])
