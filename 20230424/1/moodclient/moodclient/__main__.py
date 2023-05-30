from . import client
import sys
import threading


def run():
    """Run client."""
    try:
        cl = client.Client(login=sys.argv[1])
        receiver = threading.Thread(target=cl.receive, args=(), daemon=True)
        receiver.start()
        cl.cmdloop()
    except Exception:
        print('Your session was interrupted')
