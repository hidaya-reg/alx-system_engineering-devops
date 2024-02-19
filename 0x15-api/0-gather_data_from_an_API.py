#!/usr/bin/python3
"""Gather data from an API"""

import requests
import sys


def fetch_employee_data(employee_id):
    """Fetches employee data from the API"""
    base_url = "https://jsonplaceholder.typicode.com"
    employee_url = f"{base_url}/users/{employee_id}"
    todo_url = f"{employee_url}/todos"

    # Fetch employee data
    employee_response = requests.get(employee_url)
    employee_data = employee_response.json()
    employee_name = employee_data.get('name')

    # Fetch todo tasks
    todo_response = requests.get(todo_url)
    todo_tasks = todo_response.json()

    return employee_name, todo_tasks


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <employee_id>")
        sys.exit(1)

    employee_id = sys.argv[1]

    try:
        employee_name, todo_tasks = fetch_employee_data(employee_id)
        total_tasks = len(todo_tasks)
        completed_tasks = sum(task['completed'] for task in todo_tasks)

        print(f"Employee {employee_name} is done with tasks({completed_tasks}/"
              f"{total_tasks}):")
        for task in todo_tasks:
            if task['completed']:
                print(f"\t{task['title']}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
