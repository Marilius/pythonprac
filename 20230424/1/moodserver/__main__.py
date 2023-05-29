from . import server


if __name__ == '__main__':
    try:
        s = server.Server()
        s.start()
    except KeyboardInterrupt:
        print('Server turned off')
