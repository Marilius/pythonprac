import sys
import zlib
import glob

for i in glob.iglob(r'.git\objects\??\*'):
    with open(i, 'rb') as f:
        data = zlib.decompress(f.read())
        if b'tree' in data:
            print(data)
    # print(i)

if __name__ == '__main__':
    with open(sys.argv[1], 'rb') as f:
        data = zlib.decompress(f.read())
        print(data)

