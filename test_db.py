import asyncio
from crud import search_tenders

async def test():
    results = await search_tenders("Road")
    print("Found:", len(results), "tenders")
    for t in results:
        print(t.title)

asyncio.run(test())