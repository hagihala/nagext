#!/usr/bin/env python
# -*- coding: utf-8 -*- vim:set fileencoding=utf-8 ft=python:
import pickle
import sys
from nagext.importer import CommandList

def main():
    commands_dict = {}
    for command in CommandList():
        sys.stderr.write(command.name + "\n")
        commands_dict[command.name] = {
                'params': command.params,
                'description': command.description
                }
    pickle.dump(commands_dict, sys.stdout)

if __name__ == '__main__':
    main()
