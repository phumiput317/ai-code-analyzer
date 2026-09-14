from google import genai

API_KEY = "AQ.Ab8RN6I_ovIOnSegQ--1Dd0hQU4UONcPRc5nXmPDeHW8jHx3Wg"

client = genai.Client(api_key=API_KEY)

interaction = client.interactions.create(
    model="gemini-3.6-flash",
    input="Say Hello"
)

print(interaction.output_text)