import subprocess
import tempfile
import os
import shlex

def is_module_loadable(modname):
  ''' Can module "modname" be loaded? '''
  # subprocess --> capture STDERR (or both)
  # Look for string:
  #   The following module(s) are unknown: "modname"
  # if found return False else True

  result = subprocess.run(["module load " + modname], shell=True, stderr=subprocess.PIPE)
  stderr = result.stderr.decode("utf-8")
  target_substring = "The following module(s) are unknown: "
  index = stderr.find(target_substring)
  if index != -1:
    return False
  return True

def module_temp_publish_and_load(modname):
  tmpdirname = tempfile.TemporaryDirectory()
  modpath = os.path.join(tmpdirname.name,modname)
  os.makedirs(modpath)
  # hard encoding pkg.8 will want to come back and add functionality for different paths
  version = modname.split("/")[1]
  os.symlink(os.path.join('/share/pkg.8',modname,'modulefile.lua'), os.path.join(modpath, version + ".lua"))
  command = f'module use {tmpdirname.name} && module load {modname}'
  
  result = subprocess.run([command], shell=True, stderr=subprocess.PIPE)
  stderr = result.stderr.decode("utf-8")
  return stderr
  


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
    command = f'module help {modname}'
  else:
    modpath = os.path.join(tmpdirname.name,modname)
    os.makedirs(modpath)
    # hard encoding pkg.8 will want to come back and add functionality for different paths
    version = modname.split("/")[1]
    os.symlink(os.path.join('/share/pkg.8',modname,'modulefile.lua'), os.path.join(modpath, version + ".lua"))
    command = f'module use {tmpdirname.name} && module help {modname}'
  
  result = subprocess.run([command], shell=True, stderr=subprocess.PIPE)
  stderr = result.stderr.decode("utf-8")
  return stderr
  # make a subdir tmpdirname.name/module_name
  # and in there make a symlink to /share/pkg.8/module_name/version/modulefile.lua
  # called "version.lua"
  # 
#print(get_module_help_env_vars("modloadtest/1.0"))
  # Now call "module help" and get the STDERR 
   # if tmpdirname is not None then call "module use tmpdirname && module help"
  # Check STDERR for $SCC_MODULENAME_BLAH
  # and return a dictionary of those. 

  # use split command to split into lines then go on line by line basis and extact the SCC variables without $ to a dictonary to be returned

def stderr_to_list(stderr):
  output = stderr.split("\n")
  #print(output)
  result_list = []
  for item in output:
    x = item.find("$SCC_")
    y = item.find(" --")
    #print(x, y)
    if x != -1:
      result_list.append(item[x+1:y]) 
  return result_list

#print(stderr_to_list(get_module_help_env_vars("modloadtest/1.0")))


  
def get_module_env_vars(modname):
  ''' Similar to get_module_help_env_vars but loads the module and runs:
      module load modname && env | grep SCC_MODULE_NAME
      and then returns the discovered env variables to another dictonary'''
  # split on the equal sign and put into dictonary where path is value and env variable is key
  #
  #
  tmpdirname = tempfile.TemporaryDirectory()
  if is_module_loadable(modname):
    module_name = modname.split('/')[0].upper()
    command = f'module load {modname} && env | grep SCC_' + module_name
  else:
    modpath = os.path.join(tmpdirname.name,modname)
    os.makedirs(modpath)
    # hard encoding pkg.8 will want to come back and add functionality for different paths
    version = modname.split("/")[1]
    os.symlink(os.path.join('/share/pkg.8',modname,'modulefile.lua'), os.path.join(modpath, version + ".lua"))
    module_name = modname.split('/')[0].upper()

    command = f'module use {tmpdirname.name} && module load {modname} && env | grep SCC_' + module_name
  result = subprocess.run([command], shell=True, stdout=subprocess.PIPE)
  stdout = result.stdout.decode("utf-8")
  return stdout

#print(get_module_env_vars("modloadtest/1.0"))
#print(get_module_env_vars("quantumespresso/7.2"))
#print(stderr_to_list(get_module_help_env_vars("quantumespresso/7.2")))


def stderr_to_dictonary(stderr):
  
  output = stderr.split("\n")
  #print(output)
  result_dict = {}
  for item in output:
    x = item.find("=")
    if x != -1:
      #print(x)
      result_dict.update({item[0:x]:item[x+1:len(item)]})
  
  return result_dict

#print(stderr_to_dictonary(get_module_env_vars("modloadtest/1.0")))

def help_env_compare(help_vars, env_vars):
  #check help in env and env in help
  for var in help_vars:
    if var not in env_vars:
      #return the mismatched variable otherwise return none
      return var
  for var in env_vars:
    if var not in help_vars:
      return var
    
  return None

#print(help_env_compare(stderr_to_dictonary(get_module_env_vars("modloadtest/1.0")), stderr_to_list(get_module_help_env_vars("modloadtest/1.0"))))
  
#two checks one if the help and env agree on the ariables and second if the env paths auctually lead to something


# def stderr_to_dictonary(stderr):
#   output = stderr.split("\n")
#   print(output)
#   result_dict = {}
#   counter = 1
#   for item in output:
#     x = item.find("$")
#     y = item.find(" --")
#     print(x, y)
#     if x != -1:
#       result_dict.update({counter:item[x+1:y]})
#       counter+=1
  
#   return result_dict

# print(stderr_to_dictonary(get_module_help_env_vars("modloadtest/1.0")))


#takes dictionary of shell variables and checks if they are value for each key is valid file or directory
def is_env_variable_valid_file_or_directory(shell_variables):
  for var, path in shell_variables.items():
    if not os.path.exists(path):
      raise Exception("Env variable: " + var +" which points to " + path + " is not a valid file or directory")
    
#print(stderr_to_dictonary(get_module_env_vars("modloadtest/4.0")))    
#is_env_variable_valid_file_or_directory(stderr_to_dictonary(get_module_env_vars("modloadtest/4.0")))

"""
note on how to test: "module use /share/module.8/test" otherwise it will reference strange path for variables ie: ..../4.0/4.0/install/bin
also if making new modloadtest version must create with module load newpkg in share/pkg.8/modloadtest 
and then create symlink in /share/module.8/test/modloadtest
"""