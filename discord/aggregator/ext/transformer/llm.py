import json
import logging

import requests

logger = logging.getLogger("aggregator.transformer")

class LLMWrapper:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://api.openai.com/v1/chat/completions"

    def _create_payload(self, prompt):
        return {
            "model": "gpt-4-turbo",
            "messages": [{"role": "system", "content": prompt}],
            "max_tokens": 500,
            "temperature": 0.0,
        }

    def parse_event_details(self, input_text):
        prompt = f"""Extract event details from the following text and output strictly in the specified JSON array format:

        Text: '{input_text}'

        Output format:
        [
            {{
                "title": "<str, Club name: Title of the event maximum of 20 words>",
                "description": "<str, description of the event maximum of 200 words>",
                "location": "<str, room of the event in the format buildingroom_number e.g. MN2010>",
                "date": "<str, date of the event in the format 'day month(3 letter abbreviation)' if no date given try to find any indicators like tomorrow>",
                "time": "<str, time of the event in the format 'hh:mm - hh:mm'>"
            }},
            // if there is more than one event
            {{
                "title": "<str, Club name: Title of the event maximum of 20 words>",
                "description": "<str, description of the event maximum of 200 words>",
                "location": "<str, room of the event in the format buildingroom_number e.g. MN2010>",
                "date": "<str, date of the event in the format 'day month(3 letter abbreviation)' if no date given try to find any indicators like tomorrow>",
                "time": "<str, time of the event in the format 'hh:mm - hh:mm'>"
            }},
            // and so on....
        ]

        There will always be at least one event, but there may be multiple events. Strictly adhere to this format and provide output only in JSON array format."""



        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

        payload = self._create_payload(prompt)

        try:
            response = requests.post(self.url, headers=headers, json=payload, timeout=20)
            response.raise_for_status()  # Check if the request was successful
            completion = response.json()["choices"][0]["message"]["content"].strip()

            # Attempt to parse the returned string into a JSON object
            return json.loads(completion)

        except requests.exceptions.RequestException as e:
            logger.exception("Error fetching data from OpenAI API", exc_info=e)
            raise

        except json.JSONDecodeError as e:
            logger.exception("Error parsing JSON response", exc_info=e)
            raise
