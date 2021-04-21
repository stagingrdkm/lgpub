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

class TestThunderDisplayInfoWSAPI(unittest.TestCase):

    def setUp(self):
        self.__cpe_ip = sys.argv[1]
        self.__tv_set = True
        self.__thunder_handler = ThunderWSAPI()
        self.__thunder_handler.open_ws_connection(self.__cpe_ip + ":9998/jsonrpc")


    def tearDown(self):
        self.__thunder_handler.close_ws_connection()


    def test_C1_verify_display_info_plugin(self):

        with self.subTest(msg="Fail while checking: DisplayInfo plugin"):
            msg_prefix="Methods:"
            result = self.__thunder_handler.displayinfo_connected()
            self.assertFalse("error" in result, msg_prefix +" displayinfo_connected return error")
            self.assertTrue(type(result['result']) is bool, msg_prefix + " displayinfo_connected result is not boolen value")
            hdmi_is_connected = result['result']
            if self.__tv_set == True:
                self.assertTrue(result['result'], msg_prefix + " displayinfo_connected: " + str(result['result']) +
                    ". Make sure that CPE is connected to the TV via HDMI cable and TV is turned on" )

            edid_result = self.__thunder_handler.displayinfo_edid(1000)
            self.assertFalse("error" in edid_result, msg_prefix +" displayinfo_edid return error")
            self.assertTrue("length" in edid_result['result'], msg_prefix + " displayinfo_edid didn't return key \"length\"")
            self.assertTrue("data" in edid_result['result'], msg_prefix + " displayinfo_edid didn't return key \"data\"")

            width_result = self.__thunder_handler.displayinfo_widthincentimeters()
            self.assertFalse("error" in width_result, msg_prefix +" displayinfo_widthincentimeters return error")
            height_result = self.__thunder_handler.displayinfo_heightincentimeters()
            self.assertFalse("error" in height_result, msg_prefix +" displayinfo_heightincentimeters return error")

            if hdmi_is_connected == True:
                self.assertTrue((edid_result['result']['length'] > 20), msg_prefix + " displayinfo_edid length ")
                self.assertIn("AP///////w", edid_result['result']['data'], msg_prefix + " displayinfo_edid don't return fixed edid header pattern")
                self.assertEqual(width_result['result'], 16, msg_prefix + " displayinfo_widthincentimeters return "+str(width_result['result'])+" instead of 16")
                self.assertEqual(height_result['result'], 9, msg_prefix + " displayinfo_heightincentimeters return "+str(height_result['result'])+" instead of 9")
            else:
                self.assertTrue((edid_result['result']['length'] == 9), msg_prefix + " didn't return key \"length\"")
                self.assertEqual(edid_result['result']['data'], "dW5rbm93bgAA" , msg_prefix + " didn't return key \"length\"")
                self.assertEqual(width_result['result'], 0 , msg_prefix + " displayinfo_widthincentimeters return key "+str(width_result['result'])+" instead of 0")
                self.assertEqual(height_result['result'], 0 , msg_prefix + " displayinfo_heightincentimeters return key "+str(height_result['result'])+" instead of 0")

        with self.subTest(msg="Fail while checking: DisplayInfo plugin"):
            msg_prefix="Method: displayinfo_totalgpuram"
            result = self.__thunder_handler.displayinfo_totalgpuram()
            self.assertFalse("error" in result, msg_prefix +" return error")
            self.assertTrue(result['result'] > 400000000, msg_prefix + " didn't return expected (402653184) totalgpuram value: " + str(result['result']))

        with self.subTest(msg="Fail while checking: DisplayInfo plugin"):
            msg_prefix="Method: displayinfo_freegpuram"
            result = self.__thunder_handler.displayinfo_freegpuram()
            self.assertFalse("error" in result, msg_prefix +" return error")
            self.assertTrue(result['result'] > 270000000, msg_prefix + " didn't return expected freegpuramvalue ")

        with self.subTest(msg="Fail while checking: DisplayInfo plugin"):
            msg_prefix="Method: displayinfo_isaudiopassthrough"
            result = self.__thunder_handler.displayinfo_isaudiopassthrough()
            self.assertFalse("error" in result, msg_prefix +" return error")
            self.assertTrue(type(result['result']) is bool, msg_prefix + " result is not boolen value")

        with self.subTest(msg="Fail while checking: DisplayInfo plugin"):
            msg_prefix="Method: displayinfo_width"
            result = self.__thunder_handler.displayinfo_width()
            self.assertFalse("error" in result, msg_prefix +" return error")
            self.assertEqual(result['result'], 1920, msg_prefix + " return "+str(result['result']) + " instead of 1920")

        with self.subTest(msg="Fail while checking: DisplayInfo plugin"):
            msg_prefix="Method: displayinfo_height"
            result = self.__thunder_handler.displayinfo_height()
            self.assertFalse("error" in result, msg_prefix +" return error")
            self.assertEqual(result['result'], 1080, msg_prefix + " return "+str(result['result']) + " instead of 1080")


        with self.subTest(msg="Fail while checking: DisplayInfo plugin"):
            msg_prefix="Method: displayinfo_verticalfreq"
            result = self.__thunder_handler.displayinfo_verticalfreq()
            self.assertFalse("error" in result, msg_prefix +" return error")
            self.assertTrue(result['result'] > 0 and result['result'] <= 120, msg_prefix +
                " displayinfo_verticalfreq return value out of range:" + str(result['result']))

        with self.subTest(msg="Fail while checking: DisplayInfo plugin"):
            validate_list = ["HdcpUnencrypted", "Hdcp1X", "Hdcp2X", "HdcpAuto"]
            msg_prefix="Method: displayinfo_get_hdcpprotection"
            initial_result = self.__thunder_handler.displayinfo_get_hdcpprotection()
            self.assertFalse("error" in initial_result, msg_prefix + " return error")
            self.assertTrue(initial_result['result'] in validate_list, msg_prefix + " return unexpected value: " + str(initial_result['result']))

            for hdcp_protocol in validate_list:
                result = self.__thunder_handler.displayinfo_set_hdcpprotection(hdcp_protocol)
                msg_prefix="Method: displayinfo_set_hdcpprotection"
                self.assertFalse("error" in result, msg_prefix +" return error")
                result = self.__thunder_handler.displayinfo_get_hdcpprotection()
                msg_prefix="Method: displayinfo_set_hdcpprotection"
                self.assertEqual(result['result'], hdcp_protocol, msg_prefix + " return " + str(result['result']) + " instead of " + hdcp_protocol)

            result = self.__thunder_handler.displayinfo_set_hdcpprotection(initial_result['result'])

        with self.subTest(msg="Fail while checking: DisplayInfo plugin"):
            msg_prefix="Method: displayinfo_portname"
            result = self.__thunder_handler.displayinfo_portname()
            self.assertFalse("error" in result, msg_prefix +" return error")
            self.assertEqual(result['result'], "HDMI0", msg_prefix + " return "+str(result['result']) + " instead of HDMI0")



