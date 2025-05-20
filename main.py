import os
from bot_main import PrOrErClient
from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv('.env')
    client = PrOrErClient()
    client.run(os.getenv("TOKEN"))