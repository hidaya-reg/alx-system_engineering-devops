#!/usr/bin/python3
"""For a given employee ID, returns information about
their TODO list progress"""

import requests
import sys


def get_employee_todo_progress(employee_id):
    user_response = requests.get(
        f"https://jsonplaceholder.typicode.com/users/{employee_id}"
    )
    user_data = user_response.json()
    name = user_data.get('name')

    todos_response = requests.get(
        f'https://jsonplaceholder.typicode.com/todos?userId={employee_id}'
    )
    todos_data = todos_response.json()

    total_tasks = len(todos_data)
    completed_tasks = [task for task in todos_data if task.get('completed')]
    num_completed_tasks = len(completed_tasks)

    print(f'Employee {name} is done with tasks({num_completed_tasks}/{total_tasks}):')
    for task in completed_tasks:
        print(f'\t{task["title"]}')


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <employee_id>")
        sys.exit(1)

    employee_id = sys.argv[1]
    get_employee_todo_progress(employee_id)
