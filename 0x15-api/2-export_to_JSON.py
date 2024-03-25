#!/usr/bin/python3
""" Gather data from an API and export to JSON """
import requests
import json
from sys import argv


def export_to_json(user_id):
    """ Gather data from an API and export to JSON """
    users_url = "https://jsonplaceholder.typicode.com/users"
    todos_url = "https://jsonplaceholder.typicode.com/todos"

    todos_response = requests.get(f"{todos_url}?userId={user_id}")
    todos_data = todos_response.json()

    user_response = requests.get(f"{users_url}?id={user_id}")
    user_data = user_response.json()
    username = user_data[0]["username"]

    user_tasks = []
    for task in todos_data:
        user_tasks.append({
            "task": task["title"],
            "completed": task["completed"],
            "username": username
        })

    json_file_name = f"{user_id}.json"

    with open(json_file_name, mode='w') as file:
        json.dump({user_id: user_tasks}, file)


if __name__ == '__main__':
    if len(argv) < 2:
        exit()

    user_id = argv[1]
    export_to_json(user_id)
