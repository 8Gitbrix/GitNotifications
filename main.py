import os
from flask import request
from flask import Flask
from flask_ngrok import run_with_ngrok
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv(".env")
run_with_ngrok(app)
client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])


@app.route('/')
def api_root():
    return 'Hello World'


@app.route('/pr-comment', methods=['POST'])
def prComment():
    if request.headers['Content-Type'] == 'application/json':
        content = request.json
        message = f'{content["review"]["user"]["login"]} said {content["review"]["body"]}'
        sendComment(message)
        return content


def sendComment(message: str):
    try:
        response = client.chat_postMessage(channel='#general', text=message)
        assert response["message"]["text"] == "Hello world!"
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")



if __name__ == '__main__':
    app.run(debug=True)
