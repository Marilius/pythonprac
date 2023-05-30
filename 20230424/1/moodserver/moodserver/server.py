"""Server module of MUD game"""


import asyncio
import cowsay
import gettext
from io import StringIO
import os
import random
import shlex


JGSBAT = cowsay.read_dot_cow(StringIO(r"""
$the_cow = <<EOC;
         $thoughts
          $thoughts
    ,_                    _,
    ) '-._  ,_    _,  _.-' (
    )  _.-'.|\\\\--//|.'-._  (
     )'   .'\/o\/o\/'.   `(
      ) .' . \====/ . '. (
       )  / <<    >> \  (
        '-._/``  ``\_.-'
  jgs     __\\\\'--'//__
         (((""`  `"")))
EOC
"""))


PORT = 1337
HOST = '0.0.0.0'
CUSTOM_MONSTERS = {'jgsbat': JGSBAT}
MOVEMENTS = {'up': (0, -1), 'down': (0, 1), 'right': (1, 0), 'left': (-1, 0)}


class Monster:
    """
    Monster entity.
    """

    def __init__(self, name: str, hp: int, greeting: str):
        """
        Initiate monster.

        :param name: name of monster
        :type name: str
        :param hp: hitpoints of monster
        :type hp: int
        :param greeting: monster's greeting to players
        :type greeting: str
        """
        self.greeting = greeting
        self.name = name
        self.hp = hp


class Message:
    """
    Instances of this class represents output messages for users which have to be translated
    """

    def __init__(self, event: str, params: list = []):
        """
        Initializes the object's attributes

        :param event: event in the game.
        :type template: str
        :param params: params for event.
        :type params: list
        """
        self.event = event
        self.params = params


