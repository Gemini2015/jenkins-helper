#!/usr/bin/env python
#coding:utf-8
import os
import re
import sys

def absjoin(a, b):
    return os.path.abspath(os.path.join(a, b))

def exe_cmd(cmd):
    print(cmd)
    result = os.system(cmd)
    return result

def update_file_link(link_file, dst_file):
    # touch dst_file
    if not os.path.exists(dst_file):
        file = open(dst_file, "w")
        file.close()
    # remove old link
    if os.path.lexists(link_file):
        if sys.platform.startswith('win32'):
            os.system("del %s" % (os.path.abspath(link_file)))
        else:
            os.remove(link_file)
    # create new link
    if sys.platform.startswith('win32'):
        os.system("mklink %s %s" % (os.path.abspath(link_file), os.path.abspath(dst_file)))
    elif sys.platform.startswith('darwin'):
        os.symlink(dst_file, link_file)
    else:
        print("update_file_link not support")
