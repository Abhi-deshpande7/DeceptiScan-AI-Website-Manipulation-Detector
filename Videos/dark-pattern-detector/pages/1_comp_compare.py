import streamlit as st
import pandas as pd
import plotly.express as px
from scraper import scrape_page
from detector import detect_dark_patterns

st.set_page_config(page_title="Competitor Comparison", layout="wide")
st.title("Competitor Dark Pattern Comparison")
st.markdown("Analyse multiple websites and compare their dark pattern scores side by side.")
st.divider()

st.subheader("Enter up to 4 competitor URLs")
urls = []
c1, c2 = st.columns(2)
with c1:
    u1 = st.text_input("Website 1", placeholder="https://amazon.in")
    u2 = st.text_input("Website 2", placeholder="https://flipkart.com")
with c2:
    u3 = st.text_input("Website 3", placeholder="https://myntra.com")
    u4 = st.text_input("Website 4", placeholder="https://meesho.com")

for u in [u1, u2, u3, u4]:
    if u.strip():
        urls.append(u.strip())

if st.button("Compare All") and urls:
    results = []
    for url in urls:
        with st.spinner(f"Analysing {url}..."):
            page_data = scrape_page(url)
            if "error" not in page_data:
                patterns = detect_dark_patterns(page_data)
                high   = sum(1 for p in patterns if p.get("severity") == "High")
                medium = sum(1 for p in patterns if p.get("severity") == "Medium")
                low    = sum(1 for p in patterns if p.get("severity") == "Low")
                score  = (high * 3) + (medium * 2) + (low * 1)
                results.append({
                    "website":        url,
                    "total_patterns": len(patterns),
                    "high":           high,
                    "medium":         medium,
                    "low":            low,
                    "dark_score":     score
                })
            else:
                st.warning(f"Could not scrape {url}")

    if results:
        st.divider()
        df = pd.DataFrame(results)

        # Winner / worst
        worst  = df.loc[df["dark_score"].idxmax(), "website"]
        cleanest = df.loc[df["dark_score"].idxmin(), "website"]
        st.error(f"Most manipulative: {worst}")
        st.success(f"Cleanest website: {cleanest}")

        st.divider()

        # Bar chart
        st.subheader("Dark Pattern Score Comparison")
        fig = px.bar(
            df, x="website", y="dark_score",
            color="dark_score",
            color_continuous_scale=["green", "yellow", "red"],
            labels={"dark_score": "Dark Score", "website": "Website"}
        )
        st.plotly_chart(fig, use_container_width=True)

        # Breakdown chart
        st.subheader("Severity Breakdown")
        fig2 = px.bar(
            df, x="website",
            y=["high", "medium", "low"],
            barmode="group",
            color_discrete_sequence=["#E24B4A", "#EF9F27", "#1D9E75"],
            labels={"value": "Count", "website": "Website"}
        )
        st.plotly_chart(fig2, use_container_width=True)

        st.subheader("Full Comparison Table")
        st.dataframe(df, use_container_width=True)

        st.download_button(
            "Download Comparison CSV",
            data=df.to_csv(index=False),
            file_name="competitor_comparison.csv",
            mime="text/csv"
        )