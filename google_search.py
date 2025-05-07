# google_search.py
from googleapiclient.discovery import build
from config import GOOGLE_API_KEY, GOOGLE_CSE_ID

def search_reddit_threads(query, max_results=5):
    service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
    result = service.cse().list(q=f"{query} site:reddit.com", cx=GOOGLE_CSE_ID).execute()

    links = []
    for item in result.get('items', [])[:max_results]:
        if "reddit.com/r/" in item["link"]:
            links.append(item["link"].split("?")[0])  # clean URL

    return links
