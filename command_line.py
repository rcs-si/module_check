import argparse



def parse():
    argParser = argparse.ArgumentParser(description="Check modules for possible problems.")
    argParser.add_argument("-n", "--name", help="name of module to be checked")
    args = argParser.parse_args()
    print("args=%s" % args)
    print("args.name=%s" % args.name)