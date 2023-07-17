import argparse
from pathlib import Path


def parse():
    argParser = argparse.ArgumentParser(description="Check modules for possible problems.")
    # argParser.add_argument("-p", "--path", help="path to .lua or .tcl file of module to be checked")
    argParser.add_argument("path")
    args = argParser.parse_args()
    module_path = Path(args.path)
    

    # print(module_path)

    print(Path.cwd())

    if not module_path.exists():
        print("The target directory doesn't exist")
        raise SystemExit(1)

    for entry in module_path.iterdir():
        print(entry.name)

    # print("args=%s" % args)
    # print("args.name=%s" % args.name)
