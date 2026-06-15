import sys
import os
import asyncio

import streamlit as st
import pandas as pd
import plotly.express as px


sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )
)

from database.db import connect_database, disconnect_database, create_table, get_rejections
from services.language import t


st.set_page_config(
    page_title="Analytics",
    page_icon="📈",
    layout="wide"
)


async def load_data():
    await connect_database()
    await create_table()
    rows = await get_rejections()
    await disconnect_database()
    return rows


def apply_dark_theme(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117",
        font=dict(color="#F0F6FC")
    )
    return fig


rows = asyncio.run(load_data())
df = pd.DataFrame([dict(row) for row in rows])

st.title(f"📈 {t('analytics')}")

if df.empty:
    st.info(t("no_data"))

else:
    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
    df["date"] = df["created_at"].dt.date
    df["hour"] = df["created_at"].dt.hour.astype(str).str.zfill(2) + "h"

    st.subheader(t("production_summary"))

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(t("total_rejections"), len(df))

    with col2:
        st.metric(t("used_cameras"), df["camera"].nunique())

    with col3:
        st.metric(t("defect_types"), df["defect"].nunique())

    with col4:
        st.metric(t("most_common_defect"), df["defect"].value_counts().idxmax())

    st.divider()

    st.subheader(t("global_error_ranking"))

    defect_count = df["defect"].value_counts().reset_index()
    defect_count.columns = [t("defect"), t("occurrences")]

    fig_errors = px.bar(
        defect_count,
        x=t("occurrences"),
        y=t("defect"),
        orientation="h",
        text=t("occurrences"),
        title=t("global_error_ranking")
    )

    st.plotly_chart(
        apply_dark_theme(fig_errors),
        use_container_width=True
    )

    st.divider()

    st.subheader(t("rejections_by_date"))

    daily_count = (
        df.groupby("date")
        .size()
        .reset_index(name=t("rejections"))
    )

    fig_daily = px.line(
        daily_count,
        x="date",
        y=t("rejections"),
        markers=True,
        title=t("rejections_by_date")
    )

    st.plotly_chart(
        apply_dark_theme(fig_daily),
        use_container_width=True
    )

    st.divider()

    st.subheader(t("rejections_by_hour"))

    hourly_count = df["hour"].value_counts().reset_index()
    hourly_count.columns = ["Hour", t("rejections")]

    hourly_count = hourly_count.sort_values(
        t("rejections"),
        ascending=True
    )

    fig_hour = px.bar(
        hourly_count,
        x=t("rejections"),
        y="Hour",
        orientation="h",
        text=t("rejections"),
        title=t("rejections_by_hour")
    )

    st.plotly_chart(
        apply_dark_theme(fig_hour),
        use_container_width=True
    )

    st.divider()

    st.subheader(t("rejections_by_camera"))

    camera_count = df["camera"].value_counts().reset_index()
    camera_count.columns = [t("camera"), t("rejections")]

    fig_camera = px.bar(
        camera_count,
        x=t("camera"),
        y=t("rejections"),
        text=t("rejections"),
        title=t("rejections_by_camera")
    )

    st.plotly_chart(
        apply_dark_theme(fig_camera),
        use_container_width=True
    )

    st.divider()

    st.subheader(t("detailed_summary"))

    summary = (
        df.groupby(["camera", "defect"])
        .size()
        .reset_index(name=t("occurrences"))
        .sort_values(t("occurrences"), ascending=False)
    )

    summary = summary.rename(
        columns={
            "camera": t("camera"),
            "defect": t("defect")
        }
    )

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )