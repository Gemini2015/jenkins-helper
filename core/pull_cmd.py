#!/usr/bin/env python
#coding:utf-8

from command import JenkinsCommand
import os
import util

class Pull(JenkinsCommand):
    def __init__(self):
        self.name = 'Pull'

    def process_args(self, config, args, backup_mode=False):
        super(Pull, self).process_args(config, args)

        if backup_mode:
            self.config_root_dir = os.path.abspath(self.config.get_settings("config_backup_dir"))
        else:
            self.config_root_dir = os.path.abspath(self.config.get_settings("config_dir"))
        self.config_root_dir = os.path.abspath(self.config.get_settings("config_dir"))
        if not os.path.exists(self.config_root_dir):
            os.makedirs(self.config_root_dir)

        return True

    def do_command(self):
        super(Pull, self).do_command()

        is_all = self.args["--all"] == "true"
        target_job_full_name = self.args["--name"]

        if is_all:
            self.pull_all_jobs()
        elif target_job_full_name != "none":
            self.pull_target_job(target_job_full_name)
        else:
            print("no target")

        return True

    def pull_target_job(self, target_job_full_name):
        job_full_name = target_job_full_name.replace(".", "/").strip().strip("/")
        if not self.server.job_exists(job_full_name):
            print("target job not exists " + job_full_name)
            return

        name_prefix, job_name = os.path.split(job_full_name)
        parent_path = util.absjoin(self.config_root_dir, name_prefix)
        if not os.path.exists(parent_path):
            os.makedirs(parent_path)

        # get job config
        job_config = self.server.get_job_config(job_full_name)
        if not job_config:
            print("job config not exists " + job_full_name)
            exit(1)

        # dump xml
        job_config_path = util.absjoin(parent_path, job_name)
        with open(job_config_path + ".xml", "w") as f:
            f.write(job_config)

    def pull_all_jobs(self):
        jobs = self.server.get_jobs()
        if not jobs:
            print("can not get jobs")
            exit(1)

        self.pull_jobs(self.config_root_dir, "", jobs)

    def pull_jobs(self, parent_path, name_prefix, jobs):
        if not os.path.exists(parent_path):
            os.makedirs(parent_path)

        for job in jobs:
            job_name = job["name"]
            job_full_name = name_prefix + "/" + job_name
            if name_prefix == "":
                job_full_name = job_name

            if "jobs" in job:
                sub_path = parent_path + "/" + job_name
                sub_jobs = job["jobs"]
                self.pull_jobs(sub_path, job_full_name, sub_jobs)
            else:
                # get job config
                job_config = self.server.get_job_config(job_full_name)
                if not job_config:
                    print("job config not exists " + job_full_name)
                    exit(1)

                # dump xml
                job_config_path = util.absjoin(parent_path, job_name)
                with open(job_config_path + ".xml", "w") as f:
                    f.write(job_config.encode("utf8"))