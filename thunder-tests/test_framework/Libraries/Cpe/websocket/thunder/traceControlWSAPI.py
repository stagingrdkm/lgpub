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


class TRACECONTROL_status:
    method = "TraceControl.1.status"
    __doc__ = "Retrieves general information"

    def __init__(self, category, module):
        self.params = {}
        self.params["module"] = module
        self.params["category"] = category

    def set(self, category, module):
        self.params = {}
        self.params["module"] = module
        self.params["category"] = category
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method, "params": self.params}
        return ws.send(jsonobj, *args, **kwargs)


class TRACECONTROL_set:
    method = "TraceControl.1.set"
    __doc__ = "Sets traces"

    def __init__(self, category, state, module):
        self.params = {}
        self.params["module"] = module
        self.params["category"] = category
        self.params["state"] = state

    def set(self, category, state, module):
        self.params = {}
        self.params["module"] = module
        self.params["category"] = category
        self.params["state"] = state
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method, "params": self.params}
        return ws.send(jsonobj, *args, **kwargs)
