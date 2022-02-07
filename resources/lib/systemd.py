#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022 rimeno <rafaneto@punktona.org>

import xbmc
import subprocess
import xbmcaddon


class Systemctl():

    def __init__(self, service, system=False):
        self.service = service
        if system:
            self.user = ''
        else:
            self.user = '--user'
        self.addon = xbmcaddon.Addon()

    def _log(self, message):
        xbmc.log("[{}] systemd: {} {} : {}".format(
            self.addon.getAddonInfo('id'), self.service, self.user, message),
                 level=xbmc.LOGINFO)

    def start(self):
        ret = subprocess.run(['systemctl', "start", self.user, self.service])
        if ret.returncode == 0:
            self._log("started")
            return True
        else:
            self._log("failed to start")
            return False

    def stop(self):
        ret = subprocess.run(['systemctl', "stop", self.user, self.service])
        if ret.returncode == 0:
            self._log("stopped")
            return True
        else:
            self._log("failed to stop")
            return False

    def isActive(self):
        ret = subprocess.run(['systemctl', self.user, "is-active",
                              self.service], stdout=subprocess.DEVNULL)
        if ret.returncode != 0:
            return False
        else:
            return True

# VIM MODLINE
# vim: set ai shiftwidth=4 tabstop=4 expandtab:
