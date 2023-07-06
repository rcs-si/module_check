# module_check
Given an SCC module file name, check it for possible problems.

## Possible problems
1. Environment variable is listed in "module show" output but is not defined
2. Environment variable is defined, but incorrectly
3. Directories or files are world-writable
4. Directories of files that should be accessible to a user are not readable or executable

## Usage
```
module_check --help
# module_env_check <module_name[/version]>
```

For example:
```
module_check bedtools/2.30.0
```


Project: module_env_check

Clone this to your /projectnb/rcs-intern/

Write python code (not notebook)

Make your code modular (for each task write a separate function)

a function that processes the command line
a function that gets a list of all env. variables that are listed in the module show command
etc.
a function that processes module show command and grabs all strings that start with a "$"
a function that loads other necessary modules if required
