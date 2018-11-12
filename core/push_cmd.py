#!/usr/bin/env python
#coding:utf-8

from command import JenkinsCommand
import os
import util
import jenkins

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

        if is_all:
            self.push_all_jobs()
        elif target_job_full_name != "none":
            self.push_target_job(target_job_full_name)
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