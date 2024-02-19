#!/usr/bin/python3
""" Gather data from an API """
import requests
from sys import argv


if __name__ == '__main__':
    user_id = argv[1]
    url = 'https://jsonplaceholder.typicode.com/'

    user = requests.get(url + 'users/{}'.format(user_id)).json()
    todos = requests.get(url + 'todos', params={'userId': user_id}).json()

    completed_tasks = [task for task in todos if task.get('completed')]

    print("Employee {} is done with tasks({}/{}):".format(
        user.get('name'), len(completed_tasks), len(todos)))

    for task in completed_tasks:
        print("\t {}".format(task.get('title')))
