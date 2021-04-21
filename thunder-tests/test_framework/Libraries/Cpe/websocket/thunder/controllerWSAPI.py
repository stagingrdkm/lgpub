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


class CONTROLLER_storeconfig:
    method = "Controller.1.storeconfig"
    __doc__ = "Stores the configuration"

    def __init__(self):
        self.params = {}

    def set(self):
        self.params = {}
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method}
        return ws.send(jsonobj, *args, **kwargs)


class CONTROLLER_register:
    method = "Controller.1.register"
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

class CONTROLLER_unregister:
    method = "Controller.1.unregister"
    __doc__ = "Unregister events"

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


class CONTROLLER_deactivate:
    method = "Controller.1.deactivate"
    __doc__ = "Deactivates a plugin"

    def __init__(self, callsign):
        self.params = {}
        self.params["callsign"] = callsign

    def set(self, callsign):
        self.params = {}
        self.params["callsign"] = callsign
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method, "params": self.params}
        return ws.send(jsonobj, *args, **kwargs)


class CONTROLLER_startdiscovery:
    method = "Controller.1.startdiscovery"
    __doc__ = "Starts the network discovery"

    def __init__(self, ttl):
        self.params = {}
        self.params["ttl"] = ttl

    def set(self, ttl):
        self.params = {}
        self.params["ttl"] = ttl
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method, "params": self.params}
        return ws.send(jsonobj, *args, **kwargs)


class CONTROLLER_harakiri:
    method = "Controller.1.harakiri"
    __doc__ = "Reboots the device"

    def __init__(self):
        self.params = {}

    def set(self):
        self.params = {}
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method}
        return ws.send(jsonobj, *args, **kwargs)


class CONTROLLER_activate:
    method = "Controller.1.activate"
    __doc__ = "Activates a plugin"

    def __init__(self, callsign):
        self.params = {}
        self.params["callsign"] = callsign

    def set(self, callsign):
        self.params = {}
        self.params["callsign"] = callsign
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method, "params": self.params}
        return ws.send(jsonobj, *args, **kwargs)


class CONTROLLER_status:
    method = "Controller.1.status"
    __doc__ = "Get device status"

    def __init__(self):
        self.params = {}

    def set(self):
        self.params = {}
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method}
        return ws.send(jsonobj, *args, **kwargs)


class CONTROLLER_delete:
    method = "Controller.1.delete"
    __doc__ = "Removes contents of a directory from the persistent storage"

    def __init__(self, path):
        self.params = {}
        self.params["path"] = path

    def set(self, path):
        self.params = {}
        self.params["path"] = path
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method, "params": self.params}
        return ws.send(jsonobj, *args, **kwargs)
