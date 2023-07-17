#!/usr/bin/python3

import command_line
import lua_parse

module_path = str
def main():
    command_line.parse()
    module_path = command_line.module_name
    module_path


if __name__ == '__main__':
    main()

