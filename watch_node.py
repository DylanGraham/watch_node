#!/usr/bin/python2
"""
Usage: watch_node.py <comp000>
"""

import os
import re
import subprocess
import sys

watch_node_dir = '~/.watchnode'
watch_node_file = 'watchnode'


def setup_env():
    if not os.path.exists(watch_node_dir):
        os.makedirs(watch_node_dir)


def check_arg(node):
    # Check node name format
    valid = re.compile(r'^comp[0-9]{3}$')
    if not re.match(valid, node):
        print('Node name should be in the format: comp000')
        sys.exit(1)


def watch_node(node):
    with open(watch_node_dir + "/" + watch_node_file, 'a+') as fp:
        nodelist = fp.read().split()
        if node in nodelist:
            print("Node already watched")
        else:
            fp.write(node + " ")


def check_nodes():
    with open(watch_node_dir + "/" + watch_node_file, 'r') as fp:
        nodelist = fp.read().split()
        for node in nodelist:
            mdiag = subprocess.Popen(["mdiag -n | grep " + node + " | awk {'print $2'}"])
            print(node + " " + mdiag)


if __name__ == '__main__':
    node_name = None
    arg_length = len(sys.argv)
    if arg_length > 2:
        print(__doc__)
        sys.exit(1)
    elif arg_length == 2:
        node_name = sys.argv[1]

    setup_env()

    if node_name:
        check_arg(node_name)
        watch_node(node_name)
    else:
        check_nodes()
