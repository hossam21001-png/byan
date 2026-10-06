"""سيرفر API لتشغيل أوامر بيان من المتصفح"""
import os
import shutil
import subprocess
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/api/ping', methods=['GET'])
def ping():
    return jsonify({'status': 'ok', 'message': 'بيان API شغال'})


@app.route('/api/copy', methods=['POST'])
def copy_file():
    data = request.json
    src = data.get('source', '')
    dst = data.get('target', '')
    try:
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
        return jsonify({'status': 'ok', 'message': f'تم نسخ {src} إلى {dst}'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


@app.route('/api/move', methods=['POST'])
def move_file():
    data = request.json
    src = data.get('source', '')
    dst = data.get('target', '')
    try:
        shutil.move(src, dst)
        return jsonify({'status': 'ok', 'message': f'تم نقل {src} إلى {dst}'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


@app.route('/api/delete', methods=['POST'])
def delete_file():
    data = request.json
    path = data.get('path', '')
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
        return jsonify({'status': 'ok', 'message': f'تم حذف {path}'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


@app.route('/api/read', methods=['POST'])
def read_file():
    data = request.json
    path = data.get('path', '')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        return jsonify({'status': 'ok', 'content': content})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


@app.route('/api/write', methods=['POST'])
def write_file():
    data = request.json
    path = data.get('path', '')
    content = data.get('content', '')
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(path) else None
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return jsonify({'status': 'ok', 'message': f'تم كتابة {path}'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


@app.route('/api/mkdir', methods=['POST'])
def make_dir():
    data = request.json
    path = data.get('path', '')
    try:
        os.makedirs(path, exist_ok=True)
        return jsonify({'status': 'ok', 'message': f'تم إنشاء {path}'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


@app.route('/api/exec', methods=['POST'])
def execute_command():
    data = request.json
    cmd = data.get('command', '')
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True,
            text=True, timeout=30
        )
        return jsonify({
            'status': 'ok',
            'stdout': result.stdout,
            'stderr': result.stderr,
            'code': result.returncode
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


@app.route('/api/list', methods=['POST'])
def list_dir():
    data = request.json
    path = data.get('path', '.')
    try:
        items = os.listdir(path)
        result = []
        for item in items:
            full = os.path.join(path, item)
            result.append({
                'name': item,
                'type': 'dir' if os.path.isdir(full) else 'file',
                'size': os.path.getsize(full) if os.path.isfile(full) else 0
            })
        return jsonify({'status': 'ok', 'items': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400




# ===== SQLite =====
@app.route('/api/db/query', methods=['POST'])
def db_query():
    data = request.json
    sql = data.get('sql', '')
    db_path = data.get('db', '/storage/emulated/0/byan/byan_data.db')
    try:
        import sqlite3
        import re as regex
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # لو INSERT، تأكد إن الجدول موجود بالأعمدة الصح
        if sql.strip().upper().startswith('INSERT'):
            match = regex.search(r'INSERT INTO ([a-zA-Z0-9_]+)', sql, regex.IGNORECASE)
            if match:
                table = match.group(1)
                # استخرج الأعمدة
                cols_match = regex.search(r'\(([^)]+)\)', sql)
                if cols_match:
                    cols = [col.strip() for col in cols_match.group(1).split(',')]
                    cols_def = ', '.join(['[' + col + '] TEXT' for col in cols])
                    cursor.execute("CREATE TABLE IF NOT EXISTS " + table + " (" + cols_def + ")")
                    conn.commit()

        cursor.execute(sql)
        conn.commit()

        if sql.strip().upper().startswith('SELECT'):
            result = cursor.fetchall()
            conn.close()
            return jsonify({'status': 'ok', 'rows': result})

        rows_affected = cursor.rowcount
        conn.close()
        return jsonify({'status': 'ok', 'message': 'تم التنفيذ (' + str(rows_affected) + ' صف)'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


@app.route('/api/ai/ask', methods=['POST'])
def ai_ask():
    data = request.json
    prompt = data.get('prompt', '')
    api_key = data.get('api_key', '') or os.environ.get('OPENAI_API_KEY', '')
    try:
        import openai
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'user', 'content': prompt}]
        )
        return jsonify({
            'status': 'ok',
            'answer': response.choices[0].message.content
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


def start_server(host='127.0.0.1', port=5000):
    print(f"🚀 بدء سيرفر بيان API على http://{host}:{port}")
    app.run(host=host, port=port, debug=False, use_reloader=False)


if __name__ == '__main__':
    start_server()
