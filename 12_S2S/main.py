import speech_recognition as sr
from dotenv import load_dotenv
from openai import OpenAI
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer
import asyncio

load_dotenv()

client = OpenAI()
async_client = AsyncOpenAI()


async def tts(speech_text: str):
    async with async_client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=speech_text,
        instructions="Speak like a professional voice agent",
        response_format="pcm",
    ) as response:
        await LocalAudioPlayer().play(response)


def main():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please say something")
        r.adjust_for_ambient_noise(source)
        r.threshold = 2

        SYSTEM_PROMPT = """You are an expert voice agent.You are given transcript what user has said using voice.
            You need to output as if are an voice agent and whatever user speak will be converted to audio usinf AI and played back to user."""

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
        ]
        while True:
            audio = r.listen(source)
            print("You said: " + r.recognize_google(audio))

            messages.append({"role": "user", "content": r.recognize_google(audio)})
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "user", "content": r.recognize_google(audio)},
                ],
            )
            print("Response:", response.choices[0].message.content)
            asyncio.run(tts(response.choices[0].message.content))


main()
