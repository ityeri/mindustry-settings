import zlib
from io import BytesIO
import glob
import os


def read_java_utf8(f: BytesIO) -> str:
    length = int.from_bytes(f.read(2), byteorder='big', signed=False)
    return f.read(length).decode('utf-8')


for file_path in glob.glob('./*.msch'):
    print(f'Checking "{file_path}" ...')
    try:
        with open(file_path, 'rb') as f:
            if f.read(4) != b'msch':
                raise ValueError('File is not msch format')

            ver = int.from_bytes(f.read(1))

            if ver != 1:
                print('Version number is not recognizable. ignore')

            decomp = zlib.decompressobj()
            body_bytes = decomp.decompress(f.read())

            body = BytesIO(body_bytes)

            width = int.from_bytes(body.read(2), byteorder='big')
            height = int.from_bytes(body.read(2), byteorder='big')

            tags = int.from_bytes(body.read(1), signed=False)
            tag_map = {
                read_java_utf8(body): read_java_utf8(body)
                for i in range(tags)
            }

            new_name = tag_map['name']
            new_name = new_name.replace('/', '_')
            new_file_name = new_name + '.msch'

            os.rename(file_path, new_file_name)

        print(f'Renamed: "{file_path}" -> "{new_file_name}"')

    except FileNotFoundError:
        print('File not found. skip')
        print(file_path)