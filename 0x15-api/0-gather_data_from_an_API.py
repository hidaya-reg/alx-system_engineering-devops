#!/usr/bin/python3
""" Gather data from an API """
import requests
from sys import argv


def gather_data():
    """ Gather data from an API """
    if len(argv) < 2:
        exit()

    user_id = argv[1]
    users_url = "https://jsonplaceholder.typicode.com/users"
    todos_url = "https://jsonplaceholder.typicode.com/todos"

    todos_response = requests.get(f"{todos_url}?userId={user_id}")
    todos_data = todos_response.json()

    user_response = requests.get(f"{users_url}?id={user_id}")
    user_data = user_response.json()
    user_name = user_data[0]["name"]
    completed_tasks = [task for task in todos_data if task["completed"]]
    completed = len(completed_tasks)
    total = len(todos_data)
    print("Employee {} is done with tasks ({}/{}):".format(
        user_name, completed, total))
    for task in completed_tasks:
        print("\t{}".format(task['title']))


if __name__ == '__main__':
    gather_data()
