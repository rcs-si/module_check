# module_show_parse

import subprocess

def module_show(x):
    result = subprocess.run(['module', 'show', x], stdout=subprocess.PIPE).stdout.decode('utf-8')
    print(result)
    # subprocess.call(["bash", "module show " + x])

module_show("bwa/0.7.17")
