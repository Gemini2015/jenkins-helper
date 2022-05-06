#!/usr/bin/env python
#coding:utf-8

import os
import jenkins
from . import util
from .command import JenkinsCommand

class Push(JenkinsCommand):
    def __init__(self):
        self.name = 'Push'

    def process_args(self, config, args):
        super(Push, self).process_args(config, args)

        self.config_root_dir = os.path.abspath(self.config.get_settings("config_dir"))

        return True

    def do_command(self):
        super(Push, self).do_command()

        is_all = self.args["--all"] == "true"
        target_job_full_name = self.args["--name"]
        target_job_rel_path = self.args["--path"]

        if is_all:
            self.push_all_jobs()
        elif target_job_full_name != "none":
            self.push_target_job(target_job_full_name)
        elif target_job_rel_path  != "none":
            self.push_target_job_by_path(target_job_rel_path)
        else:
            print("no target")

        return True

    def push_target_job(self, target_job_full_name):
        job_full_name = target_job_full_name.replace(".", "/").strip().strip("/")
        if not self.server.job_exists(job_full_name):
            # create job
            job_nodes = job_full_name.split("/")[:-1]
            if len(job_nodes) > 1:
                name_prefix = ""
                for node in job_nodes:
                    temp_job_full_name = name_prefix + "/" + node
                    if name_prefix == "":
                        temp_job_full_name = node
                    if not self.server.job_exists(temp_job_full_name):
                        self.server.create_job(temp_job_full_name, jenkins.EMPTY_FOLDER_XML)
                    name_prefix = temp_job_full_name
            self.server.create_job(job_full_name, jenkins.EMPTY_CONFIG_XML)

        # update job
        job_config_path = util.absjoin(self.config_root_dir, job_full_name)
        with open(job_config_path + ".xml", "r") as f:
            job_config = f.read().decode("utf8")

        self.server.reconfig_job(job_full_name, job_config)

    def push_target_job_by_path(self, target_job_rel_path):
        abs_path, abs_ext = os.path.splitext(os.path.abspath(target_job_rel_path).replace("\\", "/"))
        config_root_dir = self.config_root_dir.replace("\\", "/")
        full_name = abs_path.replace(config_root_dir, "")
        if full_name[0] == '/':
            full_name = full_name[1:]

        print('push_target_job_by_path ' + target_job_rel_path + " full_name " + full_name)
        self.push_target_job(full_name)

    def push_all_jobs(self):
        pass
        # jobs = self.server.get_jobs()
        # if not jobs:
        #     print("can not get jobs")
        #     exit(1)

        # self.push_jobs(self.config_root_dir, "", jobs)

    # def push_jobs(self, parent_path, name_prefix, jobs):
    #     if not os.path.exists(parent_path):
    #         os.makedirs(parent_path)

    #     for job in jobs:
    #         job_name = job["name"]
    #         job_full_name = name_prefix + "/" + job_name
    #         if name_prefix == "":
    #             job_full_name = job_name

    #         if "jobs" in job:
    #             sub_path = parent_path + "/" + job_name
    #             sub_jobs = job["jobs"]
    #             self.push_jobs(sub_path, job_full_name, sub_jobs)
    #         else:
    #             # get job config
    #             job_config = self.server.get_job_config(job_full_name)
    #             if not job_config:
    #                 print("job config not exists " + job_full_name)
    #                 exit(1)

    #             # dump xml
    #             job_config_path = util.absjoin(parent_path, job_name)
    #             with open(job_config_path + ".xml", "w") as f:
    #                 f.write(job_config.encode("utf8"))

    def backup_target_job(self):
        pass