#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# antergos-bot.py
#
# Copyright © 2018 Antergos
#
# antergos-alerts.py is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# antergos-alerts.py is distributed in the hope that it will be useful,
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
# along with antergos-alerts.py; if not, see <http://www.gnu.org/licenses/>.

import os

import log
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


def setup_logging():
    """ Configure our logger """
    logger = logging.getLogger()

    logger.handlers = []

    log_level = logging.DEBUG
    #log_level = logging.INFO

    logger.setLevel(log_level)

    #context_filter = ContextFilter()
    #logger.addFilter(context_filter.filter)

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


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.

def start(_bot, update):
    """ Send a message when the command /start is issued. """
    update.message.reply_text('Hi!')


def help(_bot, update):
    """ Send a message when the command /help is issued. """
    update.message.reply_text('Help!')


#def echo(bot, update):
#    """Echo the user message."""
#    update.message.reply_text(update.message.text)


def error(bot, update, error_msg):
    """ Log Errors caused by Updates. """
    logging.warning('Update "%s" caused error "%s"', update, error_msg)


def show_alert(bot, _update, args):
    """ Shows alert to the channel @antergos_alerts """
    if not args or len(args) < 4:
        message = "Error! Bad number of parameters!"
    else:
        #subject = args[0]
        #part1 = args[1]
        #part2 = args[2]
        #part3 = args[3]
        message = "\n".join(args)
    bot.sendMessage(chat_id='@antergos_alerts', text=message)


def alarm(bot, job):
    """Send the alarm message."""
    bot.send_message(job.context, text='Beep!')


def main():
    """ Starts the Bot """
    try:
        setup_logging()

        # Create the EventHandler and pass it your bot's token.
        updater = Updater(token=os.environ['ANTERGOS_BOT_TOKEN'])

        # Get the dispatcher to register handlers
        dispatcher = updater.dispatcher

        # on different commands - answer in Telegram
        dispatcher.add_handler(CommandHandler('start', start))
        dispatcher.add_handler(CommandHandler('help', help))
        dispatcher.add_handler(CommandHandler('show', show_alert, pass_args=True))

        # Add job to queue
        job = job_queue.run_once(alarm, due, context='@antergos_alerts')
        chat_data['job'] = job

        updater.start_polling()
    except KeyError as err:
        logging.error(err)
    except telegram.error.Unauthorized as err:
        logging.error(err)

main()
