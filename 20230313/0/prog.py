import asyncio


async def echo(reader, writer):
    while not reader.at_eof():
        data = await reader.readline()
        data = data.split(maxsplit=1)

        match data:
            case ['print', a]:
                writer.write(a)
                await writer.drain()
            case ['info', b]:
                writer.write(str(writer.get_extra_info('peername')[0 if b == b'host\n' else 1]).encode())
                await writer.drain()
        # writer.write(data.swapcase())
        # await writer.drain()
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(echo, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())
