#!/usr/bin/env python
#coding:utf-8

import jenkins

class JenkinsConnection(object):
    def __init__(self):
        self.name = 'JenkinsConnection'
        self.server = None

    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(JenkinsConnection, "_instance"):
            JenkinsConnection._instance = JenkinsConnection(*args, **kwargs)
        return JenkinsConnection._instance

    def get_jenkins_server(self, config):
        if self.server:
            return self.server

        self.config = config
        self.host = self.config.get_settings("host")
        self.username = self.config.get_settings("username")
        self.token = self.config.get_settings("token")

        if not self.host or not self.username or not self.token:
            print("invalid jenkins args")
            exit(1)

        self.server = jenkins.Jenkins(self.host, username=self.username, password=self.token)
        if not self.server:
            print("open jenkins error")
            exit(1)

        user = self.server.get_whoami()
        version = self.server.get_version()
        print(self.username + " open jenkins " + self.host + " v" + version)
        return self.server