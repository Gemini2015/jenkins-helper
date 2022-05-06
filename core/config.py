#!/usr/bin/env python
#coding:utf-8
import json
import time
import os
from . import util

class Config(object):

    def load(self, config_path):
        self.config_path = config_path
        if not self.config_path:
            print('Config.load config_path is empty')
            return False
        with open(self.config_path, "r") as f:
            self.cfg = json.load(f)
        return True

    def get_settings(self, key):
        setting = self.cfg
        if not setting[key]:
            print("Config.get_settings miss setting: " + key)
            exit(1)
        return setting[key]

    def create_log_file(self, prefix):
        # log_dir/prefix-20180517-211100.log
        time_str = time.strftime("%Y%m%d-%H%M%S", time.localtime())
        log_dir = self.get_settings("log_dir")
        file_name = prefix + "-" + time_str + ".log"
        abs_log_dir = os.path.abspath(log_dir)
        if not os.path.exists(abs_log_dir):
            os.makedirs(abs_log_dir)
        log_file = os.path.join(abs_log_dir, file_name)
        log_current_link = os.path.join(abs_log_dir, prefix + "-current.log")

        util.update_file_link(log_current_link, log_file)
        return log_file
