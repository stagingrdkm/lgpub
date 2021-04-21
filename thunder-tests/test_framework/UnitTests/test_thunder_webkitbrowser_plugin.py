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


import json
import unittest
import os
import copy
import time
import sys

from Libraries.Cpe.ThunderWSAPI import ThunderWSAPI
from Libraries.Common.JsonReader import *

class TestThunderWebKitBrowserWSAPI(unittest.TestCase):

    def setUp(self):
        self.__cpe_ip = sys.argv[1]
        self.__thunder_handler = ThunderWSAPI()
        self.__thunder_handler.open_ws_connection(self.__cpe_ip + ":9998/jsonrpc")


    def tearDown(self):
        self.__thunder_handler.close_ws_connection()


    def verify_webkit_plugin(self, plugin):
        self.__thunder_handler.controller_activate_plugin(plugin)

        with self.subTest(msg="Fail while checking: "+plugin+" plugin"):
            msg_prefix="Method: "+plugin+"_bridgeevent"
            result = self.__thunder_handler.webkitbrowser_bridgeevent(plugin)
            self.assertFalse("error" in result, msg_prefix +" return error")

        with self.subTest(msg="Fail while checking: "+plugin+" plugin"):
            msg_prefix="Method: "+plugin+"_bridgereply"
            result = self.__thunder_handler.webkitbrowser_bridgereply(plugin)
            self.assertFalse("error" in result, msg_prefix +" return error")


        with self.subTest(msg="Fail while checking: "+plugin+" plugin"):
            msg_prefix="Method: "+plugin+"_localstorageenabled"
            result = self.__thunder_handler.webkitbrowser_localstorageenabled(plugin)
            self.assertFalse("error" in result, msg_prefix +" return error")


        with self.subTest(msg="Fail while checking: "+plugin+" plugin"):
            msg_prefix="Method: "+plugin+"_useragent"
            result = self.__thunder_handler.webkitbrowser_useragent(plugin)
            self.assertFalse("error" in result, msg_prefix +" return error")

        with self.subTest(msg="Fail while checking: "+plugin+" plugin"):
            msg_prefix="Method: "+plugin+"_headers"
            result = self.__thunder_handler.webkitbrowser_headers(plugin)
            self.assertFalse("error" in result, msg_prefix +" return error")

        with self.subTest(msg="Fail while checking: "+plugin+" plugin"):
            msg_prefix="Method: "+plugin+"_httpcookieacceptpolicy"
            result = self.__thunder_handler.webkitbrowser_httpcookieacceptpolicy(plugin)
            self.assertFalse("error" in result, msg_prefix +" return error")

        with self.subTest(msg="Fail while checking: "+plugin+" plugin"):
            msg_prefix="Method: "+plugin+"_languages"
            result = self.__thunder_handler.webkitbrowser_languages(plugin)
            self.assertFalse("error" in result, msg_prefix +" return error")

        self.__thunder_handler.controller_deactivate_plugin(plugin)


    def test_L1_verify_webkitbrowser_plugins(self):
        for plugin in ["WebKitBrowser","HtmlApp","LightningApp","ResidentApp","SearchAndDiscoveryApp"]:
            self.verify_webkit_plugin(plugin)
