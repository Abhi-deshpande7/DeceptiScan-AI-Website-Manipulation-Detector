import streamlit as st
import pandas as pd
import plotly.express as px
from tracker import get_all_tracked_urls, get_url_history

st.set_page_config(page_title="Trend Tracker", layout="wide")
st.title("Dark Pattern Trend Tracker")
st.markdown("Track how a website's dark pattern score changes over time.")
st.divider()

urls = get_all_tracked_urls()

if not urls:
    st.info("No websites tracked yet. Analyse a website from the main page first.")
else:
    selected = st.selectbox("Select a tracked website", urls)

    if selected:
        history = get_url_history(selected)

        if not history:
            st.warning("No history found for this website.")
        else:
            df = pd.DataFrame([{
                "date":           h["date"],
                "total_patterns": h["total_patterns"],
                "high":           h["high"],
                "medium":         h["medium"],
                "low":            h["low"]
            } for h in history])

            # KPIs
            latest = history[-1]
            first  = history[0]
            change = latest["total_patterns"] - first["total_patterns"]

            k1, k2, k3 = st.columns(3)
            k1.metric("Total Scans",        len(history))
            k2.metric("Latest Score",       latest["total_patterns"])
            k3.metric("Change since first", change, delta=change)

            st.divider()

            st.subheader("Dark Pattern Count Over Time")
            fig = px.line(
                df, x="date", y="total_patterns",
                markers=True,
                labels={"total_patterns": "Patterns Found", "date": "Scan Date"}
            )
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("Severity Breakdown Over Time")
            fig2 = px.bar(
                df, x="date",
                y=["high", "medium", "low"],
                barmode="stack",
                color_discrete_sequence=["#E24B4A", "#EF9F27", "#1D9E75"],
                labels={"value": "Count", "date": "Scan Date"}
            )
            st.plotly_chart(fig2, use_container_width=True)

            st.subheader("Scan History")
            st.dataframe(df, use_container_width=True)