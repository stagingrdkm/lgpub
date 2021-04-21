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

class TestThunderOcdmWSAPI(unittest.TestCase):

    def setUp(self):
        self.__cpe_ip = sys.argv[1]
        self.__thunder_handler = ThunderWSAPI()
        self.__thunder_handler.open_ws_connection(self.__cpe_ip + ":9998/jsonrpc")
        self.__thunder_handler.controller_activate_plugin("OCDM")


    def tearDown(self):
        self.__thunder_handler.controller_deactivate_plugin("OCDM")
        self.__thunder_handler.close_ws_connection()


    def test_D1_verify_ocdm_plugin(self):
        key_systems = None
        with self.subTest(msg="Fail while checking: OCDM plugin"):
            msg_prefix="Method: ocdm_drms"
            result = self.__thunder_handler.ocdm_drms()
            self.assertFalse("error" in result, msg_prefix +" return error")
            self.assertEqual(len(result['result']), 2, "Expected 2 key_systems, reviced: " + str(len(result['result'])))
            key_systems = copy.deepcopy(result['result'])

        with self.subTest(msg="Fail while checking: OCDM plugin"):
            msg_prefix="Method: ocdm_keysystems"
            for key_system in key_systems:
                result = self.__thunder_handler.ocdm_keysystems(key_system['name'])
                self.assertFalse("error" in result, msg_prefix +" return error")
                self.assertNotEqual(len(result['result']), 0, "Expected non 0 keys, reviced: " + str(len(result['result'])))


