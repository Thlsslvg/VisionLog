from pathlib import Path
import sys
import os
import asyncio
from collections import Counter

import streamlit as st
import pandas as pd

try:
    from streamlit_autorefresh import st_autorefresh
except ImportError:
    st_autorefresh = None


sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from database.db import connect_database, disconnect_database, create_table, get_rejections
from services.language import t


st.set_page_config(
    page_title="VLog Analytics",
    page_icon="📊",
    layout="wide"
)


if st_autorefresh:
    st_autorefresh(
        interval=5000,
        key="dashboard_refresh"
    )


BASE_DIR = Path(__file__).resolve().parent
logo_path = BASE_DIR / "assets" / "logo.png"


async def load_data():
    await connect_database()
    await create_table()
    rows = await get_rejections()
    await disconnect_database()
    return rows


def validate_log_content(content):
    lines = [
        line.strip()
        for line in content.splitlines()
        if line.strip()
    ]

    if len(lines) < 4:
        return False, t("invalid_log"), None

    try:
        data = {
            "camera": lines[0].split(":", 1)[1].strip(),
            "status": lines[1].split(":", 1)[1].strip(),
            "defect": lines[2].split(":", 1)[1].strip(),
            "time": lines[3].split(":", 1)[1].strip()
        }

        return True, t("valid_log"), data

    except Exception:
        return False, t("invalid_log"), None


if "last_acknowledged_count" not in st.session_state:
    st.session_state.last_acknowledged_count = 0


rows = asyncio.run(load_data())
df = pd.DataFrame([dict(row) for row in rows])


col1, col2 = st.columns([1, 5])

with col1:
    if logo_path.exists():
        st.image(str(logo_path), width=100)

with col2:
    st.title(t("dashboard_title"))
    st.caption(t("subtitle"))

st.divider()


if not df.empty:
    total_rejections = len(df)
    most_common_defect = Counter(df["defect"]).most_common(1)[0][0]
    critical_camera = Counter(df["camera"]).most_common(1)[0][0]
    last_rejection = df.iloc[0]["time"]
else:
    total_rejections = 0
    most_common_defect = "-"
    critical_camera = "-"
    last_rejection = "-"


ALARM_LIMIT = 5

current_rejections = total_rejections
new_rejections = current_rejections - st.session_state.last_acknowledged_count

if new_rejections >= ALARM_LIMIT:
    st.error(
        f"🚨 {t('alarm')}: {new_rejections} "
        f"{t('new_rejections_detected')}"
    )

    if st.button(f"✅ {t('acknowledge_alarm')}"):
        st.session_state.last_acknowledged_count = current_rejections
        st.rerun()

else:
    st.success(
        f"🟢 {t('system_normal')} — {new_rejections}/{ALARM_LIMIT}"
    )

st.divider()


c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(t("total_rejections"), total_rejections)

with c2:
    st.metric(t("most_common_defect"), most_common_defect)

with c3:
    st.metric(t("critical_camera"), critical_camera)

with c4:
    st.metric(t("last_rejection"), last_rejection)

st.divider()


st.subheader(f"🔍 {t('verify_log')}")

uploaded_file = st.file_uploader(
    t("select_file"),
    type=["txt"]
)

if uploaded_file:
    content = uploaded_file.read().decode("utf-8")

    st.text_area(
        "Log Info",
        value=content,
        height=150
    )

    if st.button(t("validate_log")):
        valid, message, parsed_data = validate_log_content(content)

        if valid:
            st.success(message)

            a, b, c, d = st.columns(4)

            with a:
                st.info(f"{t('camera')}: {parsed_data['camera']}")

            with b:
                st.info(f"{t('status')}: {parsed_data['status']}")

            with c:
                st.info(f"{t('defect')}: {parsed_data['defect']}")

            with d:
                st.info(f"Time: {parsed_data['time']}")

        else:
            st.error(message)

st.divider()


st.subheader(f"📋 {t('last_processed_logs')}")

if not df.empty:
    recent_df = df.head(5)

    st.dataframe(
        recent_df,
        use_container_width=True,
        hide_index=True
    )

else:
    st.info(t("no_logs"))


st.caption(t("watchdog_info"))