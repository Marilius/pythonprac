import unittest
import multiprocessing
import time
from moodserver.server import Server
from moodclient.client import Client


class TestServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = Server()
        cls.proc = multiprocessing.Process(target=cls.server.start)
        cls.proc.start()
        time.sleep(1)
        cls.player = Client('test')

    @classmethod
    def tearDownClass(cls):
        cls.proc.terminate()
        cls.player.do_exit('')

    def test_0(self):
        self.player.do_left('')
        response = self.player.socket.recv(self.player.buffer_size).decode()
        self.assertEqual(response.strip(), 'Moved to (9, 0)')

    def test_1(self):
        self.player.do_addmon('banana hello hello hp 25 coords 9 0')
        response = self.player.socket.recv(self.player.buffer_size).decode()
        self.assertEqual(response.strip(), 'Added banana to (9, 0) saying "hello"')

    def test_2(self):
        self.player.do_attack('banana with sword')
        response = self.player.socket.recv(self.player.buffer_size).decode()
        self.assertEqual(response.strip(), 'Attacked banana with sword. Damage 10 hp. banana now has 15 hp')
