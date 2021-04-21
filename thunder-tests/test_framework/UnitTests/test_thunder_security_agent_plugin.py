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

class TestThunderSecurityAgentWSAPI(unittest.TestCase):

    def setUp(self):
        self.__cpe_ip = sys.argv[1]
        self.__thunder_handler = ThunderWSAPI()
        self.__thunder_handler.open_ws_connection(self.__cpe_ip + ":9998/jsonrpc")


    def tearDown(self):
        self.__thunder_handler.close_ws_connection()


    def test_H1_verify_securityagent_plugin(self):
        # this method is avaliable only when "SECURITY_TESTING_MODE" is defined in the code
        '''
        msg_prefix="Method: securityagent_createtoken"
        url = "https://test.comcast.com"
        user = "Test"
        hash = "1CLYex47SY"
        result = self.__thunder_handler.securityagent_createtoken(url, hash, user)
        self.assertFalse("error" in result, msg_prefix +" return error")
        self.assertTrue("token" in result['result'], msg_prefix +" didn't return key \"token\"")
        token = result['result']['token']
        '''
        msg_prefix="Method: securityagent_validate"
        result = self.__thunder_handler.securityagent_validate("some_random_token")
        self.assertFalse("error" in result, msg_prefix +" return error")
        self.assertTrue("valid" in result['result'], msg_prefix +" didn't return key \"valid\"")
        self.assertFalse(result['result']['valid'], msg_prefix +" token valid = " + str(result['result']['valid']))
