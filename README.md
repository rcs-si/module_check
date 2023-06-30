# module_env_check
Given an SCC module file name, check if the listed environment variables are defined and if their definition is valid.

## Usage
```
module_env_check --help
# module_env_check <module_name[/version]>
```

For example:
```
module_env_check bedtools/2.30.0
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
