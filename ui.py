#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022 rimeno <rafaneto@punktona.org>

import xbmcaddon
import xbmcgui
import xbmc

from resources.lib.snapcontrol import SnapControl

addon = xbmcaddon.Addon()

notifIcon = addon.getAddonInfo("path") + "resources/icon.png"


def start():
    player = xbmc.Player()
    snapcast = SnapControl()
    player.stop()
    if snapcast.getMuteStatus():
        snapcast.setUnMute()
        if snapcast.client and snapcast.sync:
            snapcast.syncVol("K2S")
        xbmcgui.Dialog().notification(
            "Snapcast", addon.getLocalizedString(34011), notifIcon, 5000, False
        )


def stop():
    snapcast = SnapControl()
    if not snapcast.getMuteStatus():
        snapcast.setMute()
        xbmcgui.Dialog().notification(
            "Snapcast", addon.getLocalizedString(34012), notifIcon, 5000, False
        )


def menu():
    snapcast = SnapControl()
    if not snapcast.getMuteStatus():
        if snapcast.client and snapcast.sync:
            snapcast.syncVol("K2S")
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


if __name__ == "__main__":
    menu()
