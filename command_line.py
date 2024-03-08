import argparse
from pathlib import Path


"""
FN split() 
Should check whether the module is real before performing a split most likely. Otherwise why would you split it.

Should handle whether there are leading '/' since /abc/1.2.3 would return version name __ and number abc
"""

def split(module):
    # use split fn to split the abc and 1.2.3 in module abc/1.2.3
    parts = module.split('/')

    if module.startswith('/'):
        raise ValueError("Use the format 'module_name/version_number'")

    if len(parts) != 2:
        raise ValueError("Use the format 'module_name/version_number'")

    # Extracting module name and version
    module_name = parts[0]
    module_version = parts[1]
    
    return module_name, module_version

#### test case for split
# module = "abc/1.23.0"
# module_name, module_version = split(module)
# print("Module Name:", module_name)
# print("Module Version:", module_version)


def parse():
    argParser = argparse.ArgumentParser(description="Check modules for possible problems.")
    argParser.add_argument("-c", "--check", type=str, help="the name of module to be checked")
    argParser.add_argument("-p", "--path", type=str, help="path to the module")

    args = argParser.parse_args()
   # import pdb ; pdb.set_trace() 
    
    ## PREVIOUS VERSION
    #if not args.check:
     #   argParser.print_help()
     #   exit(0)
        
        # raise Exception("no module to check")

    if not args.check or not args.path:
        argParser.print_help()
        raise Exception("No module to check. Provide either the module name or the path to the module.")
        #exit(0)


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
