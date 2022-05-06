#!/usr/bin/env python
#coding:utf-8
from .command import CommandBase
from .pull_cmd import Pull
from .push_cmd import Push

commands = {
    'pull': Pull,
    'push': Push
}

# class CommandFactory(object):
def create(args):
    class_type = None
    for key in commands:
        if args[key]:
            class_type = commands[key]
    if class_type:
        return class_type()
    else:
        return CommandBase()
    return None
