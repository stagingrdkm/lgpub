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


class PACKAGER_install:
    method = "Packager.1.install"
    __doc__ = "Installs a package given by a name, an URL or a file path"

    def __init__(self, pkgId, ptype, url):
        self.params = {}
        self.params["pkgId"] = pkgId
        self.params["type"] = ptype
        self.params["url"] = url

    def set(self, pkgId, ptype, url):
        self.params = {}
        self.params["pkgId"] = pkgId
        self.params["type"] = ptype
        self.params["url"] = url
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method, "params": self.params}
        return ws.send(jsonobj, *args, **kwargs)


class PACKAGER_synchronize:
    method = "Packager.1.synchronize"
    __doc__ = "Synchronizes repository manifest with a repository"

    def __init__(self):
        self.params = {}

    def set(self):
        self.params = {}
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method}
        return ws.send(jsonobj, *args, **kwargs)



class PACKAGER_getInstalled:
    method = "Packager.1.getInstalled"
    __doc__ = "Get list of installed packages"

    def __init__(self):
        self.params = {}

    def set(self):
        self.params = {}
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method}
        return ws.send(jsonobj, *args, **kwargs)

class PACKAGER_isInstalled:
    method = "Packager.1.isInstalled"
    __doc__ = "Check if package is installed"

    def __init__(self, pkgId):
        self.params = {}
        self.params["pkgId"] = pkgId

    def set(self, pkgId):
        self.params = {}
        self.params["pkgId"] = pkgId
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method, "params": self.params}
        return ws.send(jsonobj, *args, **kwargs)

class PACKAGER_getPackageInfo:
    method = "Packager.1.getPackageInfo"
    __doc__ = "Get info about installed package"

    def __init__(self, pkgId):
        self.params = {}
        self.params["pkgId"] = pkgId

    def set(self, pkgId):
        self.params = {}
        self.params["pkgId"] = pkgId
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method, "params": self.params}
        return ws.send(jsonobj, *args, **kwargs)


class PACKAGER_remove:
    method = "Packager.1.remove"
    __doc__ = "Remove installed package"

    def __init__(self, pkgId):
        self.params = {}
        self.params["pkgId"] = pkgId

    def set(self, pkgId):
        self.params = {}
        self.params["pkgId"] = pkgId
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method, "params": self.params}
        return ws.send(jsonobj, *args, **kwargs)


class PACKAGER_getAvailableSpace:
    method = "Packager.1.getAvailableSpace"
    __doc__ = "Get available space"

    def __init__(self):
        self.params = {}

    def set(self):
        self.params = {}
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method}
        return ws.send(jsonobj, *args, **kwargs)

