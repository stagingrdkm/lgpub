'''
    * If not stated otherwise in this file or this component's LICENSE file the
    * following copyright and licenses apply:
    *
    * Copyright 2021 Liberty Global Service B.V.
    *
    * Licensed under the Apache License, Version 2.0 (the "License");
    * you may not use this file except in compliance with the License.
    * You may obtain a copy of the License at
    *
    * http://www.apache.org/licenses/LICENSE-2.0
    *
    * Unless required by applicable law or agreed to in writing, software
    * distributed under the License is distributed on an "AS IS" BASIS,
    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    * See the License for the specific language governing permissions and
    * limitations under the License.
'''


import sys
import argparse


class FMP_create:
    method = "org.rdk.FireboltMediaPlayer.1.create"
    __doc__ = "Create player"

    def __init__(self, id):
        self.params = {}
        self.params["id"] = id

    def set(self, id):
        self.params = {}
        self.params["id"] = id
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method, "params": self.params}
        return ws.send(jsonobj, *args, **kwargs)


class FMP_load:
    method = "org.rdk.FireboltMediaPlayer.1.load"
    __doc__ = "Load content"

    def __init__(self, id, url, autoplay):
        self.params = {}
        self.params["id"] = id
        self.params["url"] = url
        self.params["autoplay"] = autoplay

    def set(self, id, url, autoplay):
        self.params = {}
        self.params["id"] = id
        self.params["url"] = url
        self.params["autoplay"] = autoplay
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method, "params": self.params}
        return ws.send(jsonobj, *args, **kwargs)


class FMP_seek:
    method = "org.rdk.FireboltMediaPlayer.1.seekTo"
    __doc__ = "Seek to position"

    def __init__(self, id, positionSec):
        self.params = {}
        self.params["id"] = id
        self.params["positionSec"] = positionSec

    def set(self, id, positionSec):
        self.params = {}
        self.params["id"] = id
        self.params["positionSec"] = positionSec
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method, "params": self.params}
        return ws.send(jsonobj, *args, **kwargs)


class FMP_play:
    method = "org.rdk.FireboltMediaPlayer.1.play"
    __doc__ = "Play"

    def __init__(self, id):
        self.params = {}
        self.params["id"] = id

    def set(self, id):
        self.params = {}
        self.params["id"] = id
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method, "params": self.params}
        return ws.send(jsonobj, *args, **kwargs)


class FMP_pause:
    method = "org.rdk.FireboltMediaPlayer.1.pause"
    __doc__ = "Pause"

    def __init__(self, id):
        self.params = {}
        self.params["id"] = id

    def set(self, id):
        self.params = {}
        self.params["id"] = id
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method, "params": self.params}
        return ws.send(jsonobj, *args, **kwargs)


class FMP_stop:
    method = "org.rdk.FireboltMediaPlayer.1.stop"
    __doc__ = "Stop"

    def __init__(self, id):
        self.params = {}
        self.params["id"] = id

    def set(self, id):
        self.params = {}
        self.params["id"] = id
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method, "params": self.params}
        return ws.send(jsonobj, *args, **kwargs)


class FMP_release:
    method = "org.rdk.FireboltMediaPlayer.1.release"
    __doc__ = "Release"

    def __init__(self, id):
        self.params = {}
        self.params["id"] = id

    def set(self, id):
        self.params = {}
        self.params["id"] = id
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method, "params": self.params}
        return ws.send(jsonobj, *args, **kwargs)


class FMP_register:
    method = "org.rdk.FireboltMediaPlayer.1.register"
    __doc__ = "Register events"

    def __init__(self, event, id):
        self.params = {}
        self.params["event"] = event
        self.params["id"] = id

    def set(self, event, id):
        self.params = {}
        self.params["event"] = event
        self.params["id"] = id
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method, "params": self.params}
        return ws.send(jsonobj, *args, **kwargs)

