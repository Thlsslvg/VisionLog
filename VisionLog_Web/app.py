import csv
import json
import sqlite3
import sys
from datetime import datetime
from io import StringIO, BytesIO
from pathlib import Path

import pandas as pd

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    Response,
    session
)


app = Flask(__name__)
app.secret_key = "visionlog_secret_key"


BASE_DIR = Path(__file__).resolve().parent

if getattr(sys, "frozen", False):
    APP_DIR = Path(sys.executable).resolve().parent
else:
    APP_DIR = BASE_DIR


def find_project_root():
    possible_paths = [
        APP_DIR,
        APP_DIR.parent,
        APP_DIR.parent.parent,
        APP_DIR.parent.parent.parent,
        BASE_DIR,
        BASE_DIR.parent
    ]

    for path in possible_paths:
        db_path = path / "Back-End" / "database" / "visionlog.db"

        if db_path.exists():
            return path

    return BASE_DIR.parent


PROJECT_DIR = find_project_root()

DB_PATH = PROJECT_DIR / "Back-End" / "database" / "visionlog.db"
LOG_FOLDER = PROJECT_DIR / "Back-End" / "logs" / "log"
CONFIG_PATH = APP_DIR / "config.json"

ALARM_LIMIT = 5


TEXTS = {
    "en": {
        "dashboard": "Dashboard",
        "analytics": "Analytics",
        "logs": "Logs",
        "settings": "Settings",
        "total_rejections": "Total Rejections",
        "main_defect": "Main Defect",
        "critical_camera": "Critical Camera",
        "recent_logs": "Recent Logs",
        "verify_log": "Verify Log",
        "validate": "Validate",
        "alarm": "Alarm",
        "system_normal": "System Normal",
        "acknowledge": "Acknowledge Alarm",
        "filters": "Filters",
        "camera": "Camera",
        "defect": "Defect",
        "status": "Status",
        "file": "File",
        "export_csv": "Export CSV",
        "export_excel": "Export Excel",
        "language": "Language",
        "save": "Save",
        "system_status": "System Status",
        "database": "Database",
        "log_folder": "Log Folder",
        "refresh": "Refresh",
        "no_data": "No data available yet.",
        "no_logs": "No logs found yet.",
        "no_recent_logs": "No recent logs available.",
        "no_analytics": "No analytics data available yet.",
        "place_logs": "Place TXT logs in the monitored folder and keep the Watchdog running.",
                                                                                                                        "today_rejections": "Today's Rejections"
    },

    "pt": {
        "dashboard": "Dashboard",
        "analytics": "Análises",
        "logs": "Logs",
        "settings": "Configurações",
        "total_rejections": "Total de Rejeições",
        "main_defect": "Defeito Principal",
        "critical_camera": "Câmera Crítica",
        "recent_logs": "Logs Recentes",
        "verify_log": "Verificar Log",
        "validate": "Validar",
        "alarm": "Alarme",
        "system_normal": "Sistema Normal",
        "acknowledge": "Reconhecer Alarme",
        "filters": "Filtros",
        "camera": "Câmera",
        "defect": "Defeito",
        "status": "Status",
        "file": "Arquivo",
        "export_csv": "Exportar CSV",
        "export_excel": "Exportar Excel",
        "language": "Idioma",
        "save": "Salvar",
        "system_status": "Status do Sistema",
        "database": "Banco de Dados",
        "log_folder": "Pasta de Logs",
        "refresh": "Atualizar",
        "no_data": "Ainda não há dados disponíveis.",
        "no_logs": "Nenhum log encontrado ainda.",
        "no_recent_logs": "Nenhum log recente disponível.",
        "no_analytics": "Ainda não há dados suficientes para análise.",
        "place_logs": "Coloque logs TXT na pasta monitorada e mantenha o Watchdog em execução.",
    "today_rejections": "Rejeições Hoje",
    }
}


def load_config():
    if not CONFIG_PATH.exists():
        save_config({"language": "en"})

    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def save_config(config):
    with open(CONFIG_PATH, "w", encoding="utf-8") as file:
        json.dump(config, file, indent=4)


def t(key):
    lang = load_config().get("language", "en")
    return TEXTS.get(lang, TEXTS["en"]).get(key, key)


