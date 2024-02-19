#!/usr/bin/python3
"""For a given employee ID, returns information about
their TODO list progress
"""

import sys
import requests

def fetch_todo_progress(employee_id):
    base_url = 'https://jsonplaceholder.typicode.com'
    user_url = f'{base_url}/users/{employee_id}'
    todos_url = f'{base_url}/todos?userId={employee_id}'

    try:
        user_response = requests.get(user_url)
        todos_response = requests.get(todos_url)

        if user_response.status_code != 200 or todos_response.status_code != 200:
            print('Failed to fetch data. Please try again later.')
            return

        user_data = user_response.json()
        todos_data = todos_response.json()

        employee_name = user_data['name']
        total_tasks = len(todos_data)
        done_tasks = [task for task in todos_data if task['completed']]
        num_done_tasks = len(done_tasks)

        print(f"Employee {employee_name} is done with tasks({num_done_tasks}/{total_tasks}):")

        for task in done_tasks:
            print(f"\t{task['title']}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <employee_id>")
        sys.exit(1)

    employee_id = int(sys.argv[1])
    fetch_todo_progress(employee_id)
