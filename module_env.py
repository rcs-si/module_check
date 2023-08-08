import subprocess
import tempfile


def is_module_loadable(modname):
  ''' Can module "modname" be loaded? '''
  # subprocess --> capture STDERR (or both)
  # Look for string:
  #   The following module(s) are unknown: "modname"
  # if found return False else True

  result = subprocess.run(["module load " + modname], shell=True, stderr=subprocess.PIPE)
  #error = subprocess.check_output(["module load", modname], stderr=subprocess.STDOUT)
  print(result.stderr)
  target_substring = "The following module(s) are unknown: "
  index = result.stderr.find(target_substring.encode())
  if index != -1:
    print(f"The substring was found.")
  else:
    print("The substring was not found.")


is_module_loadable("chess")


# Goal: call "module help modname/ver" whether it's published
# or not
def get_module_help_env_vars(modname):
  ''' Get the names of the environment variables defined in modname
      modname: string of form   module_name/version '''
  # Can it be loaded? 
  # yes -> tmpdirname = None
  # If not - temporarily publish to a temp dir.
  tmpdirname = tempfile.TemporaryDirectory()
  if is_module_loadable(modname):
    tmpdirname = None
  else:
    result = subprocess.run(["cd" + tmpdirname + "&& mkdir" + modname])

  
  # make a subdir tmpdirname.name/module_name
  # and in there make a symlink to /share/pkg.8/module_name/version/modulefile.lua
  # called "version.lua"
  # 
  # Now call "module help" and get the STDERR 
   # if tmpdirname is not None then call "module use tmpdirname && module help"
  # Check STDERR for $SCC_MODULENAME_BLAH
  # and return a dictionary of those. 

  
def get_module_env_vars(modname):
  ''' Similar to get_module_help_env_vars but loads the module and runs:
      module load modname && env | grep SCC_MODULE_NAME
      and then returns the discovered env variables '''
  
