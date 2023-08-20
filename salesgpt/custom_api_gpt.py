import json
import requests
import asyncio

class CustomAPI:
    def __init__(self, api_key, app_id):
        self.api_key = api_key
        self.app_id = app_id
        self.base_url = 'https://ai.aiwis.cn/api/openapi/v1/chat/completions'  # Replace with your actual base URL

    def chat(self, chatId, messages):
        headers = {
            'Authorization': f'Bearer {self.api_key}-{self.app_id}',
            'Content-Type': 'application/json'
        }
        payload = {
            "chatId": chatId,
            "stream": False,
            "detail": False,
            "messages": messages
        }
        response = requests.post(self.base_url, headers=headers, json=payload)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            print(f"Error: {response.status_code}")
            return None

    async def stream_chat(self, chatId, messages, onMessage):
        # This is a placeholder for the actual streaming logic.
        # You'll need to implement this based on how your API handles streaming.
        await asyncio.sleep(1)  # Simulate some delay
        onMessage("Simulated response from the streaming API.")
        return "Simulated response"
