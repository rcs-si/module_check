#!/usr/bin/python3

import command_line
import module_env
import argparse

'''
import module_check
main():
    args 
    module_env.BASE_DIR=args.module_dir
'''

#module_path = str

def check_module_loadable(modname):
    # can the module be loaded?
    # if not published, temp publish it, then try to load it
    # if there's a lua error, print it and stop.
    stderr = module_env.module_temp_publish_and_load(modname)
    if len(stderr) > 0:
        msg = '*** Module could not be loaded ***\n'  
        raise Exception(msg + stderr)
    

def check_module_env(modname):
    # get the list of env vars from 'module help'
    help_vars = module_env.stderr_to_list(module_env.get_module_help_env_vars(modname))
    # get the dict of env vars from the shell after loading the module
    shell_vars = module_env.stderr_to_dictonary(module_env.get_module_env_vars(modname))

    
    # Is every elemtn of help_vars in shell_vars.keys() and
    # vice-versa?
    # If not, print error and stop.
    # 
    comparison_result = module_env.help_env_compare(module_env.stderr_to_dictonary(module_env.get_module_env_vars(modname)), module_env.stderr_to_list(module_env.get_module_help_env_vars(modname)))
    if comparison_result:
        msg = '*** Environment variable incorrect ***\n'
        raise Exception(msg + comparison_result)
    
    #why does this return statment exist?
    return module_env.stderr_to_dictonary(module_env.get_module_env_vars(modname))
    
    # ...move the valid check to step 2
    # In shell_vars, does each variable point to a valid file or directory?
    # If not, print error and stop.
    

    
    
# def check_files_dirs(modname):
#     # look at os.path.exists()
#     shell_variables = module_env.stderr_to_dictonary(module_env.get_module_env_vars(modname))
#     module_env.is_env_variable_valid_file_or_directory(shell_variables)
    
    
def check_files_dirs(shell_variables):
    problematic_variables = module_env.is_env_variable_valid_file_or_directory(shell_variables)
    if problematic_variables:
        print("These are not files or directories!")
        print("Bad variables:", problematic_variables)
        raise Exception("One or more environment variables are not valid files or directories.")


#for world writability, os.walk through the full directory path and save
#find a way to check for the world writability of each
#find all *.so files or *.so.* and check executability     
#check symlinks and follow them or apply os.realpath to everything
    

# may work? Other implementation possible by running a command?
def check_world_writability_and_executability(directory):
    problematic_items = []

    for root, dirs, files in os.walk(directory):
        for item in dirs + files:
            item_path = os.path.join(root, item)
            is_symlink = os.path.islink(item_path)

            # Resolve symbolic links
            if is_symlink:
                item_path = os.path.realpath(item_path)

            # Check world-writability
            if os.access(item_path, os.W_OK) and not is_symlink:
                problematic_items.append((item_path, "World-writable"))

            # Check executability for shared object files
            if item.endswith(".so") or ".so." in item:
                if os.access(item_path, os.X_OK):
                    problematic_items.append((item_path, "Executable"))

    return problematic_items


def main():
    modname = command_line.parse()
    # Step 0
    # Is the module loadable?
    check_module_loadable(modname)
    # Step 1
    # run module_env funcs to get a list of environment variables
    #check_module_env(...)
    check_module_env(modname) 
    # Step 2
    # are module env vars pointing at real files/directories?
    #
    check_files_dirs(modname)

    # Step 3
    # Next check: check *ENTIRE* module install directory tree
    # and make sure there are no files with the "anyone writable" permission.
    # ls -l util.h
    # -rwxrwxr-x 1 milechin scv   2141 Mar 29 11:00 util.h
    #         * <- looking for that entry to be a w 
    # accessible thru the os.stat() function -> look for st_mode
    # then research how to interpret that result.

    # Step 4
    # Look for modules that don't have their long description filled in

if __name__ == '__main__':
    main()

