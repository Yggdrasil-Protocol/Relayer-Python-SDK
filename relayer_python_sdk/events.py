import json
from types import NoneType
from typing import List, Union

from pydantic import BaseModel

# Define the DataFeed and SubscriptionMsg models
class DataFeed(BaseModel):
    event: str
    p: str
    feedID: str
    t: int

class SubscriptionFeed(BaseModel):
    feedID: str
    type: str

class SubscriptionMsg(BaseModel):
    event: str
    success: List[SubscriptionFeed] | NoneType
    error: List[SubscriptionFeed] | NoneType

def parse_event(event_raw: str) -> Union[DataFeed, SubscriptionMsg]:
    '''
    This function parses the event_raw string to a DataFeed or SubscriptionMsg object.

    Args:
        event_raw: str: The raw event string.
    Returns:
        Union[DataFeed, SubscriptionMsg]: The parsed DataFeed or SubscriptionMsg object.
    Raises:
        JSONDecodeError: if the event's raw string is not a valid JSON string.
        ValidationError: if the event's JSON does not match their corresponding event schema.
        ValueError: if the event type is unknown.
    '''
    event_obj = json.loads(event_raw)
    
    match event_obj:
        case {"event":"price"}:
            return DataFeed(**event_obj)
        case {"event":"subscribe-status"}:
            return SubscriptionMsg(**event_obj)
        case {"event":"subscribe-failed"}:
            return SubscriptionMsg(**event_obj)
        case _:
            raise ValueError(f"Unknown event type: {event_obj['event']}")