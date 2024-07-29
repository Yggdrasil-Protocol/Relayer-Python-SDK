import json
from types import NoneType
from typing import List, Union

from pydantic import BaseModel


class DataFeed(BaseModel):
    event: str
    price: str
    feedID: str
    t: int

class SubscriptionFeed(BaseModel):
    feedID: str
    type: str

class SubscriptionMsg(BaseModel):
    event: str
    success: List[SubscriptionFeed] | NoneType
    error: List[SubscriptionFeed] | NoneType

'''
This function parses the event_raw string to a DataFeed or SubscriptionMsg object.
Can raise a JSONDecodeError if the event_raw string is not a valid JSON string.
Can raise a ValidationError if the event_raw JSON does not match the DataFeed or SubscriptionMsg schema.
Can raise a ValueError if the event type is unknown.
'''
def parse_event(event_raw: str) -> Union[DataFeed, SubscriptionMsg]:
    event_obj = json.loads(event_raw)    
    match event_obj:
        case {"event":"data"}:
            return DataFeed(**event_obj)
        case {"event":"subscribe-status"}:
            return SubscriptionMsg(**event_obj)
        case {"event":"subscribe-failed"}:
            return SubscriptionMsg(**event_obj)
        case _:
            raise ValueError(f"Unknown event type: {event_obj['event']}")