import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path
import json
import uuid

from sentiment import analyze_sentiment
from storage import load_reviews, save_review, export_json, ensure_data_files
from reports import sentiment_summary, create_sentiment_chart, create_timeline_chart

ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"
CHART_DIR = ROOT / "charts"
CSV_PATH = DATA_DIR / "reviews.csv"
JSON_PATH = DATA_DIR / "reviews.json"

st.set_page_config(
    page_title="MoodLens | Text Sentiment Studio",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
:root { --ink:#182033; --muted:#7c879b; --violet:#7457f5; --cyan:#4bc7d5; --rose:#f17eb5; }
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
.stApp {
  background:
    radial-gradient(ellipse at 12% 3%, rgba(133,111,255,.16), transparent 33%),
    radial-gradient(ellipse at 92% 10%, rgba(241,126,181,.13), transparent 28%),
    linear-gradient(135deg,#f7f8ff 0%,#f5f9ff 52%,#fff8fc 100%);
  color:var(--ink);
}
h1,h2,h3,h4 { font-family:'Manrope',sans-serif !important; color:#202744; letter-spacing:-.035em; }
.block-container { max-width:1280px; padding-top:2rem; padding-bottom:3rem; }
.hero {
  padding:34px 38px; border-radius:26px; color:white; position:relative; overflow:hidden;
  background:linear-gradient(112deg,#4336a8 0%,#7257e9 48%,#d86ea9 100%);
  box-shadow:0 22px 55px rgba(88,69,190,.22);
  animation:heroIn .7s cubic-bezier(.2,.8,.2,1) both;
}
.hero:before,.hero:after { content:""; position:absolute; border-radius:50%; pointer-events:none; }
.hero:before { width:280px;height:280px;right:-70px;top:-150px;background:rgba(255,255,255,.13); }
.hero:after { width:150px;height:150px;right:145px;bottom:-105px;border:1px solid rgba(255,255,255,.22); }
.hero h1 { color:#fff !important; font-size:clamp(2rem,4vw,2.8rem); font-weight:800; margin:.35rem 0 0; }
.hero p { color:rgba(255,255,255,.88); font-size:1.02rem; margin:.45rem 0 0; }
@keyframes heroIn { from {opacity:0;transform:translateY(16px)} to {opacity:1;transform:translateY(0)} }
div[data-testid="stMetric"] {
  background:rgba(255,255,255,.88); border:1px solid rgba(224,226,245,.9);
  border-radius:20px; padding:18px 20px; box-shadow:0 10px 28px rgba(38,47,92,.055);
  transition:transform .22s ease,box-shadow .22s ease;
}
div[data-testid="stMetric"]:hover { transform:translateY(-3px);box-shadow:0 16px 32px rgba(38,47,92,.10); }
div[data-testid="stMetric"] label { color:#7a8499 !important; font-weight:600; }
div[data-testid="stMetric"] [data-testid="stMetricValue"] { color:#4536a4; font-family:'Manrope';font-weight:800; }
.stButton>button,.stDownloadButton>button {
  border:0; border-radius:13px; color:white; font-weight:700; padding:.68rem 1.1rem;
  background:linear-gradient(105deg,#5b49d6,#9366ec); transition:all .2s ease;
  box-shadow:0 7px 18px rgba(105,83,215,.17);
}
.stButton>button:hover,.stDownloadButton>button:hover {
  color:white; transform:translateY(-2px); box-shadow:0 11px 24px rgba(105,83,215,.28);
}
div[data-testid="stTextArea"] textarea,div[data-testid="stTextInput"] input {
  border-radius:14px; border:1px solid #e1e3f2; background:rgba(255,255,255,.94);
}
div[data-testid="stTextArea"] textarea:focus,div[data-testid="stTextInput"] input:focus {
  border-color:#927df4; box-shadow:0 0 0 3px rgba(116,87,245,.12);
}
div[data-testid="stSelectbox"] div[role="combobox"] { border-radius:12px; }
div[data-testid="stSidebar"] {
  background:linear-gradient(180deg,#efedff 0%,#f7f8ff 52%,#fff5fa 100%);
  border-right:1px solid rgba(220,219,242,.75);
}
div[data-testid="stSidebar"] .stRadio label { font-weight:600; }
.panel {
  background:rgba(255,255,255,.82); border:1px solid rgba(229,229,246,.95);
  border-radius:20px; padding:20px 22px; box-shadow:0 9px 26px rgba(35,44,90,.045);
  margin-bottom:13px; transition:transform .2s ease,box-shadow .2s ease;
}
.panel:hover { transform:translateY(-2px);box-shadow:0 14px 30px rgba(35,44,90,.075); }
.pill { display:inline-block;padding:5px 11px;border-radius:99px;font-size:.72rem;
  letter-spacing:.08em;font-weight:800;background:#eeebff;color:#6752d2; }
div[data-testid="stDataFrame"] { border:1px solid #e7e7f3;border-radius:15px;overflow:hidden; }
.stAlert { border-radius:14px; }
hr { border-color:rgba(221,222,239,.8); }
footer {visibility:hidden;}
@media (max-width: 700px) {
 .hero {padding:25px 22px;border-radius:20px;}
 .block-container {padding-left:1rem;padding-right:1rem;}
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
ensure_data_files(CSV_PATH, JSON_PATH)

def get_data():
    return load_reviews(CSV_PATH)

def header():
    st.markdown("""
    <div class="hero">
      <span style="font-weight:800;letter-spacing:2px;font-size:.72rem;opacity:.9;">PYTHON FOR GOOD&nbsp;&nbsp; / &nbsp;&nbsp;PROJECT 116</span>
      <h1>💬 MoodLens</h1>
      <p>Text Sentiment Studio — turn everyday words into meaningful insights.</p>
    </div>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 💜 MoodLens")
    st.caption("TEXT SENTIMENT STUDIO")
    page = st.radio("NAVIGATION", ["🏠 Dashboard", "✍️ Analyse Text", "🗂️ Review Library", "📊 Insights & Reports", "ℹ️ About Project"])
    st.divider()
    st.markdown("**Quick guide**")
    st.caption("1. Enter a review\n\n2. Analyse the sentiment\n\n3. Save it to your library\n\n4. Explore charts and reports")
    st.markdown("---")
    st.caption("Built with Python + Streamlit")

header()
reviews = get_data()
summary = sentiment_summary(reviews)

if page == "🏠 Dashboard":
    st.write("")
    st.subheader("Your sentiment overview")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total reviews", summary["total"])
    c2.metric("Positive", summary["positive"])
    c3.metric("Negative", summary["negative"])
    c4.metric("Neutral", summary["neutral"])
    st.write("")
    left,right = st.columns([1.15, .85])
    with left:
        st.markdown('<div class="panel"><span class="pill">WELCOME</span><h3>Understand the feeling behind the words.</h3><p>Analyse text, keep a searchable review collection, and view clear visual reports — all in one simple workspace.</p></div>', unsafe_allow_html=True)
        st.markdown("### ✨ What you can do")
        a,b = st.columns(2)
        with a:
            st.markdown('<div class="panel">✍️ **Analyse text**<br><small>Classify a review as positive, negative or neutral.</small></div>', unsafe_allow_html=True)
            st.markdown('<div class="panel">🔎 **Search reviews**<br><small>Find saved reviews with keywords.</small></div>', unsafe_allow_html=True)
        with b:
            st.markdown('<div class="panel">💾 **Save your data**<br><small>Keep records in CSV and JSON formats.</small></div>', unsafe_allow_html=True)
            st.markdown('<div class="panel">📈 **View insights**<br><small>Explore sentiment charts and summaries.</small></div>', unsafe_allow_html=True)
    with right:
        st.markdown("### Sentiment distribution")
        fig = create_sentiment_chart(reviews)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    st.caption("Tip: Start from **Analyse Text** to add your first review.")

elif page == "✍️ Analyse Text":
    st.subheader("Analyse a review")
    st.write("Type or paste a sentence below. MoodLens checks the words and estimates the overall sentiment.")
    with st.container(border=True):
        review_text = st.text_area("Your text", placeholder="Example: The delivery was quick and the product quality is excellent!", height=150, max_chars=2000)
        col1,col2 = st.columns([1,4])
        with col1:
            analyse = st.button("✨ Analyse sentiment", use_container_width=True)
        with col2:
            st.caption("No account or internet connection is needed for sentiment analysis.")
    if analyse:
        if not review_text.strip():
            st.warning("Please enter some text before analysing.")
        else:
            result = analyze_sentiment(review_text)
            st.session_state["last_analysis"] = {"text": review_text.strip(), **result}
    last = st.session_state.get("last_analysis")
    if last:
        st.write("")
        label = last["sentiment"]
        emoji = {"Positive":"😊","Negative":"🙁","Neutral":"😐"}[label]
        st.markdown(f'<div class="panel"><span class="pill">ANALYSIS RESULT</span><h2>{emoji} {label} sentiment</h2><p>{last["explanation"]}</p><b>Confidence estimate: {last["confidence"]}%</b></div>', unsafe_allow_html=True)
        st.progress(last["confidence"]/100)
        with st.expander("See the words that influenced the result"):
            st.write("Positive words:", ", ".join(last["positive_words"]) or "None found")
            st.write("Negative words:", ", ".join(last["negative_words"]) or "None found")
        if st.button("💾 Save this review"):
            record = {
                "id": str(uuid.uuid4())[:8],
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "text": last["text"],
                "sentiment": last["sentiment"],
                "score": last["score"],
                "confidence": last["confidence"]
            }
            save_review(record, CSV_PATH, JSON_PATH)
            st.success("Review saved successfully to CSV and JSON!")
            st.rerun()

elif page == "🗂️ Review Library":
    st.subheader("Review library")
    query = st.text_input("🔎 Search by keyword", placeholder="Try: excellent, slow, helpful...")
    filter_value = st.selectbox("Filter by sentiment", ["All", "Positive", "Negative", "Neutral"])
    df = pd.DataFrame(reviews)
    if not df.empty:
        if query.strip():
            df = df[df["text"].str.contains(query.strip(), case=False, na=False)]
        if filter_value != "All":
            df = df[df["sentiment"] == filter_value]
        st.caption(f"{len(df)} matching review(s)")
        st.dataframe(df[["date","text","sentiment","score"]], use_container_width=True, hide_index=True)
        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download filtered CSV", csv_data, "moodlens_reviews.csv", "text/csv")
    else:
        st.info("Your review library is empty. Analyse and save a review to see it here.")

elif page == "📊 Insights & Reports":
    st.subheader("Insights & reports")
    c1,c2,c3 = st.columns(3)
    c1.metric("Reviews analysed", summary["total"])
    c2.metric("Positive share", f'{summary["positive_pct"]}%')
    c3.metric("Negative share", f'{summary["negative_pct"]}%')
    left,right = st.columns(2)
    with left:
        st.markdown("#### Sentiment breakdown")
        fig = create_sentiment_chart(reviews)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    with right:
        st.markdown("#### Review activity")
        fig = create_timeline_chart(reviews)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    st.markdown("#### Export your data")
    e1,e2 = st.columns(2)
    with e1:
        if st.button("Create JSON export"):
            export_json(reviews, JSON_PATH)
            st.success(f"JSON data updated: {JSON_PATH.name}")
    with e2:
        json_bytes = json.dumps(reviews, indent=2, ensure_ascii=False).encode("utf-8")
        st.download_button("⬇️ Download JSON", json_bytes, "moodlens_reviews.json", "application/json")

elif page == "ℹ️ About Project":
    st.subheader("About MoodLens")
    st.markdown("""
    <div class="panel">
    <span class="pill">PROJECT 116 · PYTHON FOR GOOD</span>
    <h3>Text Sentiment Demo</h3>
    MoodLens is a beginner-friendly Python application that studies the words in a written review
    and labels its overall tone as Positive, Negative or Neutral.
    </div>
    """, unsafe_allow_html=True)
    st.markdown("### Technology used")
    st.write("- **Python 3.10+** — application logic")
    st.write("- **Streamlit** — interactive web interface")
    st.write("- **Pandas** — review data handling")
    st.write("- **Matplotlib** — charts and reports")
    st.write("- **CSV and JSON** — persistent data storage")
    st.markdown("### How sentiment detection works")
    st.write("This demo uses a simple word-based scoring method. It counts words from positive and negative vocabulary lists and compares the scores. It is an educational rule-based demo, not a human-level understanding system.")
    st.info("Important: Sentiment results are estimates. Context, sarcasm, spelling mistakes and mixed opinions may affect the result.")
    st.markdown("### Project modules")
    st.code("app.py          → Streamlit interface\nsentiment.py    → sentiment analysis logic\nstorage.py      → CSV and JSON storage\nreports.py      → statistics and charts\ndata/           → saved review records\ncharts/         → generated chart folder")

st.markdown("---")
st.caption("MoodLens · Text Sentiment Demo · Educational project")
