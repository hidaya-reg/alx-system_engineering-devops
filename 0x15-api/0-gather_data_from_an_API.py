#!/usr/bin/python3
""" Gather data from an API """
import requests
from sys import argv


def gather_data():
    """ Gather data from an API """
    if len(argv) < 2:
        exit()

    user_id = argv[1]
    url = 'https://jsonplaceholder.typicode.com/'
    todos_response = requests.get(f"{url}/todos?userId={user_id}")
    todos_data = todos_response.json()

    user_response = requests.get(f"{url}/users?id={user_id}")
    user_data = user_response.json()
    user_name = user_data[0]["name"]
    completed_tasks = [task for task in todos_data if task["completed"]]
    completed = len(completed_tasks)
    total = len(todos_data)
    print("Employee {} is done with tasks ({}/{}):".format(user_name, completed, total))
    for task in completed_tasks:
        print("\t{}".format(task['title']))


if __name__ == '__main__':
    gather_data()
