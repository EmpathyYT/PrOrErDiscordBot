import os
import threading

from flask import Flask

from bot_main import PrOrErClient
from dotenv import load_dotenv

app = Flask(__name__)


def run_bot():
    client = PrOrErClient()
    client.run(os.getenv("TOKEN"))


@app.route("/")
def index():
    return "Bot is running!"


if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=10000)
