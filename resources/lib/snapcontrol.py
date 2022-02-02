#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022 rimeno <rafaneto@punktona.org>

import asyncio
import re
import uuid
import json
import xbmc
import xbmcaddon

import snapcast.control


class SnapControl():

    def __init__(self):
        self.addon = xbmcaddon.Addon()
        host = self.addon.getSetting("ServerAddress")
        xbmc.log("[{}] debug {}".format( self.addon.getAddonInfo('id'), host), level=xbmc.LOGINFO)

        if host is not None:
            mac = ":".join(re.findall("..", "%012x" % uuid.getnode()))
            self.loop = asyncio.new_event_loop()
            self.server = self.loop.run_until_complete(
                snapcast.control.create_server(self.loop, host))
            for client in self.server.clients:
                if client.identifier == mac:
                    self.client = client
                    if self.addon.getSetting("SyncVolume"):
                        self.sync = True
                    else:
                        self.sync = False
        else:
            self.client = False
            self.sync = False

    def get_or_create_eventloop(self):
        try:
            return asyncio.get_event_loop()
        except RuntimeError as ex:
            if "There is no current event loop in thread" in str(ex):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                return asyncio.get_eventloop()

    def getFriendlyName(self):
        return self.client.friendly_name

    def getVolume(self):
        return self.client.volume

    def setVolume(self, volume):
        return self.loop.run_until_complete(self.server.client_volume(
            self.client.identifier, {'percent': volume, 'muted': False}))

    def getKodiVol(self):
        req = {
            "jsonrpc": "2.0",
            "method": "Application.GetProperties",
            "params": {"properties": ["volume", "muted"]},
            "id": 1
        }
        res = xbmc.executeJSONRPC(json.dumps(req))
        jres = json.loads(res)
        return jres["result"]["volume"]

    def syncVol(self, direction):
        if direction == "K2S":
            snapcastVol = self.getVolume()
            kodiVol = self.getKodiVol()
            self.setVolume(kodiVol)
            xbmc.log("[{}] Set vol from {} to {}".format(
                self.addon.getAddonInfo('id'), snapcastVol, kodiVol),
                     level=xbmc.LOGINFO)

# VIM MODLINE
# vim: set ai shiftwidth=4 tabstop=4 expandtab:
