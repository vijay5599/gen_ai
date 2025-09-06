from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

from .server import app
import uvicorn


def main():
    uvicorn.run(app, host="localhost", port=8000)


main()
