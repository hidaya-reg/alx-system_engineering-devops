#!/usr/bin/python3
"""
Script to export data in JSON format for all employees
"""

import json
import requests
from sys import argv

if __name__ == "__main__":
    base_url = 'https://jsonplaceholder.typicode.com'

    # Get users
    users = requests.get(f'{base_url}/users').json()

    # Get todos
    todos = requests.get(f'{base_url}/todos').json()

    # Create dictionary to store user tasks
    tasks_by_user = {}

    for user in users:
        user_id = user.get('id')
        username = user.get('username')
        tasks = [{"username": username,
                  "task": task.get('title'),
                  "completed": task.get('completed')}
                 for task in todos if task.get('userId') == user_id]
        tasks_by_user[str(user_id)] = tasks

    # Export data to JSON file
    with open('todo_all_employees.json', 'w') as json_file:
        json.dump(tasks_by_user, json_file)
