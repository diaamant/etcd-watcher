import aetcd


async def main():
    client = aetcd.Client()
    await client.put(b"rec-service", b"start")
    print('Key "rec-service" set to "start"')
    await asyncio.sleep(3)
    await client.put(b"rec-service", b"stop")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
