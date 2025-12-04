"""

The Gemini API Access

To use this you must create a .env file in the root directory with the `GOOGLE_API_KEY` inside.

"""

import requests
from requests.exceptions import RequestException, HTTPError
import os
from dotenv import load_dotenv

def configuration():
    """
    Load the `GOOGLE_API_KEY` from the .env File
    """
    load_dotenv()
    __key: str | None = os.getenv("GOOGLE_API_KEY")
    return f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={__key}"

API_ENDPOINT = configuration()

def create_payload(text: str) -> dict[str, list[dict[str, list[dict[str, str]]]]]:
    """
    Create & get the JSON structure required for the Gemini API
    """
    return {
        "contents": [
            {
                "parts": [
                    {"text": text}
                ]
            }
        ]
    }

def send_gemini(text: str) -> dict:
    """
    Sends a POST Request to gemini & receives the generated `text` from it.
    
    Returns the gemini result -> `str`.
    
    If a error occoures: 
        returns a dict that only contains the `error`.
    """
    
    payload = create_payload(text)
    
    try:
        response = requests.post(API_ENDPOINT, json=payload, timeout=10)
        response.raise_for_status()  # Raises an exception for HTTP error status codes (4xx or 5xx)
        json_response = response.json()
        generated_text = json_response["candidates"][0]["content"]["parts"][0]["text"]
        return {'text': generated_text}
    except HTTPError as http_err:
        return {
            'error': f'HTTPError - Gemini - {http_err.response.status_code}\nPlease check your API key.'
        }
    except RequestException as req_err:
        return {
            'error': f'RequestException - Gemini - Possibly a connection issue or DNS error.'
        }
    except (KeyError, IndexError) as parse_err:
        return {
            'error': f'ParseException - Gemini - Error parsing the API response\nThe structure of the API response may have changed or the response was unexpected.'
        }
        