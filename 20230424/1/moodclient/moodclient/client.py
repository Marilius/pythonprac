import cmd
import cowsay
import readline
import shlex
import socket
import locale


BUFFER_SIZE = 1024
PORT = 1337
HOST = 'localhost'
CUSTOM_MONSTERS = {'jgsbat': None}

MONSTERS = cowsay.list_cows() + list(CUSTOM_MONSTERS.keys())
WEAPONS = {'sword': 10, 'spear': 15, 'axe': 20}


class Client(cmd.Cmd):
    """
    Instance of this class represents the client which runs the game.

    :param intro: gameplay intro.
    :type intro: str
    :param prompt: command line prompt.
    :type prompt: str
    """
    intro = '<<< Welcome to Python-MUD 0.1 >>>'
    prompt = '(Dungeon) '

    def __init__(self, login, *args, **kwargs):
        """Initiate client."""
        super().__init__(*args, **kwargs)
        self.login = login
        self.buffer_size = BUFFER_SIZE
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((HOST, PORT))

        self.send(f'login {self.login}')
        ans = self.socket.recv(self.buffer_size).decode().strip()
        if ans == 'This login is taken':
            print(ans)
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()
            return True
        else:
            print(f'\r{ans}\n{readline.get_line_buffer()}', end='', flush=True)

    def send(self, command):
        self.socket.send(f'{command}\n'.encode())

    def receive(self):
        while True:
            responses = self.socket.recv(self.buffer_size).decode()
            for response in responses.split('\n'):
                if response:
                    print(f'\r{response}\n{readline.get_line_buffer()}', end='', flush=True)

    @staticmethod
    def parse_addmon(args):
        """Parse addmov command."""
        try:
            name, *others = shlex.split(args)
        except Exception:
            raise ValueError

        if not set(['hello', 'hp', 'coords']).issubset(set(others)):
            raise ValueError

        hp_pos = others.index('hp')
        coords_pos = others.index('coords')
        greet_pos = others.index('hello')

        try:
            hp = int(others[hp_pos+1])
            x, y = map(int, others[coords_pos+1:coords_pos+3])
            greeting = others[greet_pos+1]
        except Exception:
            raise ValueError

        return (name, greeting, hp, x, y)

    def do_exit(self, args):
        """Exit the game."""
        return True

    def do_up(self, args):
        """Move one step up."""
        if args:
            print('Invalid arguments')
        else:
            self.send('move 0 -1')

    def do_right(self, args):
        """Move one step right."""
        if args:
            print('Invalid arguments')
        else:
            self.send('move 1 0')

    def do_left(self, args):
        """Move one step left."""
        if args:
            print('Invalid arguments')
        else:
            self.send('move -1 0')

    def do_down(self, args):
        """Move one step down."""
        if args:
            print('Invalid arguments')
        else:
            self.send('move 0 1')

    def do_addmon(self, args):
        """
        Add a monster:  addmon <name> coord <x> <y> hello <message> hp <health points>.
        """
        try:
            name, greeting, hp, x, y = Client.parse_addmon(args)
        except Exception:
            print('Invalid arguments')
            return

        if not (0 <= x <= 9 and 0 <= y <= 9):
            print('Invalid arguments')
            return

        if name not in MONSTERS:
            print('Cannot add unknown monster')
            return

        if hp <= 0:
            print('Invalid arguments')
            return

        self.send(f'addmon {name} "{greeting}" {hp} {x} {y}')

    def complete_attack(self, text, line, begidx, endidx):
        """Attack command completion."""
        command = shlex.split(line)

        if len(command) == 3:
            return [i for i in ['with'] if i.startswith(text)]

        if (len(command) == 1 and text) \
                or (len(command) == 2 and not text) \
                or (len(command) > 2 and command[2] != 'with') \
                or len(command) > 4 \
                or (len(command) == 4 and not text) \
                or (len(command) == 3 and text):
            return []

        if len(command) < 3:
            return [monster for monster in MONSTERS if monster.startswith(text)]
        else:
            return [weapon for weapon in WEAPONS if weapon.startswith(text)]

    def do_sayall(self, args):
        """Send message to all players."""
        match shlex.split(args):
            case [message]:
                self.send(f'sayall "{message}"')
            case _:
                print('Invalid arguments')

    def do_attack(self, args):
        """Attack the monster: attack <name> [with <weapon>]."""
        weapon = ['sword']

        args = shlex.split(args)

        if not args:
            print('Invalid arguments')
            return

        name, args = args[0], args[1:]

        if args:
            try:
                _, *weapon = args
            except Exception:
                print('Invalid arguments')
                return

            if _ != 'with' or (weapon and weapon[0] not in WEAPONS):
                print('Unknown weapon')
                return

        weapon = 'sword' if not weapon else weapon[0]
        damage = WEAPONS[weapon]

        self.send(f'attack {name} {weapon} {damage}')

    def do_locale(self, args):
        """Set locale: ru or en_ng"""
        if not args:
            print('Invalid arguments')
            return

        if args not in locale.locale_alias:
            print("Invalid locale name")
            return 0

        self.send(f'locale {args}')

    def default(line):
        """Non-existing command."""
        print("Invalid command")
