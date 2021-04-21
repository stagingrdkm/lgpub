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
dir_path = os.path.dirname(os.path.realpath(__file__))

from Libraries.Cpe.ThunderWSAPI import ThunderWSAPI
from Libraries.Common.JsonReader import *

class TestThunderTraceControlWSAPI(unittest.TestCase):

    def setUp(self):
        self.__cpe_ip = sys.argv[1]
        self.__thunder_handler = ThunderWSAPI()
        self.__thunder_handler.open_ws_connection(self.__cpe_ip + ":9998/jsonrpc")


    def tearDown(self):
        self.__thunder_handler.close_ws_connection()


    def test_I1_verify_tracecontrol_plugin(self):
        msg_prefix="Method: tracecontrol_set"
        module = "Plugin_DeviceInfo"
        category = "Information"
        state = "enabled"
        result = self.__thunder_handler.tracecontrol_set(module, category, state)
        self.assertFalse("error" in result, msg_prefix +" return error")

        result = self.__thunder_handler.tracecontrol_status(module, category)
        self.assertFalse("error" in result, msg_prefix +" return error")
