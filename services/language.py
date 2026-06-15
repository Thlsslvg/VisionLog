import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "config.json"

TEXTS = {
    "en": {

        # Dashboard
        "dashboard_title": "VLog Analytics",
        "subtitle": "Visteon Vision Monitoring System",

        "alarm": "Alarm",
        "acknowledge_alarm": "Acknowledge Alarm",

        "verify_log": "Verify Log",
        "select_file": "Select TXT File",
        "validate_log": "Validate Log",

        "valid_log": "Valid Log",
        "invalid_log": "Invalid Log",

        "last_processed_logs": "Last Processed Logs",

        "critical_camera": "Critical Camera",
        "last_rejection": "Last Rejection",

        "system_normal": "System Normal",

        "new_rejections_detected": "new rejections detected since last acknowledgement.",

        # Analytics
        "analytics": "Analytics",
        "production_summary": "Production Summary",
        "total_rejections": "Total Rejections",
        "used_cameras": "Used Cameras",
        "cameras_used": "Used Cameras",
        "defect_types": "Defect Types",
        "most_common_defect": "Most Common Defect",

        "global_error_ranking": "Global Error Ranking",
        "rejections_by_date": "Rejections by Date",
        "rejections_by_hour": "Rejections by Hour",
        "rejections_by_camera": "Rejections by Camera",
        "detailed_summary": "Detailed Summary",

        "camera": "Camera",
        "defect": "Defect",
        "status": "Status",
        "occurrences": "Occurrences",
        "rejections": "Rejections",

        # Logs
        "logs": "Logs",
        "filters": "Filters",
        "search_file": "Search File",
        "showing_records": "Displayed Records",
        "total_records": "Total Records",
        "export": "Export",
        "export_csv": "Export CSV",
        "export_excel": "Export Excel",

        # Settings
        "settings": "Settings",
        "language": "Language",
        "select_language": "Select Language",
        "save_language": "Save Language",

        "system_paths": "System Paths",
        "log_folder": "Log Folder",
        "database": "Database",
        "database_path": "Database Path",

        "system_status": "System Status",
        "txt_files": "TXT Files",
        "db_records": "Database Records",

        "files_in_log_folder": "Files in Log Folder",
        "system_information": "System Information",

        "missing": "Missing",

        "no_data": "No data available.",
        "no_logs": "No logs found in database.",
        "no_txt_files": "No TXT files found.",

        "watchdog_info": "The Watchdog is controlled by main.py. Keep main.py running to process logs automatically."
    },

    "pt": {

        # Dashboard
        "dashboard_title": "VLog Analytics",
        "subtitle": "Sistema de Monitorização de Visão Visteon",

        "alarm": "Alarme",
        "acknowledge_alarm": "Reconhecer Alarme",

        "verify_log": "Verificar Log",
        "select_file": "Selecionar Arquivo TXT",
        "validate_log": "Validar Log",

        "valid_log": "Log Válido",
        "invalid_log": "Log Inválido",

        "last_processed_logs": "Últimos Logs Processados",

        "critical_camera": "Câmera Crítica",
        "last_rejection": "Última Rejeição",

        "system_normal": "Sistema Normal",

        "new_rejections_detected": "novas rejeições detectadas desde o último reconhecimento.",

        # Analytics
        "analytics": "Análises",
        "production_summary": "Resumo da Produção",
        "total_rejections": "Total de Rejeições",
        "used_cameras": "Câmeras Utilizadas",
        "cameras_used": "Câmeras Utilizadas",
        "defect_types": "Tipos de Defeito",
        "most_common_defect": "Defeito Mais Frequente",

        "global_error_ranking": "Ranking Global de Erros",
        "rejections_by_date": "Rejeições por Data",
        "rejections_by_hour": "Rejeições por Hora",
        "rejections_by_camera": "Rejeições por Câmera",
        "detailed_summary": "Resumo Detalhado",

        "camera": "Câmera",
        "defect": "Defeito",
        "status": "Status",
        "occurrences": "Ocorrências",
        "rejections": "Rejeições",

        # Logs
        "logs": "Logs",
        "filters": "Filtros",
        "search_file": "Pesquisar Arquivo",
        "showing_records": "Registros Exibidos",
        "total_records": "Total de Registros",
        "export": "Exportação",
        "export_csv": "Exportar CSV",
        "export_excel": "Exportar Excel",

        # Settings
        "settings": "Configurações",
        "language": "Idioma",
        "select_language": "Selecionar Idioma",
        "save_language": "Salvar Idioma",

        "system_paths": "Caminhos do Sistema",
        "log_folder": "Pasta de Logs",
        "database": "Banco de Dados",
        "database_path": "Caminho do Banco de Dados",

        "system_status": "Status do Sistema",
        "txt_files": "Arquivos TXT",
        "db_records": "Registros no Banco",

        "files_in_log_folder": "Arquivos na Pasta de Logs",
        "system_information": "Informações do Sistema",

        "missing": "Ausente",

        "no_data": "Nenhum dado disponível.",
        "no_logs": "Nenhum log encontrado no banco de dados.",
        "no_txt_files": "Nenhum arquivo TXT encontrado.",

        "watchdog_info": "O Watchdog é controlado pelo main.py. Mantenha o main.py em execução para processar logs automaticamente."
    }
}


def get_language():
    if not CONFIG_PATH.exists():
        return "en"

    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        config = json.load(file)

    return config.get("language", "en")


def t(key):
    language = get_language()

    value = TEXTS.get(language, {}).get(key)

    if value is None:
        return f"[MISSING:{key}]"

    return value