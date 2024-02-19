#!/usr/bin/python3
"""Script to export data in JSON format"""

import json
import requests
import sys

if __name__ == "__main__":
    user_id = sys.argv[1]

    base_url = 'https://jsonplaceholder.typicode.com'
    user_url = f'{base_url}/users/{user_id}'
    tasks_url = f'{base_url}/todos?userId={user_id}'

    response_user = requests.get(user_url)
    user_data = response_user.json()
    username = user_data[0].get('username')

    response_todo = requests.get(tasks_url)
    todo_data = response_todo.json()

    data_to_export = {
        str(user_id): [
            {
                "task": task['title'],
                "completed": task['completed'],
                "username": username
            }
            for task in todo_data
        ]
    }

    with open(f"{user_id}.json", 'w') as json_file:
        json.dump(data_to_export, json_file, indent=4)
