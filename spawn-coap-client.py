import logging
import asyncio

from aiocoap import *

COAPURI="coap://edgex/a1r/d1/int"

logging.basicConfig(level=logging.DEBUG)

async def main():
    
    context = await Context.create_client_context()

    await asyncio.sleep(2)

    payload = 5
    request = Message(code=PUT, payload=payload, uri=COAPURI)

    response = await context.request(request).response

    print('Result: %s\n%r'%(response.code, response.payload))

if __name__ == "__main__":
    asyncio.run(main())
