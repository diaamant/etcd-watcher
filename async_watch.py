import asyncio
import subprocess

import aetcd

from log import logger


# Custom exception to cancel tasks
class ErrorCancelTasks(Exception):
    pass


async def watch_callback(event):
    """Callback to handle etcd watch events."""
    if event.kind == aetcd.rtypes.EventKind.PUT and event.kv.key == b"work-service":
        if event.kv.value == b"start":
            logger.info("Starting process...")
            try:
                response = subprocess.getoutput(
                    "ip a"
                )  # You can replace this with your actual command
                logger.info(response)
            except subprocess.SubprocessError as e:
                logger.error(f"Failed to start process: {e}")
        elif event.kv.value == b"stop":
            logger.info("Stopping process...")
            # Add stop process logic here if necessary


async def watch_event():
    """Watches etcd for key 'work-service'."""
    client = aetcd.Client()

    logger.info('Watching for "work-service"...')

    try:
        watch = await client.watch(b"work-service")
        async for event in watch:
            await watch_callback(event)
    except Exception as e:
        logger.error(f"Watch event error: {e}")
    finally:
        await client.close()


async def work_task():
    """Dummy work task for demonstration."""
    iteration = 0
    while True:
        iteration += 1
        logger.info(f"Work iteration {iteration}")
        await asyncio.sleep(1.5)


async def main():
    tasks = [
        asyncio.create_task(watch_event()),
        asyncio.create_task(work_task()),
    ]

    try:
        await asyncio.gather(*tasks)
    except asyncio.TimeoutError:
        logger.warning("Timeout occurred!")
    except ErrorCancelTasks:
        logger.error("Fatal error; cancelling tasks")
        for task in tasks:
            task.cancel()
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
    finally:
        for task in tasks:
            if not task.done():
                task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        logger.info("Tasks cancelled")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Stopping watch...")
