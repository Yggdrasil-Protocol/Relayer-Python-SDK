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


consts = {
    "SCHEME": "wss",
    "NETLOC": "feeds.yggdrasilprotocol.io",
    "PATH": "",
    "URL": "/v1/ws",
}


def gen_url(
    feedIDs: List[str],
    scheme: str = "wss",
    netloc: str = "feeds.yggdrasilprotocol.io",
    path: str = "",
    url: str = "/v1/ws",
) -> str:
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


print(gen_url(["SPOT:BTC_USDT", "SPOT:ETH_USDT"]))
