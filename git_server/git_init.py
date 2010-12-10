# coding: utf-8
# To change this template, choose Tools | Templates
# and open the template in the editor.

import os, sys, ConfigParser, errno

from db_base import *

COMMANDS_READONLY = [
    'git-upload-pack',
    'git upload-pack',
    ]

COMMANDS_WRITE = [
    'git-receive-pack',
    'git receive-pack',
    ]

# the Mysql Tables structure, its require
def initialization_db_sql():
    return (u"""
SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
    """,
    u"""
--
-- 表的结构 `projects`
--
CREATE TABLE IF NOT EXISTS `{projects}` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `location` varchar(255) DEFAULT NULL,
  `description` text,
  `updated_at` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;
    """,
    u"""
--
-- 表的结构 `sshes`
--

CREATE TABLE IF NOT EXISTS `{sshes}` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `ssh_key` text NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;
    """,
    u"""
--
-- 表的结构 `users`
--
CREATE TABLE IF NOT EXISTS `{users}` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `updated_at` datetime NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `index_users_on_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;
    """)

# To read the initialization admin's ssh public key. configure the git server must.
#     usage:
#         sudo -H -u git git-init < /tmp/id_rsa.pub
#
def read_init_public_key():
    fp = sys.stdin
    return str(fp.readline()).strip()

def admin_config():
    conf = get_db_config_file()
    return conf.get('ADMIN', 'email')

# bootstrap to init tables struct and admin data.
def bootstrap():
    db_connect()
    for sql in initialization_db_sql():
        db_query(sql)

    db_query("INSERT INTO `{users}`(`email`, `created_at`, `updated_at`) VALUES('%s', NOW(), NOW())", admin_config())

    db_query("INSERT INTO `{sshes}`(`uid`, `title`, `ssh_key`, `created_at`, `updated_at`) VALUES(%d, '%s', '%s', NOW(), NOW())", db_last_insert_id(), 'lan_chi@foxmail.com', read_init_public_key())

    # commit transaction
    db_commit()

    #sys.exit()
