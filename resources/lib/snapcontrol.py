#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022 rimeno <rafaneto@punktona.org>

import asyncio
import re
import uuid
import json
import socket
from ipaddress import ip_address, IPv4Address

import xbmc
import xbmcaddon

import snapcast.control


class SnapControl:
    """
    Manage Snapcast server and clients
    """

    def __init__(self):
        self.addon = xbmcaddon.Addon()
        server = self.addon.getSetting("ServerAddress")

        if server:
            if self.test_server(server):
                mac = ":".join(re.findall("..", "%012x" % uuid.getnode()))
                self.loop = asyncio.new_event_loop()
                self.server = self.loop.run_until_complete(
                    snapcast.control.create_server(self.loop, server)
                )
                for client in self.server.clients:
                    if client.identifier == mac:
                        self.client = client
                        if self.addon.getSetting("SyncVolume"):
                            self.sync = True
                        else:
                            self.sync = False
                        break
            else:
                self.client = False
                self.sync = False
        else:
            self.client = False
            self.sync = False

    def __del__(self):
        del self.loop

    def test_server(self, server):
        try:
            res = socket.getaddrinfo(server, 0, 0, 0, socket.IPPROTO_TCP)
        except Exception as error:
            xbmc.log(
                "[{}] The server {} cannot be joined : {}".format(
                    self.addon.getAddonInfo("id"), server, error
                ),
                level=xbmc.LOGERROR,
            )
            return False
        server_ok = False
        for r in res:
            if not server_ok:
                family, b, c, d, ip = r
                if type(ip_address(ip[0])) is IPv4Address:
                    inet = socket.AF_INET
                else:
                    inet = socket.AF_INET6
                a_socket = socket.socket(inet, socket.SOCK_STREAM)
                a_socket.settimeout(1)
                result_of_check = a_socket.connect_ex((ip[0], 1704))
                a_socket.close()
                if result_of_check == 0:
                    server_ok = True
            else:
                break
        if server_ok:
            return True
        xbmc.log(
            "[{}] The host {} cannot be joined".format(
                self.addon.getAddonInfo("id"), host
            ),
            level=xbmc.LOGERROR,
        )
        return False

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
        return self.loop.run_until_complete(
            self.server.client_volume(
                self.client.identifier, {"percent": volume, "muted": False}
            )
        )

    def setMute(self):
        return self.loop.run_until_complete(
            self.server.client_volume(self.client.identifier, {"muted": True})
        )

    def setUnMute(self):
        return self.loop.run_until_complete(
            self.server.client_volume(self.client.identifier, {"muted": False})
        )

    def getMuteStatus(self):
        xbmc.log(
            f"[{self.addon.getAddonInfo('id')}] mute status: {self.client.muted}",
            level=xbmc.LOGINFO,
        )
        return self.client.muted

    def getKodiVol(self):
        req = {
            "jsonrpc": "2.0",
            "method": "Application.GetProperties",
            "params": {"properties": ["volume", "muted"]},
            "id": 1,
        }
        res = xbmc.executeJSONRPC(json.dumps(req))
        jres = json.loads(res)
        return jres["result"]["volume"]

    def syncVol(self, direction):
        if direction == "K2S":
            snapcastVol = self.getVolume()
            kodiVol = self.getKodiVol()
            self.setVolume(kodiVol)
            xbmc.log(
                "[{}] Set vol from {} to {}".format(
                    self.addon.getAddonInfo("id"), snapcastVol, kodiVol
                ),
                level=xbmc.LOGINFO,
            )


# VIM MODLINE
# vim: set ai shiftwidth=4 tabstop=4 expandtab:
