#!/bin/python
# -*- coding: utf-8 -*-
#
# antergos-alerts.py
#
# Copyright © 2017-2018 Antergos
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

import json
import os
import subprocess


class AntergosAlerts(object):
    """ Manages antergos alerts """
    APP_NAME = 'ANTERGOS_NOTIFY'
    LOCALE_DIR = '/usr/share/locale'

    ALERTS_DIR = '/var/lib/antergos-alerts'
    ALERTS_JSON = '/var/lib/antergos-alerts/alerts.json'
    COMPLETED_JSON = '/var/lib/antergos-alerts/completed.json'

    def __init__(self):
        """ Initialization """
        try:
            with open(AntergosAlerts.ALERTS_JSON) as data:
                self.alerts = json.loads(data.read())
        except (OSError, json.JSONDecodeError):
            self.alerts = {}

        try:
            with open(AntergosAlerts.COMPLETED_JSON) as data:
                self.completed_alert_ids = json.loads(data.read())
        except (OSError, json.JSONDecodeError):
            self.completed_alert_ids = []

        self.alert_ids = self.alerts.keys()


    def get_alerts(self) -> None:
        """ Gets a list of all pending alerts in a form of tuple (id, slug) """
        # Filter out completed alerts
        alerts_ids = list(set(self.alert_ids) - set(self.completed_alert_ids))

        alerts_ids.sort()

        alerts_slugs = []

        for alert_id in alerts_ids:
            alert_slug = self.alerts[alert_id]
            alerts_slugs.append((alert_id, alert_slug))
            self.completed_alert_ids.append(alert_id)

        self._save_completed_alerts()

        return alerts_slugs

    @staticmethod
    def get_alert_message(alert_id, alert_slug):
        """ Returns alert message """
        subject = 'ATTENTION: Antergos System Message'
        part1 = 'A new Antergos Alert has been issued.'
        part2 = 'Alerts contain important information regarding your system.'
        part3 = 'You can view the alert at the following URL'

        message = "{0} - {1}\n\n{2}\n{3}\n{4}\n".format(alert_id, subject, part1, part2, part3)
        message += "https://antergos.com/wiki/alerts/{}".format(alert_slug)

        return message

    def _save_completed_alerts(self):
        """ Store already shown alerts """
        try:
            with open(AntergosAlerts.COMPLETED_JSON, 'w') as json_data:
                json_data.write(json.dumps(self.completed_alert_ids))
        except PermissionError as _err:
            print("root privileges are needed to store which alerts have already been shown")
