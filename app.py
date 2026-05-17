import streamlit as st
from news_fetcher import fetch_news
from gemini_processor import analyze_article

st.set_page_config(page_title="AI News Intelligence", page_icon="📰", layout="wide")

st.title("📰 AI News Intelligence System")
st.markdown("Powered by **Google Gemini** · Real-time sentiment, summary & keyword extraction")

# Sidebar controls
with st.sidebar:
    st.header("🔧 Settings")
    topic = st.text_input("Search Topic", value="Artificial Intelligence")
    num_articles = st.slider("Number of Articles", min_value=3, max_value=10, value=5)
    analyze_btn = st.button("🔍 Analyze News", use_container_width=True)

# Sentiment color helper
def sentiment_color(sentiment: str) -> str:
    return {"Positive": "🟢", "Negative": "🔴", "Neutral": "🟡"}.get(sentiment, "🟡")

if analyze_btn:
    with st.spinner(f"Fetching latest news on '{topic}'..."):
        articles = fetch_news(topic, num_articles)

    if not articles:
        st.error("No articles found. Try a different topic or check your NewsAPI key.")
    else:
        st.success(f"Found {len(articles)} articles. Analyzing with Gemini...")

        for i, article in enumerate(articles):
            with st.spinner(f"Analyzing article {i+1} of {len(articles)}..."):
                content = f"{article['description']} {article['content']}"
                analysis = analyze_article(article["title"], content)

            with st.expander(f"{sentiment_color(analysis['sentiment'])}  {article['title']}", expanded=False):
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.markdown("**📝 Summary**")
                    st.write(analysis["summary"])

                    st.markdown("**🔑 Keywords**")
                    st.write(" · ".join(analysis["keywords"]))

                with col2:
                    st.markdown("**📊 Sentiment**")
                    score = analysis["sentiment_score"]
                    st.metric(
                        label=analysis["sentiment"],
                        value=f"{score:+.2f}",
                        delta=None
                    )
                    st.progress((score + 1) / 2)  # normalize -1→1 to 0→1

                st.markdown(f"🗞️ Source: **{article['source']}** · 🕒 {article['publishedAt'][:10]}")
                st.markdown(f"[Read full article →]({article['url']})")