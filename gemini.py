from google import genai


clinet = genai.Client(api_key="AIzaSyCaOYBSU1HVdM3702BljkRuFXxBApuk68s")

response = clinet.models.generate_content(
    model="gemini-2.5-flash",
    contents="How AI works.",
)

print("Chat completion created", response.text)
