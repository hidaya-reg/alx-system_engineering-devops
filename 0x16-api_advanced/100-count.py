#!/usr/bin/python3
"""Queries the Reddit API"""

import requests

def count_words(subreddit, word_list, word_count=None, after=None):
    """returns the count of words in word_list"""
    
    if word_count is None:
        word_count = {word.lower(): 0 for word in word_list}

    headers = {"User-Agent": "My-User-Agent"}
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    params = {"after": after}
    
    response = requests.get(url, headers=headers, params=params, allow_redirects=False)
    
    if response.status_code != 200:
        return None

    data = response.json().get("data", {})
    children = data.get("children", [])

    for child in children:
        title = child.get("data", {}).get("title", "").lower().split()
        for word in word_list:
            word_lower = word.lower()
            word_count[word_lower] += title.count(word_lower)

    after = data.get("after")
    if after:
        return count_words(subreddit, word_list, word_count, after)
    
    sorted_word_count = sorted(word_count.items(), key=lambda kv: (-kv[1], kv[0]))
    for word, count in sorted_word_count:
        if count > 0:
            print(f'{word}: {count}')
