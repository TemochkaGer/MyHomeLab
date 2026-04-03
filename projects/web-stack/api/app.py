from flask import Flask, jsonify
from datetime import datetime
import os
import socket

app = Flask(__name__)

# Получаем имя контейнера
CONTAINER_NAME = os.getenv('CONTAINER_NAME', 'unknown')
HOSTNAME = socket.gethostname()


@app.route('/')
def home():
    return jsonify({
        'message': 'Привет!\nЭто API моего домашнего сервера homelab, здесь будут собираться все важные параметры системы и заметки, которые я буду делать.',
        'timestamp': datetime.now().isoformat(),
        'container': CONTAINER_NAME,
        'hostname': HOSTNAME,
        'environ': os.environ
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/info')
def info():
    return jsonify({
        'python_version': os.popen('python3 --version').read().strip(),
        'uptime': os.popen('uptime -p').read().strip(),
        'memory_info': os.popen('free -h').read().strip()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)