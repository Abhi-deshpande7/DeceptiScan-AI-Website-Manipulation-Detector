import streamlit as st
import pandas as pd
from scraper import scrape_page, take_screenshot
from detector import detect_dark_patterns, detect_visual_dark_patterns
from legal import assess_legal_risk
from tracker import save_scan
import base64

st.set_page_config(page_title="Dark Pattern Detector", layout="wide")

st.title("Dark Pattern Detector")
st.markdown("Detect manipulative design patterns using Llama 3 + LLaVA — fully local, no API key needed.")
st.divider()

# Sidebar
st.sidebar.header("About")
st.sidebar.markdown("""
Uses **Llama 3** for text analysis and
**LLaVA** for visual screenshot analysis.
Fully local via Ollama — no API cost.
""")

st.sidebar.subheader("Try these")
examples = ["https://www.amazon.in", "https://www.booking.com", "https://www.flipkart.com"]
for ex in examples:
    if st.sidebar.button(ex):
        st.session_state.url = ex

enable_vision   = st.sidebar.toggle("Enable Visual Analysis (LLaVA)", value=True)
enable_legal    = st.sidebar.toggle("Enable Legal Risk Scoring", value=True)
save_to_tracker = st.sidebar.toggle("Save to Trend Tracker", value=True)

with st.expander("Dark pattern reference guide"):
    ref = {
        "Roach Motel":       "Easy to sign up, hard to cancel",
        "Confirmshaming":    "No thanks, I hate saving money",
        "Hidden costs":      "Price shown without fees until checkout",
        "Fake urgency":      "Only 2 left when there are 200",
        "Trick questions":   "Pre-ticked boxes to opt into marketing",
        "Forced continuity": "Free trial auto-charges with no reminder",
        "Privacy zuckering": "Default settings share maximum data",
        "Disguised ads":     "Ads that look like organic results"
    }
    st.dataframe(pd.DataFrame(ref.items(), columns=["Pattern", "Example"]), use_container_width=True)

url = st.text_input("Website URL", value=st.session_state.get("url", ""), placeholder="https://example.com")

if st.button("Analyse Website") and url:
    all_patterns = []

    # Text scraping
    with st.spinner("Scraping website content..."):
        page_data = scrape_page(url)

    if "error" in page_data:
        st.error(f"Could not scrape: {page_data['error']}")
    else:
        st.success(f"Scraped: {page_data['title']}")

        with st.spinner("Running Llama 3 text analysis..."):
            text_patterns = detect_dark_patterns(page_data)
            all_patterns.extend(text_patterns)

        # Visual analysis
        screenshot_b64 = None
        if enable_vision:
            with st.spinner("Taking screenshot for visual analysis..."):
                screenshot_b64 = take_screenshot(url)

            if screenshot_b64:
                img_bytes = base64.b64decode(screenshot_b64)
                st.image(img_bytes, caption="Screenshot analysed by LLaVA", use_column_width=True)

                with st.spinner("Running LLaVA visual analysis..."):
                    visual_patterns = detect_visual_dark_patterns(screenshot_b64)
                    for vp in visual_patterns:
                        vp["source"] = "Visual (LLaVA)"
                    all_patterns.extend(visual_patterns)
            else:
                st.warning("Screenshot failed — text analysis only.")

        for p in all_patterns:
            if "source" not in p:
                p["source"] = "Text (Llama 3)"

        # Save to tracker
        if save_to_tracker and all_patterns:
            save_scan(url, all_patterns)

        st.divider()

        if not all_patterns:
            st.success("No dark patterns detected.")
        else:
            high   = sum(1 for p in all_patterns if p.get("severity") == "High")
            medium = sum(1 for p in all_patterns if p.get("severity") == "Medium")
            low    = sum(1 for p in all_patterns if p.get("severity") == "Low")

            st.subheader("Detection Summary")
            k1, k2, k3, k4, k5 = st.columns(5)
            k1.metric("Total Found",    len(all_patterns))
            k2.metric("High",           high)
            k3.metric("Medium",         medium)
            k4.metric("Low",            low)
            k5.metric("Visual Patterns",sum(1 for p in all_patterns if p.get("source","").startswith("Visual")))

            st.divider()

            severity_icon = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}

            st.subheader("Detected Patterns")
            for pattern in all_patterns:
                sev  = pattern.get("severity", "Low")
                icon = severity_icon.get(sev, "🟢")
                src  = pattern.get("source", "Text")
                with st.expander(f"{icon} {pattern.get('pattern_name')} — {sev} — {src}"):
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown("**Category**")
                        st.write(pattern.get("category", "—"))
                        st.markdown("**Evidence**")
                        st.code(pattern.get("evidence", "—"))
                    with c2:
                        st.markdown("**Why manipulative**")
                        st.write(pattern.get("explanation", "—"))
                        st.markdown("**Ethical alternative**")
                        st.info(pattern.get("recommendation", "—"))

            # Legal risk
            if enable_legal:
                st.divider()
                st.subheader("Legal Risk Assessment")
                legal = assess_legal_risk(all_patterns)
                df_legal = pd.DataFrame(legal)
                st.dataframe(df_legal, use_container_width=True)

            st.divider()
            st.subheader("Full Report")
            df = pd.DataFrame(all_patterns)
            st.dataframe(df, use_container_width=True)
            st.download_button(
                "Download CSV Report",
                data=df.to_csv(index=False),
                file_name="dark_pattern_report.csv",
                mime="text/csv"
            )