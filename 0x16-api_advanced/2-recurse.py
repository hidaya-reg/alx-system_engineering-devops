#!/usr/bin/python3
"""hot articles for a given subreddit"""
import requests


def recurse(subreddit, hot_list=None, after=None):
    """list containing the titles of all hot articles"""
    if hot_list is None:
        hot_list = []

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {'User-Agent': 'MyUserAgent'}
    params = {'limit': 100, 'after': after}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        return None

    data = response.json().get("data")
    if not data:
        return None

    children = data.get("children", [])
    for child in children:
        title = child.get("data", {}).get("title")
        hot_list.append(title)

    after = data.get("after")
    if after:
        return recurse(subreddit, hot_list, after)

    return hot_list
