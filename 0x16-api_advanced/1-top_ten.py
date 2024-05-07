#!/usr/bin/python3
"""top 10 hot posts"""
import requests


def top_ten(subreddit):
    """
    first 10 hot posts listed for a given subreddit.

    Args:
        subreddit (str): The name of the subreddit to query.
    """
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=10"
    headers = {'User-Agent': 'MyUserAgent'}

    response = requests.get(url, headers=headers, allow_redirects=False )

    if response.status_code != 200:
        print("None")
        return

    data = response.json().get("data")
    if not data:
        print("None")
        return

    children = data.get("children", [])

    for child in children:
        title = child.get("data", {}).get("title")
        print(title)
