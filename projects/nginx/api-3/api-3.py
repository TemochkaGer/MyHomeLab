from flask import Flask, request, jsonify, send_from_directory
from pathlib import Path

app = Flask(__name__)
app.json.ensure_ascii = False

BASE_PATH = Path(__file__).parent
SYSINFO_FILE_PATH = BASE_PATH / "SysInfo" / "Sysinfo.txt"
GRAFICS_PATH = BASE_PATH / "grafs"

@app.route("/")
def home():
    return """Это 3 контейтейнер"""

@app.route("/api/info")
def info():
    try:
        if not (SYSINFO_FILE_PATH).exists():
            return jsonify({"error": f"Не удалось найти файл {SYSINFO_FILE_PATH}"}), 404

        with open(f'{SYSINFO_FILE_PATH}', 'r', encoding="utf-8") as f:
            sys_info = f.read()

        return jsonify({"system_information": sys_info})
    except PermissionError:
        return jsonify({"error": "Нет доступа на чтение файла"}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/graf/<component>")
def grafics(component):
    ALLOWED = {'amdgpu', 'k10temp', 'nvme'}
    if component not in ALLOWED:
        return jsonify({"error": f"Неизвестное устройство: {component}"}), 404
    
    filename = f"Graf_{component}.png"
    if not (GRAFICS_PATH / filename).exists():
        return jsonify({"error": "Графика не существует"}), 404
    
    return send_from_directory(f"{GRAFICS_PATH}", filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7333)