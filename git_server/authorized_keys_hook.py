# coding: utf-8
"""
Run this authorized keys hook to generate git authorized_keys file.
"""

import os, sys, re

from db_base import *

SSH_KEY_TEMPLATE = r'command="git-server %(ssh_id)d",no-port-forwarding,no-X11-forwarding,no-agent-forwarding,no-pty %(ssh_key)s'

AUTHORIZED_KEYS_PATH = r'~/.ssh/authorized_keys'

def get_ssh_records():
    db_connect()
    authorized_keys = list()
    # get all record from mysql
    res = db_query("SELECT id AS ssh_id, ssh_key AS ssh_key FROM {sshes} ORDER BY updated_at DESC")
    if db_affected_rows(res) > 0:
        while True:
            ssh = db_fetch_hash(res)
            if ssh is None:
                break
            authorized_keys.append(SSH_KEY_TEMPLATE % ssh)
    return "\n".join(authorized_keys)

def write_authorized_sshes(records):
    auth_key_path = os.path.expanduser(AUTHORIZED_KEYS_PATH)
    dirname       = os.path.dirname(auth_key_path)
    if not os.path.exists(dirname):
        os.mkdir(dirname)

    with open(auth_key_path, 'w') as f:
        f.write("%s" % records)

def bootstrap():
    records = get_ssh_records()
    write_authorized_sshes(records)

    #print SSH_KEY_TEMPLATE
