# To change this template, choose Tools | Templates
# and open the template in the editor.

import os
import sys
import errno
from db_base import *

COMMANDS_READONLY = [
    'git-upload-pack',
    'git upload-pack',
    ]

COMMANDS_WRITE = [
    'git-receive-pack',
    'git receive-pack',
    ]

db_connect()
def admin_config():
    return (
     'admin',
     '123456',
     'lan_chi@foxmail.com',
     'www.iforeach.com',
     'Init the git server config'
    )
db_query("INSERT INTO `users`(login, passwd, email, location, description, created_at, updated_at) VALUES('%s', MD5('%s'), '%s', '%s', '%s', NOW(), NOW())", admin_config())



