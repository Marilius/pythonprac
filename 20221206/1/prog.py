import asyncio

end = asyncio.Event()


async def writer(queue, delay):
    num = 0
    while not end.is_set():
        await asyncio.sleep(delay)
        await queue.put(f'{num}_{delay}')
        num += 1


async def stacker(queue, stack):
    while not end.is_set():
        curr = await queue.get()
        await stack.put(curr)


async def reader(stack, n, delay):
    num = 0
    while not end.is_set():
        await asyncio.sleep(delay)
        curr = await stack.get()
        print(curr)
        num += 1
        if num == n:
            end.set()


async def main():
    delay1, delay2, delay3, n = eval(input())

    queue = asyncio.Queue()
    stack = asyncio.LifoQueue()

    await asyncio.gather(
        writer(queue, delay1),
        writer(queue, delay2),
        stacker(queue, stack),
        reader(stack, n, delay3)
    )

asyncio.run(main())
