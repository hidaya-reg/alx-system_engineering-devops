#!/usr/bin/python3
""" Queries the Reddit API"""
import json
import requests


def number_of_subscribers(subreddit):
    """returns number of subscribers for subreddit"""
    url = "https://www.reddit.com/r/{}/about.json".format(subreddit)
    headers = {'User-Agent': 'MyUserAgent'}

    response = requests.get(url, headers=headers, allow_redirects=False)

    if response.status_code == 200:
        return response.json().get("data").get("subscribers")

    return 0
