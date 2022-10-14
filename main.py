from flask import request
from flask import 
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import requests

app = Flask(__name__)
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
    payload = '{"text": "%s"}' % message
    print(payload)
    response = requests.post(
        "https://hooks.slack.com/services/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",
        data=payload
    )
    print(response.text)


if __name__ == '__main__':
    app.run(debug=True)
