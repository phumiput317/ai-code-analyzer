import time

from google import genai

from config import (
    GEMINI_API_KEY,
    MODEL
)


client = genai.Client(
    api_key=GEMINI_API_KEY
)


def ask_ai(prompt):

    max_retries = 3

    for attempt in range(max_retries):

        try:

            response = client.models.generate_content(
                model=MODEL,
                contents=prompt
            )

            return response.text

        except Exception as e:

            error_message = str(e)

            if (
                "503" in error_message
                or
                "UNAVAILABLE" in error_message
            ):

                if attempt < max_retries - 1:

                    wait_time = (
                        attempt + 1
                    ) * 5

                    print(
                        f"Gemini busy. "
                        f"Retrying in "
                        f"{wait_time} seconds..."
                    )

                    time.sleep(
                        wait_time
                    )

                    continue

            return f"AI ERROR: {e}"

    return (
        "AI service unavailable."
    )