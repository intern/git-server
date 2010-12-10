# coding: utf-8
"""
  git-server setuptools
"""
import os, sys

from setuptools import setup,find_packages

# copy the git server config. et: db conf.
def install_config():
    cp = r"cp -f git-server/git-server.conf /etc/git.conf"
    if os.system(cp) > 0:
        print """
Please use:
> sudo python setup.py install
"""
        sys.exit()

install_config()

setup(
    name = "git server",
    version = '0.1.0',
    packages = find_packages(),
    description = "This is a version manage tool with git, It like SVN!",
    long_description = "this is long description with the git-server.",
    #install_requires = ['docutils>=0.3'],
    include_package_data = True,
    author = "LAN_CHI",
    author_email = "lan_chi@foxmail.com",
    scripts = ['git-server/git-init.py', 'git-server/git-server.py', 'git-server/authorized_keys_hook.py']
)

