"""
FN split() 
Should check whether the module is real before performing a split most likely. Otherwise why would you split it.

Should handle whether there are leading '/' since /abc/1.2.3 would return version name __ and number abc
"""
import argparse
from pathlib import Path
import subprocess

def split(module):
    parts = module.split('/')

    if module.startswith('/'):
        raise ValueError("Use the format 'module_name/version_number'")

    if len(parts) != 2:
        raise ValueError("Use the format 'module_name/version_number'")

    module_name, module_version = parts[0], parts[1]
    return module_name, module_version


def is_module_published(module_name, module_version):
    command = f"module -t -r avail {module_name}/{module_version}"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return "ModuleNotFoundError" not in result.stderr

def parse():
    argParser = argparse.ArgumentParser(description="Check modules for possible problems.")
    argParser.add_argument("-c", "--check", type=str, help="the name of module to be checked")
    argParser.add_argument("-p", "--path", type=str, help="path to the module")

    args = argParser.parse_args()

    if not args.check or not args.path:
        argParser.print_help()
        raise Exception("No module to check. Provide either the module name or the path to the module.")

    if args.path:
        module_path_str = "/share/pkg.8/" + args.check
        module_path = Path(module_path_str)

        if not module_path.exists():
            print("The target directory doesn't exist")
            raise SystemExit(1)

    if args.check:
        module_name, module_version = split(args.check)
        if not is_module_published(module_name, module_version):
            print(f"The module {args.check} is not published.")
            raise SystemExit(1)

    return args.check

# # Example usage
# module_name_to_check = parse()
# print(f"Checking module: {module_name_to_check}")
