import aetcd


async def main():
    client = aetcd.Client()
    await client.put(b"work-service", b"start")
    print('Key "work-service" set to "start"')
    await asyncio.sleep(3)
    await client.put(b"work-service", b"stop")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
