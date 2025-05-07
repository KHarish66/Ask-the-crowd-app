# Ask-the-crowd
# Ask the crowd — Extract Real Insights from Reddit Discussions

## Problem

The modern internet is saturated with:
- SEO-optimized articles,
- Sponsored content,
- Biased and affiliate-based recommendations.

Users seeking **authentic, experience-based advice** are turning to Reddit. But even Reddit comes with its own challenges:
- Thousands of scattered threads,
- Unstructured comment chains,
- No easy way to extract the best insights.

## 💡 Solution

**Ask-the-crowd** is a powerful Streamlit-based app that distills genuine community wisdom from Reddit.

### 🔍 How It Works
Ask Redditors:
- Leverages **Google Custom Search** to locate relevant Reddit threads.
- Uses **Reddit API (PRAW)** to fetch highly upvoted, meaningful comments.
- Applies **GroqCloud (LLaMA model)** for summarizing discussions.
- Presents results cleanly via a **Streamlit interface**.

## 🛠️ Tech Stack

- **🔍 Google Custom Search API** – to find Reddit threads
- **🧵 Reddit API (PRAW)** – to fetch insightful, upvoted comments
- **🧠 GroqCloud LLaMA API** – for intelligent summarization
- **📦 Streamlit** – to build a user-friendly web UI

## 🚀 Features

- ✅ Input any query (e.g., "Best mechanical keyboard under ₹5000")
- ✅ Google-powered search for Reddit discussions
- ✅ Filters meaningful top comments using Reddit’s score
- ✅ Summarizes raw comments into structured insights
- ✅ Displays both summary and original thread links

