#!/usr/bin/python3
"""Script that fetches info about a given employee using an API
and exports it in JSON format
"""

import json
import requests
import sys

BASE_URL = 'https://jsonplaceholder.typicode.com'

if __name__ == "__main__":
    # Check if user ID is provided as argument
    if len(sys.argv) != 2:
        print("Usage: python script.py <user_id>")
        sys.exit(1)

    user_id = sys.argv[1]

    # Get user info
    user_response = requests.get(f"{BASE_URL}/users/{user_id}")
    user_data = user_response.json()

    # Extract user data
    user_name = user_data[0].get('username')

    # Get user's todo tasks
    tasks_response = requests.get(f"{BASE_URL}/todos?userId={user_id}")
    tasks_data = tasks_response.json()

    # Build JSON data
    user_tasks = []
    for task in tasks_data:
        user_tasks.append({
            "task": task['title'],
            "completed": task['completed'],
            "username": user_name
        })

    # Write JSON data to file
    filename = f"{user_id}.json"
    with open(filename, 'w', encoding='UTF8') as json_file:
        json.dump({user_id: user_tasks}, json_file, indent=4)
