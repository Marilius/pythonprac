from . import server


def run():
    """Run server."""
    try:
        s = server.Server()
        s.start()
    except KeyboardInterrupt:
        print('Server turned off')
