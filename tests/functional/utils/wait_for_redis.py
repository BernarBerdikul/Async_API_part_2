import asyncio

import aioredis


async def redis_connect():
    return await aioredis.create_redis_pool(("127.0.0.1", 6379), minsize=10, maxsize=20)


async def wait_for_redis(redis_client):
    while True:
        try:
            response = redis_client.client_list()
            print(response)
            redis_client.ping()
            print("Successfully connected to redis")
            return
        except aioredis.ConnectionClosedError:
            print("Redis connection error!")
            await asyncio.sleep(5)
            continue


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    redis_client = await redis_connect()
    try:
        loop.run_until_complete(wait_for_redis(redis_client))
    finally:
        redis_client.close()
    loop.close()
