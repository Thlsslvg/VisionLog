from pathlib import Path
import sys
import os
import json
import asyncio

import streamlit as st
import pandas as pd


sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )
)

from database.db import connect_database, disconnect_database, create_table, get_rejections
from services.language import t


st.set_page_config(
    page_title="Settings",
    page_icon="⚙️",
    layout="wide"
)


async def load_data():
    await connect_database()
    await create_table()
    rows = await get_rejections()
    await disconnect_database()
    return rows


BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent.parent

LOG_FOLDER = PROJECT_DIR / "logs" / "log"
DB_PATH = PROJECT_DIR / "database" / "visionlog.db"
CONFIG_PATH = PROJECT_DIR / "config.json"


if not CONFIG_PATH.exists():
    with open(CONFIG_PATH, "w", encoding="utf-8") as file:
        json.dump({"language": "en"}, file, indent=4)


with open(CONFIG_PATH, "r", encoding="utf-8") as file:
    config = json.load(file)


current_language = config.get("language", "en")

rows = asyncio.run(load_data())
df = pd.DataFrame([dict(row) for row in rows])

st.title(f"⚙️ {t('settings')}")

st.divider()

st.subheader(t("language"))

language = st.selectbox(
    t("select_language"),
    ["English", "Portuguese"],
    index=0 if current_language == "en" else 1
)

if st.button(t("save_language")):
    config["language"] = "en" if language == "English" else "pt"

    with open(CONFIG_PATH, "w", encoding="utf-8") as file:
        json.dump(config, file, indent=4)

    st.success("OK")
    st.rerun()

st.divider()

st.subheader(t("system_paths"))

st.text_input(
    t("log_folder"),
    value=str(LOG_FOLDER),
    disabled=True
)

st.text_input(
    t("database_path"),
    value=str(DB_PATH),
    disabled=True
)

st.divider()

st.subheader(t("system_status"))

log_folder_exists = LOG_FOLDER.exists()
db_exists = DB_PATH.exists()

txt_files = (
    list(LOG_FOLDER.glob("*.txt"))
    if log_folder_exists
    else []
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        t("log_folder"),
        "OK" if log_folder_exists else t("missing")
    )

with col2:
    st.metric(
        t("database"),
        "OK" if db_exists else t("missing")
    )

with col3:
    st.metric(
        t("txt_files"),
        len(txt_files)
    )

with col4:
    st.metric(
        t("db_records"),
        len(df)
    )

st.divider()

st.subheader(t("files_in_log_folder"))

if txt_files:
    file_data = []

    for file in txt_files:
        file_data.append(
            {
                "File": file.name,
                "Size (bytes)": file.stat().st_size
            }
        )

    st.dataframe(
        pd.DataFrame(file_data),
        use_container_width=True,
        hide_index=True
    )

else:
    st.info(t("no_txt_files"))

st.divider()

st.subheader(t("system_information"))

st.info(t("watchdog_info"))