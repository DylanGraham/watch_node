#!/usr/bin/python2
"""
Usage: watch_node.py [comp000]
"""

import email_details
import os
import re
import smtplib
import subprocess
import sys
from email.mime.text import MIMEText

watch_node_dir = os.path.expanduser("~") + '/.watchnode'
watch_node_file = watch_node_dir + '/watchnode'


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
    with open(watch_node_file, 'a+') as fp:
        nodelist = fp.read().split()
        if node in nodelist:
            print("Node already watched")
        else:
            fp.write(node + " ")


def check_nodes():
    if os.path.isfile(watch_node_file):
        with open(watch_node_file, 'r') as fp:
            nodelist = fp.read().split()
            still_watch = []
            for node in nodelist:
                p1 = subprocess.Popen(["/usr/local/bin/qstat -n | grep " + node], shell=True, stdout=subprocess.PIPE)
                if not p1.communicate()[0]:
                    send_email(node)
                else:
                    still_watch.append(node)

        with open(watch_node_file, 'w') as fp:
            for node in still_watch:
                fp.write(str(node) + " ")


def send_email(node):
    sender = email_details.from_address
    recipient = email_details.to_address
    msg = MIMEText(node + ' is idle')
    msg['Subject'] = 'watched node ' + node + ' is now free'
    msg['From'] = sender
    msg['To'] = recipient
    s = smtplib.SMTP()
    s.connect(email_details.mailserver)
    s.sendmail(sender, recipient, msg.as_string())
    s.quit()


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
