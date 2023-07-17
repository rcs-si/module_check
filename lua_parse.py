# parse .lua file

def open_file(path):
    with open(path, 'r') as f:
        data = f.read()