#CHANGED README FOR GIT TEST

# module_check
Given an SCC module file name, check it for possible problems.

## Possible problems in module files
1. Environment variable is listed in "module show" output but is not defined
2. Environment variable is defined, but incorrectly
3. Directories or files are world-writable
4. Directories of files that should not be accessible to a user are not readable or executable

*Note*: the program should be flexible to handle both "lua" and "tcl" modules

## Usage
```
module_check --help
# module_check <module_name[/version]>
```

For example:
```
module_check /path/to/bedtools/2.30.0/modulefile.lua
```

Project: module_check

Clone this to your /projectnb/rcs-intern/

Write python code (not notebook)
* The main file will be called "module_check.py".  
* Use the `__name__==__main__` convention: https://realpython.com/if-name-main-python/
* Run with the system python3: `#!/usr/bin/python3` 
* Make your code modular (for each task write a separate function in a separate file)
* Use the argparse library to handle command line arguments
* a function that processes the command line
* Environment variable is listed in "module show" output but is not defined
 probably just parse the module file directly, without preloading.
* Environment variable is defined, but incorrectly
* Directories or files are world-writable
* Directories of files that should be accessible to a user are not readable or executable
* Please document all progress 
