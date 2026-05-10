import os
import requests


def send_line_message(message: str) -> None:
    channel_access_token = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
    user_id = os.environ["LINE_USER_ID"]

    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {channel_access_token}",
    }
    payload = {
        "to": user_id,
        "messages": [{"type": "text", "text": message}],
    }

    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
