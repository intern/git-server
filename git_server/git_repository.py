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

import git_status as EXIT

from db_base import *

# git repository root.
GIT_ROOT = os.path.join(os.path.expanduser("~"), "repositories")

# git commit hook, used with `git-server`
def git_commit(user, repository):
    full_path = os.path.join(GIT_ROOT, user, repository)
    #if not os.path.exists( full_path):
        #os.makedirs(full_path)
        #git_initialize(full_path)
    return full_path

# Create git project and init this
#   @public
def git_initialize(user, repository):
    full_path = os.path.join(GIT_ROOT, user, repository)
    if __git_exists(full_path):
       #debug here.
       sys.exit(EXIT.API_GIT_ALREADY_EXISTS)
    os.makedirs(full_path)
    args = ['git', '--git-dir=.', 'init']
    return_code = subprocess.call(args=args, cwd=full_path, stdout=sys.stderr, close_fds=True)
    if not return_code is 0:
        sys.exit(EXIT.API_GIT_INIT_ERROR)

# Copy project, a api helper
#   @public
def git_copy(user, repository, new_repository, new_user = None):
    if new_user is None:
        new_user = user
    source_path = os.path.join(GIT_ROOT, user, repository)
    target_path = os.path.join(GIT_ROOT, new_user, new_repository)
    if not __git_exists(source_path):
        # if source not exists
        #debug here
        sys.exit(EXIT.API_GIT_NOT_EXISTS)
    if __git_exists(target_path):
        #if target path exists
        sys.exit(EXIT.API_GIT_ALREADY_EXISTS)
    try:
        shutil.copytree(source_path, target_path)
    except IOError:
        #debug here
        sys.exit(EXIT.API_GIT_COPY_ERROR)

# move project, api helper
#   @public
def git_move(user, repository, new_repository, new_user = None):
    if new_user is None:
        new_user = user
    source_path = os.path.join(GIT_ROOT, user, repository)
    target_path = os.path.join(GIT_ROOT, new_user, new_repository)
    if not __git_exists(source_path):
        # debug here
        sys.exit(EXIT.API_GIT_NOT_EXISTS)
    if __git_exists(target_path):
        # debug here
        sys.exit(EXIT.API_GIT_ALREADY_EXISTS)
    try:
        shutil.move(source_path, target_path)
    except shutil.Error:
        #debug target exists
        sys.exit(EXIT.API_GIT_ALREADY_EXISTS)
    except IOError:
        #debug souce path not exists
        sys.exit(EXIT.API_GIT_NOT_EXISTS)

# delete the project if the exists
#   @public
def git_delete(user, repository):
    full_path = os.path.join(GIT_ROOT, user, repository)
    if __git_exists(full_path):
        shutil.rmtree(full_path)
    else:
        sys.exit(EXIT.API_GIT_NOT_EXISTS)

# Check the project exists
#   @public
def git_exists(user, repository):
    full_path = os.path.join(GIT_ROOT, user, repository)
    if __git_exists(full_path):
       sys.exit(EXIT.API_GIT_ALREADY_EXISTS)
    else:
       sys.exit(EXIT.API_GIT_NOT_EXISTS)

# helper for git_exists
#   @private
def __git_exists(full_path):
    return os.path.isdir(full_path)
