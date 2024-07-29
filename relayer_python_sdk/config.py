from typing import List, NamedTuple
from urllib.parse import urlencode, urlunparse

# NamedTuple to match the internal signature of urlunparse
class Components(NamedTuple):
    scheme: str
    netloc: str
    url: str
    path: str
    query: str
    fragment: str


# constants for the ws conn url
SCHEME = "wss"
NETLOC = "feeds.yggdrasilprotocol.io"
PATH = ""
URL = "/v1/ws"

# constants in seconds
PING_INTERVAL = 30
PING_TIMEOUT = 60

def gen_url(
    feedIDs: List[str],
    scheme: str = SCHEME,
    netloc: str = NETLOC,
    path: str = PATH,
    url: str = URL,
) -> str:
    '''
    This function generates the websocket connection URL. 

    Args:
        feedIDs: ``List[str]``: The list of feedIDs to subscribe to.
        scheme: ``str``: The scheme of the URL.
        netloc: ``str``: The netloc of the URL.
        path: ``str``: The path of the URL.
        url: ``str``: The URL.
    
    Returns:
        ``str``: The generated URL.
    '''
    return str(
        urlunparse(
            Components(
                scheme=scheme,
                netloc=netloc,
                query=urlencode({"feedIDs": ",".join(feedIDs)}),
                path=path,
                url=url,
                fragment="",
            )
        )
    )


# print(gen_url(["SPOT:BTC_USDT", "SPOT:ETH_USDT"]))
