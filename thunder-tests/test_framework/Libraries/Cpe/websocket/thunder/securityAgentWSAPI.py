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


class SECURITYAGENT_createtoken:
    method = "SecurityAgent.1.createtoken"
    __doc__ = "Creates Token"

    def __init__(self, url, hash, user):
        self.params = {}
        self.params["url"] = url
        self.params["user"] = user


    def set(self, url, hash, user):
        self.params = {}
        self.params["url"] = url
        self.params["user"] = user
        self.params["hash"] = hash
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method, "params": self.params}
        return ws.send(jsonobj, *args, **kwargs)


class SECURITYAGENT_validate:
    method = "SecurityAgent.1.validate"
    __doc__ = "Validates Token"

    def __init__(self, token):
        self.params = {}
        self.params["token"] = token

    def set(self, token):
        self.params = {}
        self.params["token"] = token
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method, "params": self.params}
        return ws.send(jsonobj, *args, **kwargs)
