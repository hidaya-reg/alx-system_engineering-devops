#!/usr/bin/python3
""" Gather data from an API and export to JSON """
import requests
import json


def todo_all_employees():
    """ Gather data from an API and export to JSON """
    users_url = "https://jsonplaceholder.typicode.com/users"
    todos_url = "https://jsonplaceholder.typicode.com/todos"

    response_users = requests.get(users_url)
    users = response_users.json()

    todos_response = requests.get(todos_url)
    todos = todos_response.json()

    user_tasks = {}

    for user in users:
        user_id = user.get('id')
        username = user.get('username')
        user_tasks[user_id] = []

        for todo in todos:
            if todo.get('userId') == user_id:
                task = {
                        "username": username,
                        "task": todo.get('title'),
                        "completed": todo.get('completed')
                        }
                user_tasks[user_id].append(task)


    with open('todo_all_employees.json', mode='w') as file:
        json.dump(user_tasks, file)


if __name__ == '__main__':
    todo_all_employees()
