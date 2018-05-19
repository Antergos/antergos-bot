#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# antergos-bot.py
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

from datetime import timedelta
import logging
import os

from telegram.ext import Updater, CommandHandler
#from telegram.ext import MessageHandler, Filters

import botlog
import alerts

class AntergosBot(object):
    """ Antergos Telegram Bot """

    def __init__(self):
        """ Starts the Bot """
        try:
            botlog.setup_logging()

            self.alerts = alerts.AntergosAlerts()

            # Create the EventHandler and pass it your bot's token.
            self.updater = Updater(token=os.environ['ANTERGOS_BOT_TOKEN'])

            # Get the dispatcher to register handlers
            dispatcher = self.updater.dispatcher

            # on different commands - answer in Telegram
            handler = CommandHandler('start', self.start)
            dispatcher.add_handler(handler)
            handler = CommandHandler('show', self.show_alerts)
            dispatcher.add_handler(handler)
            handler = CommandHandler('help', self.help)
            dispatcher.add_handler(handler)

            # Add job to queue
            job_queue = self.updater.job_queue
            job_queue.run_repeating(self.show_alerts_job, timedelta(minutes=60))
        except KeyError as err:
            logging.error(err)
        except telegram.error.Unauthorized as err:
            logging.error(err)

    def run(self):
        """ Starts bot """
        self.updater.start_polling()
        # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
        # SIGABRT. This should be used most of the time, since start_polling() is
        # non-blocking and will stop the bot gracefully.
        self.updater.idle()

    # Define a few command handlers. These usually take the two arguments bot and
    # update. Error handlers also receive the raised TelegramError object in error.

    @staticmethod
    def start(_bot, update):
        """ Send a message when the command /start is issued. """
        update.message.reply_text(
            'Hi! Please issue a /show command to see all pending alerts')

    @staticmethod
    def help(_bot, update):
        """ Send a message when the command /help is issued. """
        update.message.reply_text(
            'Issue a /show command to see all pending alerts')

    @staticmethod
    def error(_bot, update, error_msg):
        """ Log Errors caused by Updates. """
        logging.warning('Update "%s" caused error "%s"', update, error_msg)

    def show_alerts_job(self, bot, _job):
        """ Job that shows all pending alerts """
        self.show_alerts(bot)

    def show_alerts(self, bot, _update=None):
        """ Shows alert to the channel @antergos_alerts """
        pending_alerts = self.alerts.get_alerts()
        for (alert_id, alert_slug) in pending_alerts:
            message = self.alerts.get_alert_message(alert_id, alert_slug)
            bot.sendMessage(chat_id='@antergos_alerts', text=message)


if __name__ == "__main__":
    AntergosBot().run()
