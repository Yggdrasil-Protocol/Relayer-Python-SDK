# Relayer-Python-SDK [![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

> <p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/Yggdrasil-Protocol/Relayer-Go-SDK">Relayer-Go-SDK</a> by <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://github.com/Yggdrasil-Protocol">Yggdrasil-Protocol</a> is licensed under <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">CC BY-NC-SA 4.0<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/nc.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/sa.svg?ref=chooser-v1" alt=""></a></p>

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg

# Example

Here is an example of how to use the Relayer-Python-SDK:

```python
import asyncio
from relayer_python_sdk.ws import RelayerWS
from relayer_python_sdk import events

feedIDs = ["SPOT:BTC_USDT", "SPOT:ETH_USDT"]
ws = RelayerWS(feedIDs)


@ws.on_data_event
async def on_data_event(event: events.DataFeed):
    print("Data Feed Event:", event)


@ws.on_info_event
async def on_info_event(event: events.SubscriptionMsg):
    print("Info event:", event)


async def main():
    sub_task = asyncio.create_task(ws.connect())

    await asyncio.sleep(10)
    await ws.close()

    await sub_task


if __name__ == "__main__":
    asyncio.run(main())
```

This code will subscribe to the data feeds `SPOT:BTC_USDT` and `SPOT:ETH_USDT` and print the price events and info events.
