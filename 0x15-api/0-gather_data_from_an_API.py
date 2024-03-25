#!/usr/bin/python3
""" Gather data from an API """
import requests
from sys import argv


def gather_data(user_id):
    """ Gather data from an API """
    name = None
    completed = 0
    total = 0
    users_url = "https://jsonplaceholder.typicode.com/users"
    todos_url = "https://jsonplaceholder.typicode.com/todos"

    todos_data = requests.get(f"{todos_url}?userId={user_id}").json()

    user_data = requests.get(f"{users_url}?id={user_id}").json()

    user_name = user_data[0]["name"]
    completed_tasks = [task for task in todos_data if task["completed"]]
    completed = len(completed_tasks)
    total = len(todos_data)
    print("Employee {} is done with tasks({}/{}):".format(
        user_name, completed, total))
    for task in completed_tasks:
        print("\t{}".format(task['title']))


if __name__ == '__main__':
    if len(argv) < 2:
        exit()
    user_id = int(argv[1])
    gather_data(user_id)
