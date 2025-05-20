import hashlib
import hmac
import os
import threading

from flask import Flask, request

from bot_main import PrOrErClient
from dotenv import load_dotenv

load_dotenv()

client = PrOrErClient()


def verify_signature(incoming):
    signature = incoming.headers.get('X-Hub-Signature-256')
    if signature is None:
        return False

    sha_name, signature = signature.split('=')
    if sha_name != 'sha256':
        return False

    mac = hmac.new(os.getenv("GITHUB_SECRET").encode(), msg=incoming.data, digestmod=hashlib.sha256)
    return hmac.compare_digest(mac.hexdigest(), signature)


app = Flask(__name__)


def run_bot():
    client.run(os.getenv("TOKEN"))


@app.route("/")
def index():
    return "Bot is running!"


@app.route('/github', methods=['POST'])
async def github():
    data = request.json
    if not verify_signature(request):
        return "Invalid signature", 403

    event = request.headers.get('X-GitHub-Event')
    if event == 'release':
        await client.on_github_hook(data)

    return "", 200


if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=10000)
