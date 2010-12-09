# coding: utf-8
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

def initialization_db_sql():
    return u"""
SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
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

--
-- 表的结构 `users`
--
CREATE TABLE IF NOT EXISTS `{users}` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `updated_at` datetime NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;
    """

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



