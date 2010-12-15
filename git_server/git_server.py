# coding: utf-8

import os, sys, errno, logging

import optparse

# Import database layout
from db_base import *

from git_repository import commit_repository


logging.basicConfig(filename = '/var/log/git/git.log', level = logging.INFO)

ALLOW_RE = re.compile("^'/*(?P<path>[a-zA-Z0-9][a-zA-Z0-9@._-]*(/[a-zA-Z0-9][a-zA-Z0-9@._-]*)*)'$")

ERROR_TIP = "Server is busy."

CURRENT_USER = {}

COMMANDS_READONLY = [
    'git-upload-pack',
    'git upload-pack',
    ]

COMMANDS_WRITE = [
    'git-receive-pack',
    'git receive-pack',
    ]

# return command ssh_id for sshes tbale.
def parser_ssh_id_from_command():
    c_handle = optparse.OptionParser()
    (options, args) = c_handle.parse_args()
    if not len(args):
        logging.error("git-server params error, Is't ssh_id number, it is None")
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
        logging.error("Must run this with ssh, becase SSH_ORIGINAL_COMMAND is None.")
        sys.exit(1)
    logging.info("Runing command: %(cmd)r", dict(cmd = cmd))
    if '\n' in cmd:
        logging.error("Error: Command may not contain newline: '%s'" % cmd)
        sys.exit(1)
    command, args = cmd.split(None, 1)

    # if command like "git upload-pack path_to_project.git"
    if command is 'git':
        try:
            sub_command, args= args.split(None, 1)
        except ValueError:
            sys.exit(1)
        command = "%s %s" % (command, sub_command)
    if command not in COMMANDS_WRITE and command not in COMMANDS_READONLY:
        logging.error("Error: Command '%s' is invalid!" % cmd)
        sys.exit(1)
    match = ALLOW_RE.match(args)
    if match is None:
        logging.error("Error: Command args '%s' is invalid! unsafe." % args)
        sys.exit(1)
    path = match.group('path')

    logging.info("path=>%s; args=> %s" % (path,args))

    if path is None:
        logging.error("path is None. exit")
        sys.exit(1)
    user = current_user()

    repor_path = standard_git_path(user, path)
    
    if repor_path is False:
       logging.error("git path not standard. exit")
       sys.exit(1)

    full_path = commit_repository(path)
    final_cmd = "%(command)s '%(path)s'" % dict(
        command=command,
        path=full_path
        )
    logging.info("Commiting....%s" % final_cmd)
    os.execvp('git', ['git', 'shell', '-c', final_cmd])
    
    logging.info("ERROR.")


def standard_git_path(user, path):
    try:
        sub_path, repository = path.split('/')
    except ValueError:
        logging.error("git...(%s)r" % path)
        sys.exit(1)
    logging.error("user: %s: path :%s git: %s" % (user.get("login", "None"), sub_path, str(repository.endswith(".git"))))
    if sub_path == user.get('login', None) and repository.endswith(".git"):
        repository_name = repository[:-4]
        res = db_query("SELECT id FROM {projects} WHERE uid = %d AND name='%s'", user.get('id', None), repository_name)
        if not db_affected_rows(res):
            logging.error("Project not find.")
            sys.exit(1)
        return '/'.join([sub_path, repository])
    return False    

def bootstrap():
#    os.system("echo %s >> /tmp/git_dev.log" % parser_command_ssh_id())

    # change to git user's home dir
    os.chdir(os.path.expanduser('~'))
    db_connect()
    current_user()
    handle_ssh_args()




#    print 'git-server here@ ok.'
#    s = os.environ.get('SSH_ORIGINAL_COMMAND', None)
#    os.system("echo s > ~/a")

