import asyncio
import hashlib
import hmac
import os
import threading
from quart import Quart, request
from bot_main import PrOrErClient
from dotenv import load_dotenv

load_dotenv()
port = int(os.environ.get("PORT", 10000))
app = Quart(__name__)
client = PrOrErClient()


async def verify_signature(incoming):
    signature = incoming.headers.get('X-Hub-Signature-256')
    if signature is None:
        return False

    sha_name, signature = signature.split('=')
    if sha_name != 'sha256':
        return False

    data = await incoming.data

    mac = hmac.new(os.getenv("GITHUB_SECRET").encode(), msg=data, digestmod=hashlib.sha256)
    return hmac.compare_digest(mac.hexdigest(), signature)


async def run_bot():
    await client.start(os.getenv("TOKEN"))


@app.route("/")
def index():
    return "Bot is running!"


@app.route('/github', methods=['POST'])
async def github():
    data = await request.json
    # if not await verify_signature(request):
    #     return "Invalid signature", 403

    event = request.headers.get('X-GitHub-Event')
    if event == 'release' and data['action'] == 'prereleased':
        asyncio.create_task(client.on_github_hook(data))
        return "", 200

    return "Event not handled", 400

async def main():
    await asyncio.gather(
        run_bot(),
        app.run_task(host='0.0.0.0',port=port)
    )
#todo create roles for the feature request and bug report and ping them
if __name__ == "__main__":
    asyncio.run(main())