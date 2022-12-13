import datetime


class DIR:
    left = 'left'
    right = 'right'


Name = 'MUD'
VERSION = 0.01
DEVELOPERS = 'ME!'
while True:
    curr = input('> ')
    match curr.split():
        case ['about']:
            print(f'{Name} version {VERSION}')
        case ['credits']:
            print(f'Copyright (c) {DEVELOPERS}')
        case ['credits', '--year']:
            print(f'Copyright (c) {DEVELOPERS} {datetime.date.today()}')
        case ['move']:
            print('Unknown movement direction')
        case ['move', direction]:
            match direction:
                case 'left':
                    print('<-moved')
                case 'right':
                    print('moved->')
                case _:
                    print('Unknown movement direction')

        case ['travel', *directions]:
            if directions:
                for i in directions:
                    match i:
                        case DIR.left:
                            print('<-moved')
                        case DIR.right:
                            print('moved->')
                        case _:
                            print('Unknown movement direction')
            else:
                print('Nowhere to travel')

        case ['quit']:
            break
        case _:
            print('Cannot parse')
