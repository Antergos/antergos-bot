#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# botlog.py
#
# Copyright © 2018 Antergos
#
# Antergos Bot is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Antergos Bot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# The following additional terms are in effect as per Section 7 of the license:
#
# The preservation of all legal notices and author attributions in
# the material or in the Appropriate Legal Notices displayed
# by works containing it is required.
#
# You should have received a copy of the GNU General Public License
# along with Antergos Bot; if not, see <http://www.gnu.org/licenses/>.

""" Configure logs for Antergos Bot """

import logging

def setup_logging():
    """ Configure our logger """
    logger = logging.getLogger()

    logger.handlers = []

    #log_level = logging.DEBUG
    log_level = logging.INFO

    logger.setLevel(log_level)

    # Log format
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(filename)s(%(lineno)d) %(funcName)s(): %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S")

    # File logger
    try:
        file_handler = logging.FileHandler('/tmp/antergos-bot.log', mode='w')
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except PermissionError as permission_error:
        print("Can't open /tmp/antergos-bot.log : ", permission_error)

    # Stdout logger
    # Show log messages to stdout
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
