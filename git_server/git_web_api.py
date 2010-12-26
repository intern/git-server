"""
  You can use it to operate git projects:
    - git_API_init
    - git_API_rename
    - git_API_move
    - git_API_copy
    - git_API_delete
    - git_API_exists
    - git_API_run_key_hook
"""

import os, sys

import git_status as EXIT

from optparse import OptionParser

from git_repository import *

GIT_WEB_APIs = ['git_API_init', 'git_API_rename', 'git_API_move', 'git_API_copy', 'git_API_delete', 'git_API_exists', 'git_API_run_key_hook']

# API for git init a project
#   params:
#       user       *require
#       repository *require
def git_API_init(*args, **k_args):
    git_initialize(*args, **k_args)

# API for rename a git project name
#   @see git_API_move
def git_API_rename(*args, **k_args):
    git_move(*args, **k_args)

# API for move a git to target path
#   alias git_API_rename
def git_API_move(*args, **k_args):
    git_move(*args, **k_args)

# API for copy a exists git project
def git_API_copy(*args, **k_args):
    git_copy(*args, **k_args)

# API for delete a exists project
def git_API_delete(*args, **k_args):
    git_delete(*args, **k_args)

# API for check the git project exists
def git_API_exists(*args, **k_args):
    git_exists(*args, **k_args)

# API for append ssh key to ~/.ssh/authorized_keys
def git_API_run_key_hook(*args, **k_args):
    return os.system("run-auth-keys-hook")

# API main action handle to OP all sports
def git_API_action():
    __action_boot()

def __action_boot():
    parser = OptionParser()
    parser.add_option(
        "-a",
        "--action",
        dest="action",
        type="string",
        help="the git API action eg: init, rename, move, copy, delete"
    )
    options, args = parser.parse_args()
    if options.action is None:
        sys.exit(EXIT.API_NO_ACTION)
    API_callback = "git_API_%s" % options.action
    if API_callback in GIT_WEB_APIs:
        globals()[API_callback](*args)
    else:
        sys.exit(EXIT.API_NO_ACTION)
