# coding: utf-8
"""
Run this authorized keys hook to generate git authorized_keys file.
"""

import os, sys, re

SSH_KEY_TEMPLATE = r'command="git-server %(ssh_id)d",no-port-forwarding,no-X11-forwarding,no-agent-forwarding,no-pty %(ssh_key)s'

def bootstrap():
    print SSH_KEY_TEMPLATE
