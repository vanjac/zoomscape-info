# KA Archive extractor

import sys, struct, os.path, os

def main():
    filepath = sys.argv[1]
    dirname = os.path.basename(filepath).replace(".", "_")
    with open(filepath, 'rb') as f:
        def read_uint16():
            return struct.unpack('<H', f.read(2))[0]
        def read_uint32():
            return struct.unpack('<I', f.read(4))[0]
        def read_string(len):  # null terminated
            return f.read(len).split(b'\0', 1)[0].decode("utf-8")

        magic = f.read(10)
        if magic != b'KA Archive':
            print("Not a KA Archive file!")
            return

        f.seek(0x14, 0)
        num_files = read_uint16()
        print(num_files, "files")
        entries = []
        for i in range(0, num_files):
            name = read_string(13)
            offset = read_uint32()
            len = read_uint32()
            entries.append((name, offset, len))

        print("Extracting to", dirname)
        if not os.path.isdir(dirname):
            os.mkdir(dirname)

        for entry in entries:
            name, offset, len = entry
            print(name)
            f.seek(offset, 0)
            data = f.read(len)
            with open(dirname + os.path.sep + name, 'wb') as out_f:
                out_f.write(data)
    print("Done")

if __name__ == "__main__":
    main()