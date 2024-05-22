import requests
import uuid
from datetime import datetime, timedelta, timezone

def get_url():
    with open("./api.txt", "r") as f:
        return f.readline()

def validate_id(id):
    try:
        uuid.UUID(str(id))
        return True
    except ValueError:
        return False


def send_message(msg_json, user_id):
    if not validate_id(user_id):
        print("ERROR")
        return 1
    # construct HTTP POST request
    response = requests.post(get_url() + 'messages/' + user_id, json=msg_json)
    return 0

def recieve_messages(user_id):
    # send HTTP GET request
    response = requests.get(get_url() + f'messages/{user_id}')
    if response.status_code == 400:
        print("Error recieving messages")
        return 1
    return 0
