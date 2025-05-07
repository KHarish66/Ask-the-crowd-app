import requests
import streamlit as st

def search_reddit_threads(query, num_results=5):
    api_key = st.secrets["GOOGLE_API_KEY"]
    cse_id = st.secrets["GOOGLE_CSE_ID"]

    search_url = "https://customsearch.googleapis.com/customsearch/v1"
    params = {
        "q": f"{query} site:reddit.com",
        "key": api_key,
        "cx": cse_id,
        "num": num_results,
    }

    response = requests.get(search_url, params=params)
    response.raise_for_status()
    results = response.json()

    return [item["link"] for item in results.get("items", [])]