@app.context_processor
def inject_language():
    return {"t": t}


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def fetch_all_logs(camera=None, defect=None, status=None, search=None):
    connection = get_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM rejections WHERE 1=1"
    params = []

    if camera:
        query += " AND camera = ?"
        params.append(camera)

    if defect:
        query += " AND defect = ?"
        params.append(defect)

    if status:
        query += " AND status = ?"
        params.append(status)

    if search:
        query += " AND filename LIKE ?"
        params.append(f"%{search}%")

    query += " ORDER BY id DESC"

    cursor.execute(query, params)
    logs = cursor.fetchall()

    connection.close()

    return logs


def get_today_rejections():
    connection = get_connection()
    cursor = connection.cursor()

    today = datetime.now().strftime("%Y-%m-%d")

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM rejections
        WHERE substr(created_at, 1, 10) = ?
        """,
        (today,)
    )

    count = cursor.fetchone()[0]

    connection.close()

    return count


def get_dashboard_data():
    logs = fetch_all_logs()

    total = len(logs)

    defects = {}
    cameras = {}

    for log in logs:
        defects[log["defect"]] = defects.get(log["defect"], 0) + 1
        cameras[log["camera"]] = cameras.get(log["camera"], 0) + 1

    main_defect = max(defects, key=defects.get) if defects else "-"
    critical_camera = max(cameras, key=cameras.get) if cameras else "-"

    return {
        "total_rejections": total,
        "main_defect": main_defect,
        "critical_camera": critical_camera,
        "recent_logs": logs[:5],
        "has_data": total > 0
    }


def get_analytics_data():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT defect, COUNT(*) AS count
        FROM rejections
        GROUP BY defect
        ORDER BY count DESC
    """)
    defects = cursor.fetchall()

    cursor.execute("""
        SELECT camera, COUNT(*) AS count
        FROM rejections
        GROUP BY camera
        ORDER BY count DESC
    """)
    cameras = cursor.fetchall()

    cursor.execute("""
        SELECT substr(created_at, 1, 10) AS date, COUNT(*) AS count
        FROM rejections
        WHERE created_at IS NOT NULL
        GROUP BY date
        ORDER BY date
    """)
    dates = cursor.fetchall()

    cursor.execute("""
        SELECT substr(created_at, 12, 2) AS hour, COUNT(*) AS count
        FROM rejections
        WHERE created_at IS NOT NULL
        GROUP BY hour
        ORDER BY hour
    """)
    hours = cursor.fetchall()

    cursor.execute("""
        SELECT substr(created_at, 1, 10) AS date, defect, COUNT(*) AS count
        FROM rejections
        WHERE created_at IS NOT NULL
        GROUP BY date, defect
        ORDER BY date
    """)
    defect_trend = cursor.fetchall()

    cursor.execute("""
        SELECT substr(created_at, 1, 10) AS date, camera, COUNT(*) AS count
        FROM rejections
        WHERE created_at IS NOT NULL
        GROUP BY date, camera
        ORDER BY date
    """)
    camera_trend = cursor.fetchall()

    connection.close()

    return {
        "defects": defects,
        "cameras": cameras,
        "dates": dates,
        "hours": hours,
        "defect_trend": defect_trend,
        "camera_trend": camera_trend,
        "has_data": bool(defects or cameras or dates or hours)
    }


def get_filter_values():
    logs = fetch_all_logs()

    cameras = sorted(set(log["camera"] for log in logs))
    defects = sorted(set(log["defect"] for log in logs))
    statuses = sorted(set(log["status"] for log in logs))

    return cameras, defects, statuses


def validate_log_content(content):
    lines = [
        line.strip()
        for line in content.splitlines()
        if line.strip()
    ]

    if len(lines) < 4:
        return False, "Invalid log format", None

    try:
        data = {
            "camera": lines[0].split(":", 1)[1].strip(),
            "status": lines[1].split(":", 1)[1].strip(),
            "defect": lines[2].split(":", 1)[1].strip(),
            "time": lines[3].split(":", 1)[1].strip()
        }

        return True, "Valid log", data

    except Exception:
        return False, "Invalid log format", None


