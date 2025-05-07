# reddit_utils.py
import praw
import streamlit as st

# Initialize Reddit client using Streamlit secrets
reddit = praw.Reddit(
    client_id=st.secrets["REDDIT_CLIENT_ID"],
    client_secret=st.secrets["REDDIT_CLIENT_SECRET"],
    user_agent=st.secrets["REDDIT_USER_AGENT"],
)

def extract_post_id(url):
    try:
        parts = url.split("/")
        idx = parts.index("comments")
        return parts[idx + 1]
    except ValueError:
        return None

def get_top_comments_from_post(url, max_comments=10):
    """
    Extracts top-level insightful comments from a Reddit post URL.
    Priority is given to high-upvote and longer comments.
    """
    post_id = extract_post_id(url)
    if not post_id:
        return []

    submission = reddit.submission(id=post_id)
    submission.comments.replace_more(limit=0)

    # Sort by upvotes and content length
    comments = sorted(
        [c for c in submission.comments if hasattr(c, "body")],
        key=lambda x: (x.score, len(x.body.split())),
        reverse=True
    )

    top_comments = []
    for comment in comments:
        if comment.score >= 5 and len(comment.body.split()) > 10:
            top_comments.append(comment.body.strip())
            if len(top_comments) >= max_comments:
                break

    return top_comments
