#!/usr/bin/python3

#import command_line
import lua_parse
import module_env
import argparse


#module_path = str

def check_module_loadable(modname):
    # can the module be loaded?
    # if not published, temp publish it, then try to load it
    # if there's a lua error, print it and stop.
    stderr = module_env.module_temp_publish_and_load(modname)
    if len(stderr) > 0:
        # print(stderr)
        raise Exception(stderr)
    

def check_module_env(modname):
    # get the list of env vars from 'module help'
    help_vars = module_env.stderr_to_list(module_env.get_module_help_env_vars(modname))
    # get the dict of env vars from the shell after loading the module
    shell_vars = module_env.get_module_env_vars(...)

    
    # Is every elemtn of help_vars in shell_vars.keys() and
    # vice-versa?
    # If not, print error and stop.
    # 
    comparison_result = module_env.help_env_compare(module_env.help_env_compare(module_env.stderr_to_dictonary(module_env.get_module_env_vars(modname)), module_env.stderr_to_list(module_env.get_module_help_env_vars(modname))))
    if comparison_result:
        raise Exception(comparison_result)

    return module_env.stderr_to_dictonary(module_env.get_module_env_vars(modname))
    # ...move the valid check to step 2
    # In shell_vars, does each variable point to a valid file or directory?
    # If not, print error and stop.
    
def check_files_dirs(mod_vars):
    # look at os.path.exists()
    pass 


    

def main():
    #command_line.parse()
    # Step 0
    # Is the module loadable?
    #check_module_loadable(...)
    # Step 1
    # run module_env funcs to get a list of environment variables
    mod_vars = check_module_env(...) 
    # Step 2
    # are module env vars pointing at real files/directories?
    #
    pass


if __name__ == '__main__':
    main()

