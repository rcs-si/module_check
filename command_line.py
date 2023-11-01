import argparse
from pathlib import Path


def parse():
    argParser = argparse.ArgumentParser(description="Check modules for possible problems.")
    argParser.add_argument("-c", "--check", type=str, help="the name of module to be checked")
   # argParser.add_argument("path")
    args = argParser.parse_args()
   # import pdb ; pdb.set_trace() 
    
    if not args.check:
        argParser.print_help()
        exit(0)
        
        # raise Exception("no module to check")
    module_path_str = "/share/pkg.8/" + args.check
    module_path = Path(module_path_str)

    if not module_path.exists():
        print("The target directory doesn't exist")
        raise SystemExit(1)

    return args.check
    # for entry in module_path.iterdir():
    #     print(entry.name)

    # print("args=%s" % args)
    # print("args.name=%s" % args.name)
