# coding: utf-8
"""
  Management project structure and initialization
    commit repository if it's exists, or create it and commit.
      - initialize
      - move
      - copy
      - delete
"""
import os, sys, subprocess, shutil

from db_base import *

GIT_ROOT = os.path.expanduser("~/repositories")

def commit_repository(path, action = None):
    full_path = "%s/%s" % (GIT_ROOT, path)
    if not os.path.exists( full_path):
        os.makedirs(full_path)
        git_initialize(full_path)
    return full_path


def git_commit(full_path):
    pass

def git_initialize(full_path):
    args = ['git', '--git-dir=.', 'init']
    return_code = subprocess.call(args=args, cwd=full_path, stdout=sys.stderr, close_fds=True)
    if not return_code is 0:
        sys.exit(1)

def git_copy(full_path, new_path):
    pass

def git_move(full_path, new_path):
    pass

def git_delete(full_path, new_path):
    pass
