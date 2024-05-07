#!/usr/bin/python3
""" Queries the Reddit API"""


def number_of_subscribers(subreddit):
    """
    Queries the Reddit API and returns number of subscribers for subreddit.

    Args:
        subreddit (str): The name of the subreddit to query.

    Returns:
        int: The number of subscribers for the given subreddit.
        Returns 0 if the subreddit is invalid.
    """
    import requests


    url = "https://www.reddit.com/r/{}/about.json".format(subreddit)
    headers = {'User-Agent': 'MyBot/0.0.1'}

    response = requests.get(url, headers=headers, allow_redirects=False)

    if response.status_code >= 300:
        return 0
    return response.json().get("data").get("subscribers")
