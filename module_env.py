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
  if stderr != None:
    print(stderr)
    return
  return
  


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
  print(output)
  result_list = []
  for item in output:
    x = item.find("$")
    y = item.find(" --")
    print(x, y)
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
    command = f'module load {modname} && env | grep SCC_'
  else:
    modpath = os.path.join(tmpdirname.name,modname)
    os.makedirs(modpath)
    # hard encoding pkg.8 will want to come back and add functionality for different paths
    version = modname.split("/")[1]
    os.symlink(os.path.join('/share/pkg.8',modname,'modulefile.lua'), os.path.join(modpath, version + ".lua"))
    command = f'module use {tmpdirname.name} && module load {modname} && env | grep SCC_'
  result = subprocess.run([command], shell=True, stdout=subprocess.PIPE)
  stdout = result.stdout.decode("utf-8")
  return stdout

#print(get_module_env_vars("modloadtest/1.0"))


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

print(stderr_to_dictonary(get_module_env_vars("modloadtest/1.0")))

def help_env_compare(help_vars, env_vars):
  if env_vars.keys() == help_vars:
    return True
  return False


  
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