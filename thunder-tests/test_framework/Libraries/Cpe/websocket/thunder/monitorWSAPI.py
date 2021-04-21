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


class MONITOR_restartlimits:
    method = "Monitor.1.restartlimits"
    __doc__ = "Sets new restart limits for a service"

    def __init__(self, callsign, restart):
        self.params = {}
        self.params["callsign"] = callsign
        self.params["restart"] = restart

    def set(self, callsign, restart):
        self.params = {}
        self.params["callsign"] = callsign
        self.params["restart"] = restart
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method, "params": self.params}
        return ws.send(jsonobj, *args, **kwargs)


class MONITOR_resetstats:
    method = "Monitor.1.resetstats"
    __doc__ = "Resets memory and process statistics for a single service watched by the Monitor"

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


class MONITOR_status:
    method = "Monitor.1.status"
    __doc__ = "Service statistics"

    def __init__(self):
        self.params = {}

    def set(self):
        self.params = {}
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method}
        return ws.send(jsonobj, *args, **kwargs)
