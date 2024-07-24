"""
FN split() 
Should check whether the module is real before performing a split most likely. Otherwise why would you split it.

Should handle whether there are leading '/' since /abc/1.2.3 would return version name __ and number abc
"""
import argparse
from pathlib import Path
import subprocess
import os

DEFAULT_PATH = "/share/pkg.8/"

def is_module_published(module_name, module_version):
    command = f"module -t -r avail {module_name}/{module_version}"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return len(result.stderr) > 0

def split(module):
    parts = module.split('/')

    if module.startswith('/'):
        raise ValueError("Use the format 'module_name/version_number'")

    if len(parts) != 2:
        raise ValueError("Use the format 'module_name/version_number'")

    module_name, module_version = parts[0], parts[1]
    return module_name, module_version

def parse():
    argParser = argparse.ArgumentParser(description="Check modules for possible problems.")
    argParser.add_argument("-c", "--check", type=str, help="the name of module to be checked", required=True)
    argParser.add_argument("-p", "--path", type=str, help="path to the module")

    args = argParser.parse_args()

    module_path_str = os.path.join(DEFAULT_PATH, args.check)

    if args.path:
        module_path_str = os.path.join(args.path, args.check)

    module_path = Path(module_path_str)

    # R uses a capital R for the module name but is lower-cased in /share/pkg.X/r 
    # ...implement a specific fix for this and the other handful of module names
    # with uppercase in the published name in the future. 
    
    module_name, module_version = split(args.check)
    if not is_module_published(module_name, module_version):
        print(f"The module {args.check} is not published. Check spelling of module or path for correctness.")
        #raise SystemExit(1)

    return args.check

# # Example usage
# module_name_to_check = parse()
# print(f"Checking module: {module_name_to_check}")
