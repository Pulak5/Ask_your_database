"""Streamlit UI for Ask Your Database."""
import os

import plotly.graph_objects as go
import requests
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(page_title="Ask Your Database 🔍", layout="wide")
st.title("Ask Your Database 🔍")
st.caption("Type a question in plain English. The AI generates SQL, runs it, and shows you a chart.")

# Sidebar
with st.sidebar:
    st.header("Settings")
    few_shot = st.toggle("Few-shot prompting", value=False)
    show_sql = st.toggle("Show generated SQL", value=True)
    st.markdown("---")
    st.markdown(f"**Backend:** Connected to FastAPI at `{API_BASE_URL}`")
    # health check
    try:
        health = requests.get(f"{API_BASE_URL}/health", timeout=3).json()
        st.success(f"✅ API online — model: `{health.get('backend', 'unknown')}`")
    except Exception:
        st.error("❌ API unreachable")

# Example questions
st.subheader("Example questions")
examples = [
    "List all films in the Action category",
    "Who are the top 5 customers by total spending?",
    "Which films have never been rented?",
    "How many rentals occurred each month?",
    "What is the average rental duration by film category?",
    "Which actors have appeared in more than 10 films?",
    "What is the total revenue per store?",
    "List the 10 most rented films",
]
cols = st.columns(4)
selected_example = None
for i, ex in enumerate(examples):
    if cols[i % 4].button(ex, key=f"ex_{i}"):
        selected_example = ex

# Question input
if "question" not in st.session_state:
    st.session_state["question"] = ""
if selected_example:
    st.session_state["question"] = selected_example

question = st.text_input("Your question:", value=st.session_state.get("question", ""), key="question_input")
col_ask, col_clear = st.columns([1, 5])
ask = col_ask.button("🔍 Ask", type="primary")
if col_clear.button("🔄 Clear"):
    st.session_state["question"] = ""
    st.rerun()

if ask and question.strip():
    with st.spinner("Generating SQL and running query..."):
        try:
            resp = requests.post(
                f"{API_BASE_URL}/ask",
                json={"question": question, "few_shot": few_shot},
                timeout=30
            )
            if resp.status_code == 400:
                st.error(f"🚫 Query blocked: {resp.json().get('detail', 'unsafe query')}")
            elif resp.status_code != 200:
                st.error(f"API error {resp.status_code}: {resp.text}")
            else:
                data = resp.json()
                if show_sql:
                    with st.expander("Generated SQL", expanded=True):
                        st.code(data["sql"], language="sql")
                st.caption(f"⏱ {data['latency_ms']:.0f} ms | backend: `{data['backend']}`")
                if data.get("blocked"):
                    st.warning(f"Query was blocked: {data.get('block_reason')}")
                elif data.get("rows"):
                    st.subheader("Results")
                    st.dataframe(data["rows"], use_container_width=True)
                    if data.get("plotly_fig"):
                        fig = go.Figure(data["plotly_fig"])
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Query returned no results.")
        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to API. Make sure `docker compose up` is running.")
        except Exception as e:
            st.error(f"Unexpected error: {e}")
