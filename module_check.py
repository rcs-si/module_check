#!/usr/bin/python3

#import command_line
import lua_parse
import module_env
import argparse


#module_path = str

def check_module_loadable(...):
    # can the module be loaded?
    # if not published, temp publish it, then try to load it
    # if there's a lua error, print it and stop.
    pass

def check_module_env(...):
    # get the list of env vars from 'module help'
    help_vars = module_env.get_module_help_env_vars(...)
    # get the dict of env vars from the shell after loading the module
    shell_vars = module_env.get_module_env_vars(...)
    # Is every elemtn of help_vars in shell_vars.keys() and
    # vice-versa?
    # If not, print error and stop.
    # In shell_vars, does each variable point to a valid file or directory?
    # If not, print error and stop.


    

def main():
    #command_line.parse()
    # Step 0
    # Is the module loadable?
    #check_module_loadable(...)
    # Step 1
    # run module_env funcs to get a list of environment variables
    check_module_env(...) 
 
    


if __name__ == '__main__':
    main()

