#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2017 frafall
# SPDX-FileCopyrightText: 2022 rimeno <rafaneto@punktona.org>

import xbmc
import xbmcaddon
import xbmcgui

from resources.lib.systemd import Systemctl
from resources.lib.snapcontrol import SnapControl

addon = xbmcaddon.Addon()

notifIcon = addon.getAddonInfo("path") + "/resources/icon.png"


def log(message):
    xbmc.log(f'[{addon.getAddonInfo("id")}] {message}', level=xbmc.LOGINFO)


class Monitor(xbmc.Monitor):
    def __init__(self, player):
        super().__init__(self)
        self.player = player

    def onSettingsChanged(self):
        log("event onSettingsChanged!")


class Player(xbmc.Player):
    def __init__(self):
        super().__init__(self)
        self.service = Systemctl("snapclient")

    def start(self):
        if not self.service.isActive():
            self.service.start()
            control = SnapControl()
            if control.client and control.sync:
                control.syncVol("K2S")
            xbmcgui.Dialog().notification(
                "Snapcast", addon.getLocalizedString(34011), notifIcon, 5000, False
            )

    def stop(self):
        if self.service.isActive():
            self.service.stop()
            xbmcgui.Dialog().notification(
                "Snapcast", addon.getLocalizedString(34012), notifIcon, 5000, False
            )

    def onStartup(self):
        log("event onStartup!")
        if addon.getSetting("StartupAutoStart") == "true":
            self.start()
        else:
            log("not started due to settings")

    def onShutdown(self):
        log("event onShutdown!")
        self.stop()

    def onPlayBackStarted(self):
        log("event onPlayBackStarted!")
        self.stop()

    def onPlayBackStopped(self):
        log("event onPlayBackStopped!")
        if addon.getSetting("AutoStart") == "true":
            self.start()
        else:
            log("not started tue to settings")

    def onPlayBackPaused(self):
        log("event onPlayBackPaused!")

    def onPlayBackResumed(self):
        log("event onPlayBackResumed!")


if __name__ == "__main__":
    log("Initializing snapcast addon!")
    player = Player()
    Monitor(player).waitForAbort()


# VIM MODLINE
# vim: set ai shiftwidth=4 tabstop=4 expandtab:
