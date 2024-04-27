from datetime import datetime, timedelta
import json

with open("./910667146185572382_20240426_221430.json", "r") as file:
    data = json.load(file)

seven_days_ago = datetime.utcnow() - timedelta(days=7)

for message in data["messages"]:
    message_timestamp = datetime.fromisoformat(
        message["timestamp"].replace("Z", "+00:00")
    ).replace(tzinfo=None)
    if message_timestamp < seven_days_ago:
        print(f"Message ID {message['id']} is older than 7 days.")
    else:
        print(f"Message ID {message['id']} is within the last 7 days.")
