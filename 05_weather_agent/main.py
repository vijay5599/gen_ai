from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()  # take environment variables from .env.


client = OpenAI()


def main():
    user_query = input("Enter your query > ")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": user_query,
            }
        ],
    )

    print("🤖", response.choices[0].message.content)


main()
