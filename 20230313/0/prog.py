import asyncio


async def echo(reader, writer):
    host, port = writer.get_extra_info('peername')
    while not reader.at_eof():
        data = (await reader.readline()).strip()
        data = data.split(maxsplit=1)

        match data:
            case [b'print', a]:
                writer.write(a.swapcase())
            case [b'info', b'host']:
                writer.write(host.encode())
            case [b'info', b'post']:
                writer.write(f'{port}'.encode())
            case [b'quit']:
                break
        writer.write(b'\n')
        # await writer.drain()
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(echo, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())
