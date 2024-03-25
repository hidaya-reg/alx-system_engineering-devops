#!/usr/bin/python3
""" Gather data from an API """
import requests
from sys import argv


def gather_data(user_id):
    """ Gather data from an API """
    completed = 0
    total = 0

    users_url = "https://jsonplaceholder.typicode.com/users"
    todos_url = "https://jsonplaceholder.typicode.com/todos"

    todos_data = requests.get(todos_url).json()

    users_data = requests.get(users_url).json()

    name = None
    for user in users_data:

        if user["id"] == int(user_id):
            name = user["name"]

    for todo in todos_data:
        if todo['userId'] == user_id:
            total += 1
        if (todo['completed'] and todo['userId'] == user_id):
            completed += 1

    print("Employee {} is done with tasks ({}/{}):".format(
        name, completed, total))
    for todo in todos_data:
        if todo["userId"] == user_id and todo['completed']:
            print("\t{}".format(todo['title']))


if __name__ == '__main__':
    if len(argv) < 2:
        exit()
    user_id = int(argv[1])
    gather_data(user_id)
