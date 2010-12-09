# coding: utf-8
"""
  git-server setuptools
"""
from setuptools import setup,find_packages

setup(
   name = "git server",
   version = '0.1.0',
   packages = find_packages(),
   description = "This is a version manage tool with git, It like SVN!",
   long_description = "this is long description with the git-server.",
   #install_requires = ['docutils>=0.3'],
   author = "LAN_CHI",
   author_email = "lan_chi@foxmail.com",
   scripts = ['git-init.py', 'git-server.py', 'authorized_keys_hook.py']
)
