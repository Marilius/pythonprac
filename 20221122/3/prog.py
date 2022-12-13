import sys
import struct

wav = sys.stdin.buffer.read()
if len(wav) < 44 or struct.unpack('4s', wav[8:12])[0] != b'WAVE':
    print('NO')
else:
    titles = 'Size', 'Type', 'Channels', 'Rate', 'Bits', 'Data size'
    params = struct.unpack('i', wav[4:8]) + struct.unpack('hhi', wav[20:28]) + struct.unpack('h', wav[34:36]) + \
             struct.unpack('i', wav[40:44])

    ans = map(lambda x: f'{x[0]}={x[1]}', zip(titles, params))
    print(', '.join(ans))
