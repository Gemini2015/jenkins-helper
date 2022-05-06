#!/usr/bin/env python
#coding:utf-8

from .jenkins_connection import JenkinsConnection

class CommandBase(object):
    def __init__(self):
        self.name = 'CommandBase'

    def process_args(self, config, args):
        return True

    def do_command(self):
        return True


class JenkinsCommand(CommandBase):
    def __init__(self):
        self.name = 'JenkinsCommand'
        self.server = None

    def process_args(self, config, args):
        self.config = config
        self.args = args
        return True

    def do_command(self):
        return self.open_jenkins()

    def open_jenkins(self):
        self.server = JenkinsConnection.instance().get_jenkins_server(self.config)
        return True