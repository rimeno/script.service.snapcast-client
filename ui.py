#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022 rimeno <rafaneto@punktona.org>

import xbmcaddon
import xbmcgui
import xbmc

from resources.lib.systemd import Systemctl
from resources.lib.snapcontrol import SnapControl

addon = xbmcaddon.Addon()

notifIcon = addon.getAddonInfo('path') + "resources/icon.png"


def start():
    service = Systemctl("snapclient")
    player = xbmc.Player()
    control = SnapControl()
    player.stop()
    if not service.isActive():
        service.start()
        if control.client and control.sync:
            control.syncVol("K2S")
        xbmcgui.Dialog().notification('Snapcast',
                                      addon.getLocalizedString(34011),
                                      notifIcon, 5000, False)


def stop():
    service = Systemctl("snapclient")
    if service.isActive():
        service.stop()
        xbmcgui.Dialog().notification('Snapcast',
                                      addon.getLocalizedString(34012),
                                      notifIcon, 5000, False)


def isActive():
    return Systemctl("snapclient").isActive()



def menu():
    if isActive():
        control = SnapControl()
        if control.client and control.sync:
            control.syncVol("K2S")
        switcher = {
            0: stop,
            1: addon.openSettings,
        }
        items = [
            addon.getLocalizedString(30012),
            addon.getLocalizedString(30013),
        ]
    else:
        switcher = {
            0: start,
            1: addon.openSettings,
        }
        items = [
            addon.getLocalizedString(30011),
            addon.getLocalizedString(30013),
        ]
    action = xbmcgui.Dialog().select(addon.getLocalizedString(30001), items)
    func = switcher.get(action)
    if func:
        return func()


if __name__ == '__main__':
    menu()
