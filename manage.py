#!/usr/bin/env python
#coding:utf-8

"""Jenkins Helper
Usage:
    manage.py pull [--all=<all>] [--name=<job_name>]
    manage.py push [--all=<all>] [--name=<job_name>]
    manage.py -h | --help

Options:
    -h --help                   Show this screen.
    --all=<all>                 all jobs [default: false]
    --name=<job_name>           job name [default: none]

"""


from core import config, command_factory
import docopt
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

def main():
    args = docopt.docopt(__doc__, version='Jenkins Helper 1.0')
    # print(args)
    cfg = config.Config()
    cfg.root_dir = ROOT_DIR
    if not cfg.load("./config.json"):
        exit(1)

    cmd = command_factory.create(args)
    if cmd:
        cmd.process_args(cfg, args)
        cmd.do_command()
    else:
        print('command not found.')


if __name__ == '__main__':
    main()