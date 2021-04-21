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


class WEBKITBROWSER_bridgeevent:
    method = ".1.bridgeevent"
    __doc__ = "Send legacy $badger event"

    def __init__(self, app = "WebKitBrowser"):
        self.__app = app
        self.params = {}

    def set(self, app = "WebKitBrowser"):
        self.__app = app
        self.params = {}
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.__app + self.method}
        return ws.send(jsonobj, *args, **kwargs)


class WEBKITBROWSER_bridgereply:
    method = ".1.bridgereply"
    __doc__ = "A response for legacy $badger"

    def __init__(self, app = "WebKitBrowser"):
        self.__app = app
        self.params = {}

    def set(self, app = "WebKitBrowser"):
        self.__app = app
        self.params = {}
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.__app + self.method}
        return ws.send(jsonobj, *args, **kwargs)


class WEBKITBROWSER_localstorageenabled:
    method = ".1.localstorageenabled"
    __doc__ = "Controls the local storage availability"

    def __init__(self, app = "WebKitBrowser"):
        self.__app = app
        self.params = {}

    def set(self, app = "WebKitBrowser"):
        self.__app = app
        self.params = {}
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.__app + self.method}
        return ws.send(jsonobj, *args, **kwargs)


class WEBKITBROWSER_useragent:
    method = ".1.useragent"
    __doc__ = "UserAgent string used by browser"

    def __init__(self, app = "WebKitBrowser"):
        self.__app = app
        self.params = {}

    def set(self, app = "WebKitBrowser"):
        self.__app = app
        self.params = {}
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.__app + self.method}
        return ws.send(jsonobj, *args, **kwargs)


class WEBKITBROWSER_headers:
    method = ".1.headers"
    __doc__ = "Headers to send on all requests that the browser makes"

    def __init__(self, app = "WebKitBrowser"):
        self.__app = app
        self.params = {}

    def set(self, app = "WebKitBrowser"):
        self.__app = app
        self.params = {}
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.__app + self.method}
        return ws.send(jsonobj, *args, **kwargs)


class WEBKITBROWSER_httpcookieacceptpolicy:
    method = ".1.httpcookieacceptpolicy"
    __doc__ = "HTTP cookies accept policy"

    def __init__(self, app = "WebKitBrowser"):
        self.__app = app
        self.params = {}

    def set(self, app = "WebKitBrowser"):
        self.__app = app
        self.params = {}
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.__app + self.method}
        return ws.send(jsonobj, *args, **kwargs)


class WEBKITBROWSER_languages:
    method = ".1.languages"
    __doc__ = "User preferred languages"

    def __init__(self, app = "WebKitBrowser"):
        self.__app = app
        self.params = {}

    def set(self, app = "WebKitBrowser"):
        self.__app = app
        self.params = {}
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.__app + self.method}
        return ws.send(jsonobj, *args, **kwargs)