@app.route("/", methods=["GET", "POST"])
def dashboard():
    data = get_dashboard_data()

    today_rejections = get_today_rejections()
    today_key = datetime.now().strftime("%Y-%m-%d")

    if session.get("alarm_date") != today_key:
        session["alarm_date"] = today_key
        session["ack_count"] = 0

    if "ack_count" not in session:
        session["ack_count"] = 0

    new_rejections = today_rejections - session["ack_count"]
    alarm_active = new_rejections >= ALARM_LIMIT

    validation = None

    if request.method == "POST":

        if "refresh" in request.form:
            return redirect(url_for("dashboard"))

        if "acknowledge" in request.form:
            session["ack_count"] = today_rejections
            return redirect(url_for("dashboard"))

        uploaded_file = request.files.get("log_file")

        if uploaded_file and uploaded_file.filename != "":
            try:
                content = uploaded_file.read().decode("utf-8")

                valid, message, parsed = validate_log_content(content)

                validation = {
                    "valid": valid,
                    "message": message,
                    "parsed": parsed,
                    "content": content
                }

            except Exception as e:
                validation = {
                    "valid": False,
                    "message": f"Erro ao ler arquivo: {e}",
                    "parsed": None,
                    "content": ""
                }

        else:
            validation = {
                "valid": False,
                "message": "Nenhum arquivo selecionado.",
                "parsed": None,
                "content": ""
            }

    return render_template(
        "index.html",
        data=data,
        alarm_active=alarm_active,
        new_rejections=new_rejections,
        alarm_limit=ALARM_LIMIT,
        validation=validation,
        today_rejections=today_rejections
    )


@app.route("/analytics")
def analytics():
    data = get_analytics_data()

    return render_template(
        "analytics.html",
        data=data
    )


@app.route("/logs")
def logs():
    camera = request.args.get("camera")
    defect = request.args.get("defect")
    status = request.args.get("status")
    search = request.args.get("search")

    logs_data = fetch_all_logs(
        camera,
        defect,
        status,
        search
    )

    cameras, defects, statuses = get_filter_values()

    return render_template(
        "logs.html",
        logs=logs_data,
        cameras=cameras,
        defects=defects,
        statuses=statuses,
        selected_camera=camera,
        selected_defect=defect,
        selected_status=status,
        search=search,
        has_logs=len(logs_data) > 0
    )


@app.route("/export_csv")
def export_csv():
    logs_data = fetch_all_logs()

    output = StringIO()
    writer = csv.writer(output)

    writer.writerow(
        [
            "ID",
            "Camera",
            "Status",
            "Defect",
            "Time",
            "Filename",
            "Created At"
        ]
    )

    for log in logs_data:
        writer.writerow(
            [
                log["id"],
                log["camera"],
                log["status"],
                log["defect"],
                log["time"],
                log["filename"],
                log["created_at"]
            ]
        )

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=visionlog_logs.csv"
        }
    )


@app.route("/export_excel")
def export_excel():
    logs_data = fetch_all_logs()

    data = []

    for log in logs_data:
        data.append(
            {
                "ID": log["id"],
                "Camera": log["camera"],
                "Status": log["status"],
                "Defect": log["defect"],
                "Time": log["time"],
                "Filename": log["filename"],
                "Created At": log["created_at"]
            }
        )

    df = pd.DataFrame(data)

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(
            writer,
            index=False,
            sheet_name="Logs"
        )

    output.seek(0)

    return Response(
        output.getvalue(),
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=visionlog_logs.xlsx"
        }
    )


@app.route("/settings", methods=["GET", "POST"])
def settings():
    config = load_config()

    if request.method == "POST":
        config["language"] = request.form.get("language", "en")
        save_config(config)

        return redirect(url_for("settings"))

    txt_files = (
        list(LOG_FOLDER.glob("*.txt"))
        if LOG_FOLDER.exists()
        else []
    )

    settings_data = {
        "database_path": str(DB_PATH),
        "log_folder": str(LOG_FOLDER),
        "database_exists": DB_PATH.exists(),
        "log_folder_exists": LOG_FOLDER.exists(),
        "total_txt_files": len(txt_files),
        "total_db_records": get_dashboard_data()["total_rejections"],
        "language": config.get("language", "en")
    }

    return render_template(
        "settings.html",
        settings=settings_data
    )


if __name__ == "__main__":
    app.run(
        debug=False,
        host="127.0.0.1",
        port=5000,
        use_reloader=False
    )
