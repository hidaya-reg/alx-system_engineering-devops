#!/usr/bin/python3
"""
Extended Python script that fetches info about a given employee using an API
and exports it in CSV format
"""

import csv
import requests
import sys

BASE_URL = 'https://jsonplaceholder.typicode.com'


def export_to_csv(user_id):
    # Get user info
    user_response = requests.get(f"{BASE_URL}/users/{user_id}")
    user_data = user_response.json()
    username = user_data.get('username')

    # Get user's todo tasks
    tasks_response = requests.get(f"{BASE_URL}/todos?userId={user_id}")
    tasks_data = tasks_response.json()

    # Write to CSV
    filename = f"{user_id}.csv"
    with open(filename, 'w', newline='', encoding='UTF8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(
            ["USER_ID", "USERNAME", "TASK_COMPLETED_STATUS", "TASK_TITLE"]
        )
        for task in tasks_data:
            csv_writer.writerow(
                [user_id, username, task['completed'], task['title']]
            )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <user_id>")
        sys.exit(1)

    user_id = sys.argv[1]
    export_to_csv(user_id)
