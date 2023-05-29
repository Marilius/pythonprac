import cowsay
import shlex
import cmd
import readline
import socket


BUFFER_SIZE = 1024
PORT = 1337
HOST = 'localhost'
CUSTOM_MONSTERS = {'jgsbat': None}


class Client(cmd.Cmd):

    intro = '<<< Welcome to Python-MUD 0.1 >>>'
    prompt = '(Dungeon) '

    def __init__(self, username, *args, **params):
        super().__init__(*args, **params)
        self.username = username
        self.buffer_size = BUFFER_SIZE
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((HOST, PORT))

        # register
        self.send(f'login {self.username}')
        data = self.socket.recv(self.buffer_size).decode().strip()
        if data == 'This username is taken':
            print(data)
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()
            return True
        else:
            print(f'\r{data}\n{readline.get_line_buffer()}', end='', flush=True)

    @staticmethod
    def parse_addmon(args):
        try:
            name, *others = shlex.split(args)
        except Exception:
            raise ValueError

        if not set(['hello', 'hp', 'coords']).issubset(set(others)):
            raise ValueError

        hp_index = others.index('hp')
        coords_index = others.index('coords')
        greet_index = others.index('hello')

        try:
            hitpoints = int(others[hp_index+1])
            x, y = map(int, others[coords_index+1:coords_index+3])
            greeting = others[greet_index+1]
        except Exception:
            raise ValueError

        return (name, greeting, hitpoints, x, y)

    def send(self, command):
        self.socket.send(f'{command}\n'.encode())

    def do_exit(self, args):
        return True

    def do_up(self, args):
        if args:
            print('Invalid arguments')
        else:
            self.send('move 0 -1')

    def do_right(self, args):
        if args:
            print('Invalid arguments')
        else:
            self.send('move 1 0')

    def do_left(self, args):
        if args:
            print('Invalid arguments')
        else:
            self.send('move -1 0')

    def do_down(self, args):
        if args:
            print('Invalid arguments')
        else:
            self.send('move 0 1')

    def do_addmon(self, args):
        try:
            name, greeting, hitpoints, x, y = Client.parse_addmon(args)
        except Exception:
            print('Invalid arguments')
            return

        if x < 0 or x > 9 or y < 0 or y > 9 or hitpoints <= 0:
            print('Invalid arguments')
            return

        if name not in cowsay.list_cows() and name not in CUSTOM_MONSTERS:
            print('Cannot add unknown monster')
            return

        self.send(f'addmon {name} "{greeting}" {hitpoints} {x} {y}')

    def do_sayall(self, args):
        match shlex.split(args):
            case [message]:
                self.send(f'sayall "{message}"')
            case _:
                print('Invalid arguments')

    def do_attack(self, args):
        WEAPONS = {'sword': 10, 'spear': 15, 'axe': 20}
        weapon = ['sword']

        args = shlex.split(args)

        if not args:
            print('Invalid arguments')
            return

        name = args[0]  # name of monster
        args = args[1:]  # extract name from args

        if args:
            try:
                parameter, *weapon = args
            except Exception:
                print('Invalid arguments')
                return

            if not parameter == 'with' or (weapon and weapon[0] not in WEAPONS):
                print('Unknown weapon')
                return

        weapon = 'sword' if not weapon else weapon[0]
        damage = WEAPONS[weapon]

        self.send(f'attack {name} {weapon} {damage}')

    def do_locale(self, args):
        if not args:
            print('Invalid arguments')
            return

        self.send(f'locale {args}')

    def complete_attack(self, text, line, begidx, endidx):
        WEAPONS = {'sword', 'spear', 'axe'}
        AVAILABLE_MONSTERS = set(cowsay.list_cows()) | CUSTOM_MONSTERS.keys()

        command = shlex.split(line)

        if (len(command) == 1 and text) \
                or (len(command) == 2 and not text) \
                or (len(command) > 2 and command[2] != 'with') \
                or len(command) > 4 \
                or (len(command) == 4 and not text) \
                or (len(command) == 3 and text):
            # First case: attack not in line yet
            # Second case: attack somebody already in line
            # Third case: attack somebody bla-bla (not with)
            # Fourth case: attack somebody with weapon bla...
            # Fifth case: attack somebody with weapon already in line
            # Sixth case: attack somebody with and with not in line yet
            return []

        if len(command) < 3:
            # Case: attack some...
            return [monster for monster in AVAILABLE_MONSTERS if monster.startswith(text)]
        else:
            # Case: attack somebody with ...
            return [weapon for weapon in WEAPONS if weapon.startswith(text)]

    def receive(self):
        while True:
            responses = self.socket.recv(self.buffer_size).decode()
            for response in responses.split('\n'):
                if response:
                    print(f'\r{response}\n{readline.get_line_buffer()}', end='', flush=True)
