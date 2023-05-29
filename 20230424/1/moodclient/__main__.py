from . import client
import sys
import threading


if __name__ == '__main__':
    try:
        cl = client.Client(username=sys.argv[1])
        receiver = threading.Thread(target=cl.receive, args=(), daemon=True)
        receiver.start()
        cl.cmdloop()
    except Exception:
        print('Your session was interrupted')
