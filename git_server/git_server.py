# coding: utf-8

import os, sys, errno, logging

import optparse

# Import database layout
from db_base import *

from git_repository import git_commit


logging.basicConfig(filename = '/var/log/git/git.log', level = logging.INFO)

ALLOW_RE = re.compile("^'/*(?P<path>[a-zA-Z0-9][a-zA-Z0-9@._-]*(/[a-zA-Z0-9][a-zA-Z0-9@._-]*)*)'$")

ERROR_TIP = "Server is busy."

CURRENT_USER = {}

# have readonly access
COMMANDS_READONLY = [
    'git-upload-pack',
    'git upload-pack',
    ]

# have write access
COMMANDS_WRITE = [
    'git-receive-pack',
    'git receive-pack',
    ]

# return command ssh_id for sshes tbale.
def parser_ssh_id_from_command():
    c_handle = optparse.OptionParser()
    (options, args) = c_handle.parse_args()
    if not len(args):
        logging.error("git-server params error, Please check the auth key file.")
        sys.exit(1)
    return int(args.pop(0))

# return user info from {users} table.
#     used parser_ssh_id_from_command()
def current_user():
    global CURRENT_USER
    
    if CURRENT_USER:
        return CURRENT_USER

    ssh_id  = parser_ssh_id_from_command()

    results = db_query("SELECT user.* FROM master_users AS user LEFT JOIN master_sshes AS ssh ON ssh.uid = user.id WHERE ssh.id = %d limit 1", ssh_id)

    user = db_fetch_hash(results)

    if user is None:
        logging.error("Can't find current user with ssh_id '%s', exit!", ssh_id)
        sys.exit(1)

    CURRENT_USER = user

    return CURRENT_USER

def handle_ssh_args():
    cmd = os.environ.get('SSH_ORIGINAL_COMMAND', None)
    if cmd is None:
        logging.error("Must access this with ssh, because SSH_ORIGINAL_COMMAND is None!")
        sys.exit(1)

    if '\n' in cmd:
        logging.error("Command may not contain newline. :'%s'" % cmd)
        sys.exit(1)

    command, args = cmd.split(None, 1)

    # if command like "git upload-pack path_to_project.git"
    if command is 'git':
        try:
            sub_command, args= args.split(None, 1)
        except ValueError:
            logging.error("Invalid ssh command: %s" % cmd)
            sys.exit(1)
        command = "%s %s" % (command, sub_command)

    if command not in COMMANDS_WRITE and command not in COMMANDS_READONLY:
        logging.error("Command '%s' is invalid!" % cmd)
        sys.exit(1)

    match = ALLOW_RE.match(args)

    if match is None:
        logging.error("Command args '%s' is invalid! unsafe." % args)
        sys.exit(1)

    path = match.group('path')

    if path is None:
        logging.error("Git path is None, exit!")
        sys.exit(1)
    # get current user info
    user = current_user()

    try:
        user_path, repository = standard_git_path(user, path)
    except ValueError:
       logging.error("git path not standard. exit")
       sys.exit(1)

    full_path = git_commit(user_path, repository)

    final_cmd = "%(command)s '%(path)s'" % dict(
        command=command,
        path=full_path
        )

    logging.debug("Commiting....%s" % final_cmd)

    os.execvp('git', ['git', 'shell', '-c', final_cmd])
    
    logging.error('"%s" Program execution failed.' % final_cmd)


def standard_git_path(user, path):
    try:
        _user, repository = path.split('/')
    except ValueError:
        logging.error("git path error. Can't split with '/'" % path)
        sys.exit(1)
    if _user == user.get('login', None) and repository.endswith(".git"):
        repository_name = repository[:-4]
        res = db_query("SELECT id FROM {projects} WHERE uid = %d AND name='%s'", user.get('id', None), repository_name)
        if not db_affected_rows(res):
            logging.error("Project '%s' not found with user '%s'." % (repository, _user))
            sys.exit(1)
        return (_user, repository)
    return False 

def bootstrap():
    # change to git user's home dir
    os.chdir(os.path.expanduser('~'))
    db_connect()
    #current_user()
    handle_ssh_args()




#    print 'git-server here@ ok.'
#    s = os.environ.get('SSH_ORIGINAL_COMMAND', None)
#    os.system("echo s > ~/a")

