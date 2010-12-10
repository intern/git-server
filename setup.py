# coding: utf-8
"""
  git-server setuptools
"""
import os, sys

from setuptools import setup,find_packages

# copy the git server config. et: db conf.
def install_config():
    cp = r"cp -f git_server/git-server.conf /etc/git.conf"
    if os.system(cp) > 0:
        print """
Please use:
> sudo python setup.py install
"""
        sys.exit()

install_config()

setup(
    name = "git-server",
    version = '0.1.0',
    packages = find_packages(),
    description = "This is a version manage tool with git, It like SVN!",
    long_description = """
Manage git repositories, provide access to them over SSH, with tight
access control and not needing shell accounts.

This is long description with the git-server.""",
    install_requires = ['setuptools>=0.6c5'],
    include_package_data = True,
    zip_safe = False,
    author = "LAN_CHI",
    author_email = "lan_chi@foxmail.com",
    entry_points = {
        'console_scripts': [
            'git-server = git_server.git_server:bootstrap',
            'git-init   = git_server.git_init:bootstrap',
            'run-auth-keys-hook = git_server.authorized_keys_hook:bootstrap'
            ]
        }
    #scripts = ['git-server/git-init.py', 'git-server/git-server.py', 'git-server/authorized_keys_hook.py']
)

