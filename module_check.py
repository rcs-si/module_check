#!/usr/bin/python3

import command_line
import module_env
import argparse


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
    

    
    
def check_files_dirs(modname):
    # look at os.path.exists()
    shell_varibles = module_env.stderr_to_dictonary(module_env.get_module_env_vars(modname))
    module_env.is_env_variable_valid_file_or_directory(shell_varibles)
    


#for world writability, os.walk through the full directory path and save
#find a way to check for the world writability of each
#find all *.so files or *.so.* and check executability     
#check symlinks and follow them or apply os.realpath to everything
    

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
    pass


if __name__ == '__main__':
    main()

