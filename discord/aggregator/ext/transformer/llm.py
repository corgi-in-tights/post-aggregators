import json
import logging
from datetime import datetime

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

    def parse_event_details(self, input_text, additional_data=None, timezone=None):
        prompt = f"""Extract event details from the following text and output strictly in the specified JSON format:

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

        There may be multiple events. Strictly adhere to this format and provide output only in JSON array format.
        If you are unable to recognize a minimum of one event, please return \"Failed to extract\"."""

        if additional_data:
            prompt += f"""\n\nThe events come from an organization that: {additional_data["description"]}
            Today's date is {datetime.now(timezone).strftime("%d %b")}.

            Here is a list of events this organization has held in the past. Ensure any new events are not a duplicate:
            - {"\n-".join(additional_data["past_events"])}
            If it is a duplicate, please return \"Duplicate\".
            """"""


        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

        payload = self._create_payload(prompt)

        try:
            response = requests.post(self.url, headers=headers, json=payload, timeout=20)
            response.raise_for_status()  # Check if the request was successful
            completion = response.json()["choices"][0]["message"]["content"].strip()

            s = completion.replace(" ", "").replace("\n", "")

            # Attempt to parse the returned string into a JSON object
            data = json.loads(completion.strip())
            for key in ["title", "description", "location", "date", "time"]:
                if key not in data:
                    logger.error("Failed to extract %s from the response %s.", key, data)
                    return None
            return data  # noqa: TRY300

        except requests.exceptions.RequestException as e:
            logger.exception("Error fetching data from OpenAI API", exc_info=e)
            return None

        except json.JSONDecodeError as e:
            logger.exception("Error parsing JSON response", exc_info=e)
            return None
