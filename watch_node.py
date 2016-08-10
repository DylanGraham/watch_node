#!/usr/bin/python2
"""
Usage: watch_node.py <comp000>
"""

import os
import re
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
    with open(watch_node_dir + "/" + watch_node_file, 'a') as fp:
        fp.write(node + "\n")


def check_nodes():
    with open(watch_node_dir + "/" + watch_node_file, 'r') as fp:
        pass


if __name__ == '__main__':
    if len(sys.argv) > 2:
        print(__doc__)
        sys.exit(1)

    setup_env()

    if sys.argv[1]:
        check_arg(sys.argv[1])
        watch_node(sys.argv[1])
    else:
        check_nodes()
