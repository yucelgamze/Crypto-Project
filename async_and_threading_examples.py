import threading
import requests
import time
import asyncio
import aiohttp
import certifi
import ssl


def get_data_sync(urls):
    start_time = time.time()
    json_array = []
    for url in urls:
        json_array.append(requests.get(url).json)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Execution time: ", elapsed_time, " seconds")
    return json_array


class ThreadingDownloader(threading.Thread):

    json_array = []

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        response = requests.get(self.url)
        self.json_array.append(response.json())
        return self.json_array


def get_data_threading(urls):
    start_time = time.time()
    threads = []
    for url in urls:
        t = ThreadingDownloader(url)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
        print(t)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Execution time: ", elapsed_time, " seconds")


async def get_data_async_but_as_a_wrapper(urls):
    start_time = time.time()
    json_array = []

    ssl_context = ssl.create_default_context(cafile=certifi.where())
    conn = aiohttp.TCPConnector(ssl=ssl_context)
    async with aiohttp.ClientSession(connector=conn) as session:
        for url in urls:
            async with session.get(url) as response:
                json_array.append(await response.json())

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Execution time: ", elapsed_time, " seconds")
    return json_array

async def get_data(session, url, json_array):
    async with session.get(url) as response:
        json_array.append(await response.json())


async def get_data_async_concurrently(urls):
    start_time = time.time()
    json_array = []

    ssl_context = ssl.create_default_context(cafile=certifi.where())
    conn = aiohttp.TCPConnector(ssl=ssl_context)
    async with aiohttp.ClientSession(connector=conn) as session:
        tasks = []
        for url in urls:
            tasks.append(asyncio.ensure_future(get_data(session, url, json_array)))
        await asyncio.gather(*tasks)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Execution time: ", elapsed_time, " seconds")



urls = ["https://postman-echo.com/delay/3"] * 10  # 10 defa bu isteği atacak ve her istek 3 saniye sürecek

# get_data_sync(urls)    # 46.87 saniye sürdü
# get_data_threading(urls) # 3.96 saniye sürdü
#asyncio.run(get_data_async_but_as_a_wrapper(urls)) # 32 saniye
#asyncio.run(get_data_async_concurrently(urls)) # 4  saniye