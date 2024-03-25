#!/usr/bin/python3
""" Gather data from an API and export to CSV """
import requests
import csv
from sys import argv


def export_to_csv(user_id):
    """ Gather data from an API and export to CSV """
    users_url = "https://jsonplaceholder.typicode.com/users"
    todos_url = "https://jsonplaceholder.typicode.com/todos"

    todos_response = requests.get(f"{todos_url}?userId={user_id}")
    todos_data = todos_response.json()

    user_response = requests.get(f"{users_url}?id={user_id}")
    user_data = user_response.json()
    username = user_data[0]["username"]

    csv_file_name = f"{user_id}.csv"

    with open(csv_file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        for task in todos_data:
            writer.writerow([user_id, username, task["completed"], task["title"]])


if __name__ == '__main__':
    if len(argv) < 2:
        exit()

    user_id = argv[1]
    export_to_csv(user_id)