class Server:
    """
    Game server

    :param _clients: storage of clients' queues
    :type _clients: dict['str':asyncio.Queue]
    :param _players: storage of players in the game
    :type _players: dict['str':Player]
    """
    _clients = {}
    _players = {}

    def __init__(self, host: str = HOST, port: int = PORT, n: int = 10):
        """
        Initializes the object's attributes

        :param n: size of the dungeon
        :type n: int
        :param host: address where server should be run
        :type host: str
        :param port: host's port where server should be run
        :type port: int
        """
        self.host = host
        self.port = port

        self.n = n
        self.field = [[None for j in range(n)] for i in range(n)]
        self.monsters = []

    def start(self) -> None:
        """Method to start the server"""
        async def routine():
            """Auxiliary asynchronous function to be run by asyncio"""
            server = await asyncio.gather(
                asyncio.start_server(self.game, self.host, self.port),
                self.monster_motion()
            )
            async with server:
                await server.serve_forever()

        asyncio.run(routine())

    async def monster_motion(self) -> None:
        """
        Monster's movement realisation.
        """
        while True:
            await asyncio.sleep(30)
            if self.monsters:
                moved = False
                while not moved:
                    monster_x, monster_y = random.choice(self.monsters)

                    if self.field[monster_x][monster_y] is None:
                        if (monster_x, monster_y) in self.monsters:
                            self.monsters.pop(self.monsters.index((monster_x, monster_y)))

                        moved = True
                        break

                    movement = random.choice(list(MOVEMENTS.keys()))
                    dx, dy = MOVEMENTS[movement]
                    cell = self.field[monster_x+dx][monster_y+dy]
                    if cell is None:
                        moved = True

                        tmp = self.field[monster_x+dx][monster_y+dy], \
                            self.field[monster_x][monster_y]
                        self.field[monster_x][monster_y], self.field[monster_x+dx][monster_y+dy] = tmp

                        self.monsters.pop(self.monsters.index((monster_x, monster_y)))
                        self.monsters.append((monster_x+dx, monster_y+dy))

                        monster = self.field[monster_x+dx][monster_y+dy]

                        for ID in self._clients.keys():
                            encounter_message = self.encounter(ID)
                            translate_movement = self.translate(ID, Message(movement))
                            message_to_user = Message('monster_move', [monster.name, translate_movement])
                            await self._clients[ID].put(self.translate(ID, message_to_user) + encounter_message)

    async def game(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        """
        Method to process a player's client side

        :param reader: represents a reader object that provides APIs to read data from the IO stream
        :type reader: asyncio.StreamReader
        :param writer: represents a writer object that provides APIs to write data to the IO stream
        :type writer: asyncio.StreamWriter
        """
        ID = '{}:{}'.format(*writer.get_extra_info('peername'))
        personal_queue = asyncio.Queue()
        send = asyncio.create_task(reader.readline())
        receive = asyncio.create_task(personal_queue.get())
        connected = True
        try:
            while connected and not reader.at_eof():
                done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
                for task in done:
                    message_to_users = None
                    if task is send:
                        send = asyncio.create_task(reader.readline())
                        data = task.result().decode().strip()
                        match shlex.split(data):
                            case ['login', login]:
                                if login in self._clients.keys():
                                    response = 'This login is taken'
                                else:
                                    ID = login
                                    self._clients[ID] = personal_queue
                                    self._players[ID] = {'x': 0, 'y': 0, 'locale': ''}
                                    response = Message('me_register', [ID])
                                    message_to_users = Message('other_register', [ID])
                            case ['locale', locale]:
                                self._players[ID]['locale'] = locale
                                response = Message('locale', [locale])
                            case ['attack', *args]:
                                name, weapon, hp = args

                                hp = int(hp)

                                cell = self.field[self._players[ID]['x']][self._players[ID]['y']]

                                if not isinstance(cell, Monster) or cell.name != name:
                                    res = f'Reject {name}'
                                else:
                                    damage = min(cell.hp, hp)
                                    cell.hp -= damage
                                    if cell.hp <= 0:
                                        self.field[self._players[ID]['x']][self._players[ID]['y']] = None

                                        try:
                                            self.monsters.pop(self.monsters.index((self._players[ID]['x'], self._players[ID]['y'])))
                                        except Exception:
                                            pass

                                    res = f'Damage {name} {damage} {cell.hp}'

                                match shlex.split(res):
                                    case ['Reject', name]:
                                        response = Message('Reject', [name])
                                    case ['Damage', name, damage, hp]:
                                        response = self.translate(ID, Message(
                                                                  'attacked', [name, Message(weapon), damage, Message('hp', [damage])]))
                                        message_to_users = [Message(
                                                                  'other_attacked', [ID, name, Message(weapon), damage, Message('hp', [damage])])]
                                        if int(hp) <= 0:
                                            dead = Message('dead', [name])
                                            response += self.translate(ID, dead)
                                            message_to_users.append(dead)
                                        else:
                                            remainder = Message('remained_hp', [name, hp, Message('hp', [hp])])
                                            response += self.translate(ID, remainder)
                                            message_to_users.append(remainder)
                                    case _:
                                        pass
                            case ['move', *args]:
                                dx, dy = map(int, args)

                                self._players[ID]['x'] = (self._players[ID]['x'] + dx) % self.n
                                self._players[ID]['y'] = (self._players[ID]['y'] + dy) % self.n

                                message = Message('move', [str(self._players[ID]['x']), str(self._players[ID]['y'])])
                                response = self.translate(ID, message) + self.encounter(ID)
                            case ['addmon', *args]:
                                name, greeting, hp, x, y = args

                                hp, x, y = int(hp), int(x), int(y)

                                replaced = isinstance(self.field[x][y], Monster)
                                self.field[x][y] = Monster(name, hp, greeting)
                                self.monsters.append((x, y))
                                message = Message('me_addmon', [name, str(x), str(y), greeting])
                                replace_message = Message('replace')
                                response = self.translate(ID, message) + (self.translate(ID, replace_message) if replaced else '')

                                message_to_users = Message('other_addmon', [ID, name, hp, Message('hp', [hp]), x, y])
                            case ['sayall', message]:
                                response = ''
                                message_to_users = f'{ID}: {message}'
                            case ['exit']:
                                connected = False
                                response = 'You are successfully left'
                                message_to_users = Message('other_left', [ID])
                            case _:
                                response = Message('error')

                        if isinstance(response, Message):
                            await personal_queue.put(self.translate(ID, response))
                        else:
                            await personal_queue.put(response)

                        if message_to_users:
                            for other_ID, q in self._clients.items():
                                if q is not personal_queue:
                                    lst = message_to_users if isinstance(message_to_users, list) else [message_to_users]
                                    for message in lst:
                                        if isinstance(message, Message):
                                            await q.put(self.translate(other_ID, message))
                                        else:
                                            await q.put(message)
                    elif task is receive:
                        receive = asyncio.create_task(personal_queue.get())
                        writer.write(f'{task.result()}\n'.encode())
                        await writer.drain()

            send.cancel()
            receive.cancel()
            writer.close()
            await writer.wait_closed()
        except Exception as e:
            print(e)

        if ID in self._clients.keys():
            del self._clients[ID]
            message_to_users = Message('other_left', [ID])
            for other_ID, q in self._clients.items():
                await q.put(self.translate(other_ID, message_to_users))

    @staticmethod
    def translate_event(event: str, params: list[str], _, ngettext) -> str:
        """
        Method to transform event to its translated description

        :param event: event
        :type event: str
        :param params: parameters for the event
        :type params: list[str]
        :param _: gettext
        :type _: function
        :param ngettext: ngettext
        :type ngettext: function
        :return: translated description of the event
        :rtype: str
        """
        EVENTS = {
            'locale': _('Set up locale: {}'),
            'me_register': _('You are successfully registered as {}'),
            'other_register': _('{} joined the game'),
            'other_left': _('{} left the game'),
            'move': _('Moved to ({}, {})'),
            'me_addmon': _('Added {} to ({}, {}) saying "{}"'),
            'replace': _('. Replaced the old monster'),
            'other_addmon': _('{} added {} with {} {} to ({}, {})'),
            'monster_move': _('{} moved one cell {}'),
            'right': _('right'),
            'left': _('left'),
            'up': _('up'),
            'down': _('down'),
            'error': _('Something bad has happened. Please reconnect to the server'),
            'Reject': _('No {} here'),
            'dead': _(' {} is dead'),
            'remained_hp': _(' {} now has {} {}'),
            'axe': _('axe'),
            'spear': _('spear'),
            'sword': _('sword'),
            'attacked': _('Attacked {} with {}. Damage {} {}.'),
            'other_attacked': _('{} attacked {} with {}. Damage {} {}.'),
            'hp': ngettext('hp', 'hp', int(params[0]) if event == 'hp' else 1)
        }

        return EVENTS[event].format(*params)

    def translate(self, ID: str, message: Message) -> str:
        """
        Method to translate whole message for the player

        :param ID: identificator of a player
        :type ID: str
        :param message: message for the player
        :type message: str
        :return: translated message for the player
        :rtype: str
        """
        translation_path = os.path.join(os.path.dirname(__file__), 'translation')
        translation = gettext.translation('moodserver', translation_path, languages=[self._players[ID]['locale']], fallback=True)
        _, ngettext = translation.gettext, translation.ngettext

        params = []
        for param in message.params:
            if isinstance(param, Message):
                params.append(Server.translate_event(param.event, param.params, _, ngettext))
            else:
                params.append(param)

        return Server.translate_event(message.event, params, _, ngettext)

    def encounter(self, ID: str) -> str:
        """
        Method to check if a player has encountered a monster

        :param ID: identificator of a player
        :type ID: str
        :return: monster's greeting if player's met a monster
        :rtype: str
        """
        cell = self.field[self._players[ID]['x']][self._players[ID]['y']]
        if isinstance(cell, Monster):
            cow, cowfile = cell.name, None

            if cow in CUSTOM_MONSTERS:
                cow, cowfile = 'default', CUSTOM_MONSTERS[cell.name]

            message = cowsay.cowsay(cell.greeting, cow=cow, cowfile=cowfile)

            return f'\n{message}'
        return ''
