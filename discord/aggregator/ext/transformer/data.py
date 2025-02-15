import json
from pathlib import Path


def get_guild_prompting(guild_channel_id: int):
    # add check for if past events are expired
    with Path("./guild_prompting.json").open() as f:
        return json.load(f)[str(guild_channel_id)]

def add_guild_past_event(guild_channel_id: int, event_title: str, event_date: str):
    with Path("./guild_prompting.json", "r").open() as f:
        data = json.load(f)[str(guild_channel_id)]
        data[str(guild_channel_id)]["past_events"].append(f"{event_title}|{event_date}")

    with Path("./guild_prompting.json", "w").open() as f:
        json.dump(data, f, indent=4)

