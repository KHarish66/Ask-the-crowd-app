# app.py
import os
import requests
import time
import streamlit as st
from dotenv import load_dotenv
from google_search import search_reddit_threads
from reddit_utils import get_top_comments_from_post

# Loading environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQCLOUD_API_KEY")

# GroqCloud endpoint
model_endpoint = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}


def is_product_suggestion(query: str) -> bool:
    product_keywords = ["best", "recommend", "suggest", "which", "top", "buy", "vs", "under", "between"]
    return any(kw in query.lower() for kw in product_keywords)


# Summarize Reddit data using Groq
def summarize_reddit_data(reddit_data, query, thread_urls):
    url_mapping = "\n".join([f"[ref{i + 1}]: {url}" for i, url in enumerate(thread_urls)])

    if is_product_suggestion(query):
        prompt = (
            "You're an assistant summarizing real user discussions from Reddit.\n"
            f"User's question: '{query}'\n\n"
            "Based on the Reddit comments below, provide clear product-related insights.\n"
            "- Present each point as a clear and concise bullet; use emojis only if they add clarity or enhance understanding.\n"
            "- After each insight, include a direct link to the source thread like (**[Source](<actual_link>)**).\n"
            "- Provide exactly 5 insights. Use a variety of threads if possible.\n"
            "- Do not include unrelated content or mention thread numbers.\n\n"
            f"Reddit data:\n{reddit_data}\n\n"
            f"Thread sources:\n{url_mapping}"
        )
    else:
        prompt = (
            "You're an assistant summarizing Reddit threads to extract meaningful user insights.\n"
            f"User's question: '{query}'\n\n"
            "Summarize 5 important points clearly. Attach (**[Source](<actual_link>)**) directly after each insight.\n"
            "Only include relevant points. Use emojis only if they enhance clarity. Keep it readable and professional.\n\n"
            f"Reddit data:\n{reddit_data}\n\n"
            f"Thread sources:\n{url_mapping}"
        )

    input_data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}]
    }

    for attempt in range(5):
        try:
            res = requests.post(model_endpoint, headers=headers, json=input_data)
            if res.status_code == 200:
                return res.json().get("choices", [{}])[0].get("message", {}).get("content", "⚠ No summary found.")
            else:
                print(f"API error: {res.status_code} - {res.text}")
                return "⚠ Failed to summarize insights."
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            time.sleep(5)
    return "⚠ Max retries exceeded."


# Streamlit App
st.set_page_config(page_title=" Ask the Crowd", page_icon="💬")
st.title("💬  Ask the Crowd")

# Disclaimer Section
st.markdown(
    """
    💡 **The insights provided in this application are generated based on user discussions from Reddit. While we strive to offer relevant and accurate summaries, the content is sourced from a variety of personal opinions and may not always be fact-checked or reliable.**
    """
)

query = st.text_input("Enter your question:")

if st.button("Submit") and query:
    with st.spinner("🔍 Searching Reddit..."):
        reddit_urls = search_reddit_threads(query)

        if not reddit_urls:
            st.warning("❌ No Reddit threads found.")
        else:
            all_comments = ""
            any_data = False

            for url in reddit_urls[:5]:
                comments = get_top_comments_from_post(url, max_comments=5)
                if comments:
                    any_data = True
                    all_comments += f"\nThread: {url}\n"
                    for comment in comments:
                        all_comments += f"- {comment}\n"

            if not any_data:
                st.info("ℹ No useful insights found in any thread.")
            else:
                with st.spinner("🧠 Summarizing Reddit insights..."):
                    final_summary = summarize_reddit_data(all_comments, query, reddit_urls[:5])

                if final_summary:
                    st.subheader("📌 Insights from Reddit")
                    st.markdown(final_summary, unsafe_allow_html=True)
