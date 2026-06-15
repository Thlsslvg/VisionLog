import sys
import os
import asyncio
from io import BytesIO

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
    page_title="Logs",
    page_icon="📋",
    layout="wide"
)


async def load_data():
    await connect_database()
    await create_table()
    rows = await get_rejections()
    await disconnect_database()
    return rows


def to_excel(dataframe):
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        dataframe.to_excel(
            writer,
            index=False,
            sheet_name="Logs"
        )

    return output.getvalue()


rows = asyncio.run(load_data())
df = pd.DataFrame([dict(row) for row in rows])

st.title(f"📋 {t('logs')}")

if df.empty:
    st.info(t("no_logs"))

else:
    st.subheader(t("filters"))

    col1, col2, col3 = st.columns(3)

    with col1:
        camera_filter = st.selectbox(
            t("camera"),
            ["All"] + sorted(df["camera"].unique().tolist())
        )

    with col2:
        defect_filter = st.selectbox(
            t("defect"),
            ["All"] + sorted(df["defect"].unique().tolist())
        )

    with col3:
        status_filter = st.selectbox(
            t("status"),
            ["All"] + sorted(df["status"].unique().tolist())
        )

    search_file = st.text_input(
        t("search_file"),
        placeholder="log1.txt"
    )

    filtered_df = df.copy()

    if camera_filter != "All":
        filtered_df = filtered_df[
            filtered_df["camera"] == camera_filter
        ]

    if defect_filter != "All":
        filtered_df = filtered_df[
            filtered_df["defect"] == defect_filter
        ]

    if status_filter != "All":
        filtered_df = filtered_df[
            filtered_df["status"] == status_filter
        ]

    if search_file:
        filtered_df = filtered_df[
            filtered_df["filename"]
            .astype(str)
            .str.contains(search_file, case=False, na=False)
        ]

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.metric(t("showing_records"), len(filtered_df))

    with col2:
        st.metric(t("total_records"), len(df))

    st.divider()

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader(t("export"))

    col1, col2 = st.columns(2)

    with col1:
        csv = filtered_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label=f"⬇️ {t('export_csv')}",
            data=csv,
            file_name="visionlog_logs.csv",
            mime="text/csv"
        )

    with col2:
        excel_file = to_excel(filtered_df)

        st.download_button(
            label=f"⬇️ {t('export_excel')}",
            data=excel_file,
            file_name="visionlog_logs.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )