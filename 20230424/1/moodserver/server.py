"""Server module of MUD game"""


import asyncio
import shlex
import cowsay
import random
from io import StringIO
import gettext


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


class MessageToTranslate:
    """
    Instances of this class represents output messages for users which have to be translated
    """

    def __init__(self, event: str, params: list = []):
        """
        Initializes the object's attributes

        :param event: event in the game. For example, 'attack'
        :type template: str
        :param params: params for event. For above example: ['user1', 'banana', 'sword']
        :type params: list
        """
        self.event = event
        self.params = params


class EmptyCell:
    """Instances of this class indicate empty cell in dungeon"""
    pass


class Monster:
    """
    Instances of this class indicate monster in dungeon cell
    """

    def __init__(self, name: str, hitpoints: str, greeting: str):
        """
        Initializes the object's attributes

        :param name: name of monster
        :type name: str
        :param hitpoints: hitpoints of monster
        :type hitpoints: int
        :param greeting: monster's greeting to players
        :type greeting: str
        """
        self.greeting = greeting
        self.name = name
        self.hitpoints = hitpoints


class Dungeon:
    """
    Instance of this class represents a dungeon in the game
    """

    def __init__(self, size: int = 10):
        """
        Initializes the object's attributes

        :param size: size of the dungeon
        :type size: int
        """
        self.size = size
        self.field = [[EmptyCell()] * size for i in range(size)]
        self.monsters = []


class Player:
    """
    Instance of this class represents the player in the dungeon
    """

    def __init__(self):
        """Initializes the object's attributes"""
        self.x = 0
        self.y = 0
        self.locale = ''


class Server:
    """
    Instance of this class represents the server which runs the game

    :param _clients: storage of clients' queues
    :type _clients: dict['str':asyncio.Queue]
    :param _players: storage of players in the game
    :type _players: dict['str':Player]
    :param _dungeon: game's dungeon
    :type _dungeon: Dungeon
    """
    _clients = {}
    _players = {}
    _dungeon = Dungeon()

    def __init__(self, host: str = HOST, port: int = PORT):
        """
        Initializes the object's attributes

        :param host: address where server should be run
        :type host: str
        :param port: host's port where server should be run
        :type port: int
        """
        self.host = host
        self.port = port

    def start(self) -> None:
        """Method to start the server"""
        async def routine():
            """Auxiliary asynchronous function to be run by asyncio"""
            server = await asyncio.gather(
                asyncio.start_server(self.chat, self.host, self.port),
                self.monster_migration()
                )
            async with server:
                await server.serve_forever()

        asyncio.run(routine())

    async def monster_migration(self) -> None:
        """
        Method to pick random monster and direction
        every 30 seconds and move monster in this direction
        """
        MOVEMENTS = {'up': (0, -1), 'down': (0, 1), 'right': (1, 0), 'left': (-1, 0)}

        while True:
            await asyncio.sleep(30)
            if self._dungeon.monsters:
                moved = False
                while not moved:
                    monster_x, monster_y = random.choice(self._dungeon.monsters)
                    movement = random.choice(list(MOVEMENTS.keys()))
                    dx, dy = MOVEMENTS[movement]
                    cell = self._dungeon.field[monster_x+dx][monster_y+dy]
                    if isinstance(cell, EmptyCell):
                        moved = True
                        # swap EmptyCell and Monster
                        t = self._dungeon.field[monster_x+dx][monster_y+dy], \
                            self._dungeon.field[monster_x][monster_y]
                        self._dungeon.field[monster_x][monster_y], self._dungeon.field[monster_x+dx][monster_y+dy] = t

                        # change dungeon.monsters information
                        self._dungeon.monsters.pop(self._dungeon.monsters.index((monster_x, monster_y)))
                        self._dungeon.monsters.append((monster_x+dx, monster_y+dy))

                        # notify users of monster's movement
                        # and some of those who has encountered this monster
                        monster = self._dungeon.field[monster_x+dx][monster_y+dy]

                        for ID in self._clients.keys():
                            encounter_message = self.encounter(ID)
                            translate_movement = self.translate(ID, MessageToTranslate(movement))
                            message_to_user = MessageToTranslate('monster_move', [monster.name, translate_movement])
                            await self._clients[ID].put(self.translate(ID, message_to_user) + encounter_message)

    async def chat(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
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
                done, pending = await asyncio.wait([send, receive],
                                                   return_when=asyncio.FIRST_COMPLETED)
                for task in done:
                    message_to_users = None
                    if task is send:
                        send = asyncio.create_task(reader.readline())
                        command = task.result().decode().strip()
                        match shlex.split(command):
                            case ['login', username]:
                                if username in self._clients.keys():
                                    response = 'This username is taken'
                                else:
                                    ID = username
                                    self._clients[ID] = personal_queue
                                    self._players[ID] = Player()
                                    response = MessageToTranslate('me_register', [ID])
                                    message_to_users = MessageToTranslate('other_register', [ID])
                            case ['locale', locale]:
                                self._players[ID].locale = locale
                                response = MessageToTranslate('locale', [locale])
                            case ['attack', *args]:
                                name, weapon, hitpoints = args
                                res = self.attack(ID, name, int(hitpoints))
                                match shlex.split(res):
                                    case ['Reject', name]:
                                        response = MessageToTranslate('Reject', [name])
                                    case ['Damage', name, damage, hitpoints]:
                                        response = self.translate(ID, MessageToTranslate(
                                                                  'attacked', [name, MessageToTranslate(weapon), damage, MessageToTranslate('hp', [damage])]))
                                        message_to_users = [MessageToTranslate(
                                                                  'other_attacked', [ID, name, MessageToTranslate(weapon), damage, MessageToTranslate('hp', [damage])])]
                                        if int(hitpoints) == 0:
                                            dead = MessageToTranslate('dead', [name])
                                            response += self.translate(ID, dead)
                                            message_to_users.append(dead)
                                        else:
                                            remainder = MessageToTranslate('remained_hp', [name, hitpoints, MessageToTranslate('hp', [hitpoints])])
                                            response += self.translate(ID, remainder)
                                            message_to_users.append(remainder)
                                    case _:
                                        pass
                            case ['move', *args]:
                                dx, dy = map(int, args)
                                response = self.move(ID, dx, dy)
                            case ['addmon', *args]:
                                name, greeting, hitpoints, x, y = args
                                response = self.addmon(ID, name, int(x), int(y), int(hitpoints), greeting)
                                message_to_users = MessageToTranslate(
                                                   'other_addmon', [ID, name, hitpoints, MessageToTranslate('hp', [hitpoints]), x, y])
                            case ['sayall', message]:
                                response = ''
                                message_to_users = f'{ID}: {message}'
                            case ['exit']:
                                connected = False
                                response = 'You are successfully left'
                                message_to_users = MessageToTranslate('other_left', [ID])
                            case _:
                                response = MessageToTranslate('error')

                        if isinstance(response, MessageToTranslate):
                            await personal_queue.put(self.translate(ID, response))
                        else:
                            await personal_queue.put(response)

                        if message_to_users:
                            for other_ID, q in self._clients.items():
                                if q is not personal_queue:
                                    lst = message_to_users if isinstance(message_to_users, list) else [message_to_users]
                                    for message in lst:
                                        if isinstance(message, MessageToTranslate):
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
            message_to_users = MessageToTranslate('other_left', [ID])
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

    def translate(self, ID: str, message: MessageToTranslate) -> str:
        """
        Method to translate whole message for the player

        :param ID: identificator of a player
        :type ID: str
        :param message: message for the player
        :type message: str
        :return: translated message for the player
        :rtype: str
        """
        translation = gettext.translation('server', 'translation', languages=[self._players[ID].locale], fallback=True)
        _, ngettext = translation.gettext, translation.ngettext

        params = []
        for param in message.params:
            if isinstance(param, MessageToTranslate):
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
        cell = self._dungeon.field[self._players[ID].x][self._players[ID].y]
        if isinstance(cell, Monster):
            cow, cowfile = cell.name, None

            if cow in CUSTOM_MONSTERS:
                cow, cowfile = 'default', CUSTOM_MONSTERS[cell.name]

            message = cowsay.cowsay(cell.greeting, cow=cow, cowfile=cowfile)

            return f'\n{message}'
        return ''

    def move(self, ID: str, dx: int, dy: int) -> str:
        """
        Method to move a player in the dungeon

        :param ID: identificator of a player
        :type ID: str
        :param dx: offset along axis X
        :type dx: int
        :param dy: offset along axis Y
        :type dy: int
        :return: notification of movement and monster's greeting if meeting happend
        :rtype: str
        """
        self._players[ID].x = (self._players[ID].x + dx) % self._dungeon.size
        self._players[ID].y = (self._players[ID].y + dy) % self._dungeon.size

        message = MessageToTranslate('move', [str(self._players[ID].x), str(self._players[ID].y)])
        response = self.translate(ID, message) + self.encounter(ID)
        return response

    def addmon(self, ID: str, name: str, x: int, y: int, hitpoints: int, greeting: str) -> str:
        """
        Method to add a monster

        :param ID: identificator of a player
        :type ID: str
        :param name: name of a monster
        :type name: str
        :param x: monster's position on axis X
        :type x: int
        :param y: monster's position on axis Y
        :type y: int
        :param hitpoints: hitpoints of the monster
        :type hitpoints: int
        :param greeting: monster's greeting to players
        :type greeting: str
        :return: monster's deployment notification
        :rtype: str
        """
        replaced = isinstance(self._dungeon.field[x][y], Monster)
        self._dungeon.field[x][y] = Monster(name, hitpoints, greeting)
        self._dungeon.monsters.append((x, y))
        message = MessageToTranslate('me_addmon', [name, str(x), str(y), greeting])
        replace_message = MessageToTranslate('replace')
        response = self.translate(ID, message) + (self.translate(ID, replace_message) if replaced else '')
        return response

    def attack(self, ID: str, name: str, hitpoints: int) -> str:
        """
        Method to attack a monster by player

        :param ID: identificator of a player
        :type ID: str
        :param name: name of a monster to be attacked
        :type name: str
        :param hitpoints: damage to be made to the monster
        :type hitpoints: int
        :return: log of attacking
        :rtype: str
        """
        cell = self._dungeon.field[self._players[ID].x][self._players[ID].y]

        if not isinstance(cell, Monster) or cell.name != name:
            return f'Reject {name}'
        else:
            damage = min(cell.hitpoints, hitpoints)
            cell.hitpoints -= damage
            if cell.hitpoints == 0:
                self._dungeon.field[self._players[ID].x][self._players[ID].y] = EmptyCell()
            return f'Damage {name} {damage} {cell.hitpoints}'
