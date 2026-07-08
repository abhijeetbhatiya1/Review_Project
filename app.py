"""
The frontend: a Streamlit dashboard for a business owner.

Paste customer reviews (one per line), click Analyze, and see the results.
This app does NOT call Gemini directly. It calls OUR OWN backend (api.py),
exactly the way we called external APIs in Lesson 9.

Run it (in a SECOND terminal, while api.py is also running):
    uv run streamlit run app.py
"""

from collections import Counter

import requests
import streamlit as st

# Our own database code, kept in a separate file (database.py).
from database import init_db, save_results, load_history, DB_FILE

# The address of our own backend service.
API_URL = "http://127.0.0.1:8000/analyze"

def save_and_clear():
    if "results" in st.session_state:
        save_results(st.session_state.results)
        st.session_state.success_message = f"Saved {len(st.session_state.results)} reviews to the database."
        st.session_state.fade_out = True
    st.session_state.reviews_input = ""

# Make sure the table exists before the app uses it.
init_db()

st.title("📝 Customer Feedback Analyzer")

if "success_message" in st.session_state:
    st.success(st.session_state.success_message)
    del st.session_state.success_message

st.write("Paste your customer reviews below, one review per line.")

reviews_text = st.text_area("Reviews", height=200, key="reviews_input")

if st.button("Analyze"):
    # Split the text box into separate reviews, ignoring blank lines.
    reviews = [line.strip() for line in reviews_text.split('\n') if line.strip()]

    if not reviews:
        st.warning("Please provide at least one review.")
        if "results" in st.session_state:
            del st.session_state.results
    else:
        st.session_state.fade_out = False
        results = []
        # Go through each review and ask our backend to analyze it.
        for review in reviews:
            try:
                response = requests.post(API_URL, json={"text":review})
                data = response.json()
                results.append({
                    "review": review,
                    "label": data["label"],
                    "score": data["score"],
                    "theme": data["theme"]
                })
            except Exception:
                # One bad review should not stop the whole batch.
                results.append({
                    "review": review,
                    "label": "error",
                    "score": 0,
                    "theme": "error",
                })

        # Save results in session_state so they survive button clicks.
        st.session_state.results = results

# Show the results if we have any.
if "results" in st.session_state:
    results = st.session_state.results

    # Inject CSS for the fade-out animation if the fade_out flag is True
    if st.session_state.get("fade_out", False):
        st.markdown(
            """
            <style>
            @keyframes fadeOut {
                0% {
                    opacity: 1;
                    max-height: 2000px;
                }
                99% {
                    opacity: 0;
                    max-height: 0px;
                    margin: 0 !important;
                    padding: 0 !important;
                    overflow: hidden;
                }
                100% {
                    opacity: 0;
                    max-height: 0px;
                    margin: 0 !important;
                    padding: 0 !important;
                    overflow: hidden;
                    display: none !important;
                }
            }
            .st-key-results_container {
                animation: fadeOut 2.5s cubic-bezier(0.4, 0, 0.2, 1) forwards;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

    with st.container(key="results_container"):
        st.subheader("Results")
        st.dataframe(results)

        # ---- A simple summary for the business owner ----
        scores = [r["score"] for r in results if r["label"] != "error"]
        positive = [r for r in results if r["label"] == "positive"]
        themes = [r["theme"] for r in results if r["theme"] != "error"]

        st.subheader("Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("Reviews", len(results))
        if scores:
            col2.metric("Average score", round(sum(scores) / len(scores), 1))
            col3.metric("% Positive", f"{round(len(positive) / len(results) * 100)}%")

        if themes:
            # Counter tells us which theme appears most often.
            top_theme = Counter(themes).most_common(1)[0][0]
            st.info(f"Customers talk most about: **{top_theme}**")

        # ---- Save the full report to the database ----
        st.button("💾 Save to database", on_click=save_and_clear)

# ---- Show everything we have ever saved (reads from the database) ----
with st.expander("📚 Saved history (all reviews in the database)", expanded=st.session_state.get("fade_out", False)):
    history = load_history()
    if history:
        st.write(f"Total saved so far: {len(history)}")
        st.dataframe(
            [{"review": r[0], "label": r[1], "score": r[2], "theme": r[3]} for r in history]
        )
    else:
        st.write("Nothing saved yet. Analyze some reviews and click Save.")