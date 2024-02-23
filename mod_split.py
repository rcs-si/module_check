"""
Should check whether the module is real before performing a split most likely. Otherwise why would you split it.

Should handle whether there are leading '/' since /abc/1.2.3 would return version name __ and number abc
"""

def split(module):
    if module.startswith('/'):
        raise ValueError("Use the format 'module_name/version_number'")

    # use split fn to split the abc and 1.2.3 in module abc/1.2.3
    parts = module.split('/')

    # Extracting module name and version
    module_name = parts[0]
    module_version = parts[1] # MIGHT NEED LATER. DUMB WAY OF HANDLING IT: if len(parts) > 1 else None. 
    
    return module_name, module_version


module = "abc/1.23.0"
module_name, module_version = split(module)
print("Module Name:", module_name)
print("Module Version:", module_version)