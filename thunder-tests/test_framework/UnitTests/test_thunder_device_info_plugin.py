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
dir_path = os.path.dirname(os.path.realpath(__file__))

from Libraries.Cpe.ThunderWSAPI import ThunderWSAPI
from Libraries.Common.JsonReader import *

class TestThunderDeviceInfoWSAPI(unittest.TestCase):

    def setUp(self):
        self.__cpe_ip = sys.argv[1]
        self.__thunder_handler = ThunderWSAPI()
        self.__thunder_handler.open_ws_connection(self.__cpe_ip + ":9998/jsonrpc")


    def tearDown(self):
        self.__thunder_handler.close_ws_connection()


    def test_B1_verify_device_info_plugin(self):
        with self.subTest(msg="Fail while checking: DeviceInfo plugin"):
            msg_prefix="Method: deviceinfo_systeminfo"
            result = self.__thunder_handler.deviceinfo_systeminfo()
            self.assertFalse("error" in result, msg_prefix +" return error")
            self.assertTrue("version" in result['result'], msg_prefix +" didn't return key \"version\"")
            self.assertTrue("uptime" in result['result'], msg_prefix +" didn't return key \"uptime\"")
            self.assertTrue("totalram" in result['result'], msg_prefix +" didn't return key \"totalram\"")
            self.assertTrue("freeram" in result['result'], msg_prefix +" didn't return key \"freeram\"")
            self.assertTrue("devicename" in result['result'], msg_prefix +" didn't return key \"devicename\"")
            self.assertTrue("cpuload" in result['result'], msg_prefix +" didn't return key \"cpuload\"")
            self.assertTrue("serialnumber" in result['result'], msg_prefix +" didn't return key \"serialnumber\"")
            self.assertTrue("time" in result['result'], msg_prefix +" didn't return key \"time\"")

        with self.subTest(msg="Fail while checking: DeviceInfo plugin"):
            msg_prefix="Method: deviceinfo_addresses"
            result = self.__thunder_handler.deviceinfo_addresses()
            self.assertFalse("error" in result, msg_prefix +" return error")
            self.assertEqual(len(result['result']), 3, "Expected 3 interfaces, reviced: " + str(len(result['result'])))
            for interface in result['result']:
                self.assertTrue("name" in interface, msg_prefix +" didn't return key \"name\"")
                self.assertTrue("mac" in interface, msg_prefix +" didn't return key \"mac\"")
                # "ip" is optional so we don't verify that key now

        with self.subTest(msg="Fail while checking: DeviceInfo plugin"):
            msg_prefix="Method: deviceinfo_socketinfo"
            result = self.__thunder_handler.deviceinfo_socketinfo()
            self.assertFalse("error" in result, msg_prefix +" return error")
            self.assertTrue("runs" in result['result'], msg_prefix +" didn't return key \"runs\"")
            # "total", "open", "link", "exception", "shutdown", are optional so we don't verify those keys now
