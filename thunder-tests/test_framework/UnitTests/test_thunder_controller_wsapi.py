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

class TestThunderControllerWSAPI(unittest.TestCase):

    def setUp(self):
        self.__cpe_ip = sys.argv[1]
        self.__plugins = json_file_reader(sys.argv[2])
        self.__thunder_handler = ThunderWSAPI()
        self.__thunder_handler.open_ws_connection(self.__cpe_ip + ":9998/jsonrpc")


    def tearDown(self):
        self.__thunder_handler.close_ws_connection()


    def test_A1_verify_number_of_plugins(self):
        result = self.__thunder_handler.controller_get_status()
        self.assertEqual(len(result['result']), len(self.__plugins), "The number of plugins does not match pattern: " +
            str(len(result['result'])) +" != "+ str(len(self.__plugins)))


    def test_A2_verify_plugins_status(self):
        plugins = copy.deepcopy(self.__plugins)
        result = self.__thunder_handler.controller_get_status()
        for plugin in result['result']:
            if plugin['callsign'] in plugins:
                with self.subTest(msg="Fail while checking: "+ plugin['callsign']):
                    self.assertEqual(plugin['classname'], plugins[plugin['callsign']]['classname'], "Controller returned unknown classname: " + plugin['classname'])
                    self.assertEqual(plugin['callsign'], plugins[plugin['callsign']]['callsign'], "Controller returned unknown callsign: " + plugin['callsign'])
                    for key in plugins[plugin['callsign']]:
                        self.assertEqual(plugin[key] , plugins[plugin['callsign']][key], "Key: " + key + " value: " + str(plugin[key]) +
                            " don't match pattern: " + str(plugins[plugin['callsign']][key]))

                del plugins[plugin['callsign']]
        self.assertEqual(len(plugins), 0 ,"Controller did not return all expected plugins: " + str(plugins))


    def test_A3_verify_plugins_state_change(self):
        result = self.__thunder_handler.controller_get_status()
        del result['result'][0]
        self.__thunder_handler.controller_register_event("all", "client.Controller.events")
        for plugin in result['result']:
            with self.subTest(msg="Fail while checking: "+ plugin['callsign']):
                if plugin['state'] == "activated":
                    msg_prefix="Method: controller_deactivate " + plugin['callsign'] + " plugin"
                    def signalValidator(resp):
                        self.assertEqual(resp['params']['callsign'], plugin['callsign'])
                        self.assertEqual(resp['params']['data']['state'], "deactivated")
                        self.assertEqual(resp['params']['data']['reason'], "Requested")
                        return True
                    result = self.__thunder_handler.controller_deactivate_plugin(plugin['callsign'], signalValidator)
                else:
                    msg_prefix="Method: controller_activate " + plugin['callsign'] + " plugin"
                    def signalValidator(resp):
                        self.assertEqual(resp['params']['callsign'], plugin['callsign'])
                        self.assertEqual(resp['params']['data']['state'], "activated")
                        self.assertEqual(resp['params']['data']['reason'], "Requested")
                        return True
                    result = self.__thunder_handler.controller_activate_plugin(plugin['callsign'], signalValidator)
                self.assertFalse("error" in result, msg_prefix +" return error " + str(result))

        self.__thunder_handler.controller_unregister_event("all", "client.Controller.events")


    def test_Z1_set_plugins_init_state(self):
        plugins = copy.deepcopy(self.__plugins)
        del plugins['Controller']
        for plugin in plugins:
            if plugins[plugin]['state'] == "activated":
                self.__thunder_handler.controller_activate_plugin(plugins[plugin]['callsign'])
            else:
                self.__thunder_handler.controller_deactivate_plugin(plugins[plugin]['callsign'])


