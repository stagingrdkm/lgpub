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
import threading
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))

from Libraries.Cpe.ThunderWSAPI import ThunderWSAPI
from Libraries.Common.JsonReader import *

class FmpEventHandler:
    def __init__(self, pid):
        self.mutex = threading.Lock()
        self.pid = pid
        self.keys = {}

    def handle(self, resp):
        result = False
        self.mutex.acquire()
        method = resp['method']
        params = resp['params']
        if self.pid in params:
            result = True
            keys = params[self.pid]
            for key in keys:
#                print ("Got " + method + "." + str(key) + "=" + str(keys[key]));
                self.keys[key] = keys[key]
        self.mutex.release()
        return result

    def get(self, key):
        result = -1
        self.mutex.acquire()
        if key in self.keys:
            result = self.keys[key]
        self.mutex.release()
        return result


class TestThunderFmpWSAPI(unittest.TestCase):

    def setUp(self):
        self.pid = "MyPlayer"
        self.handler = FmpEventHandler(self.pid)
        self.__cpe_ip = sys.argv[1]
        self.__thunder_handler = ThunderWSAPI()
        self.__thunder_handler.open_ws_connection(self.__cpe_ip + ":9998/jsonrpc", self.handler)
        self.__thunder_handler.controller_activate_plugin("OCDM")
        self.__thunder_handler.controller_activate_plugin("org.rdk.FireboltMediaPlayer")

    def tearDown(self):
        self.__thunder_handler.controller_deactivate_plugin("org.rdk.FireboltMediaPlayer")
        self.__thunder_handler.controller_deactivate_plugin("OCDM")
        self.__thunder_handler.close_ws_connection()

    def checkState(self, expected):
        with self.subTest(msg="Check state"):
            state = self.handler.get('state')
            self.assertEqual(state, expected, "Wrong state")

    def checkSpeed(self, expected):
        with self.subTest(msg="Check speed"):
            speed = self.handler.get('speed')
            self.assertEqual(speed, expected, "Wrong speed")

    def checkPositionGt(self, expectedSec):
        with self.subTest(msg="Check position"):
            pos = self.handler.get('positionMiliseconds')
            self.assertGreater(pos, expectedSec * 1000, "Wrong position")

    def checkPositionLs(self, expectedSec):
        with self.subTest(msg="Check position"):
            pos = self.handler.get('positionMiliseconds')
            self.assertLess(pos, expectedSec * 1000, "Wrong position")

    def checkPlayback(self, url):
        pfx = "FMP"
        pid = self.pid
        pos1 = 20
        pos2 = 10

        result = self.__thunder_handler.fmp_create(pid)
        self.assertFalse("error" in result, pfx +" return error")

        with self.subTest(msg="Register event handler"):
            result = self.__thunder_handler.fmp_register_event("playbackStarted",       "org.rdk.FirebolMediaPlayer.1")
            self.assertFalse("error" in result, pfx +" return error")
            result = self.__thunder_handler.fmp_register_event("playbackStateChanged",  "org.rdk.FirebolMediaPlayer.1")
            self.assertFalse("error" in result, pfx +" return error")
            result = self.__thunder_handler.fmp_register_event("playbackProgressUpdate","org.rdk.FirebolMediaPlayer.1")
            self.assertFalse("error" in result, pfx +" return error")
            result = self.__thunder_handler.fmp_register_event("bufferingChanged",      "org.rdk.FirebolMediaPlayer.1")
            self.assertFalse("error" in result, pfx +" return error")
            result = self.__thunder_handler.fmp_register_event("playbackSpeedChanged",  "org.rdk.FirebolMediaPlayer.1")
            self.assertFalse("error" in result, pfx +" return error")
            result = self.__thunder_handler.fmp_register_event("playbackFailed",        "org.rdk.FirebolMediaPlayer.1")
            self.assertFalse("error" in result, pfx +" return error")

        print ("Load '" + url + "'")
        result = self.__thunder_handler.fmp_load(pid, url, False)
        self.assertFalse("error" in result, pfx +" return error")

        result = self.__thunder_handler.fmp_play(pid)
        self.assertFalse("error" in result, pfx +" return error")

        with self.subTest(msg="Seek forward"):
            print ("Wait before seek..")
            time.sleep(3)
            result = self.__thunder_handler.fmp_seek(pid, pos1)
            self.assertFalse("error" in result, pfx +" return error at seek")
            print ("Wait after seek..")
            time.sleep(5)
            self.checkState(8)
            self.checkSpeed(1)
            self.checkPositionGt(pos1)

        with self.subTest(msg="Pause then play"):
            result = self.__thunder_handler.fmp_pause(pid)
            self.assertFalse("error" in result, pfx +" return error at pause")
            print ("Wait before resume..")
            time.sleep(3)
            self.checkState(6)
            self.checkSpeed(0)
            result = self.__thunder_handler.fmp_play(pid)
            self.assertFalse("error" in result, pfx +" return error at play")

        with self.subTest(msg="Seek backward"):
            print ("Wait before seek..")
            time.sleep(3)
            result = self.__thunder_handler.fmp_seek(pid, pos2)
            self.assertFalse("error" in result, pfx +" return error at seek")
            print ("Wait after seek..")
            time.sleep(5)
            self.checkPositionLs(pos1)
            self.checkPositionGt(pos2)

        with self.subTest(msg="Stop"):
            print ("Wait before stop..")
            time.sleep(3)
            result = self.__thunder_handler.fmp_stop(pid)
            self.assertFalse("error" in result, pfx +" return error at stop")

        result = self.__thunder_handler.fmp_release(pid)
        self.assertFalse("error" in result, pfx +" return error at release")

    def test_J1_verify_fmp_hls_playback(self):
        self.checkPlayback("http://demo.unified-streaming.com/video/tears-of-steel/tears-of-steel.ism/.m3u8")

    def test_J2_verify_fmp_dash_playback(self):
        self.checkPlayback("http://amssamples.streaming.mediaservices.windows.net/bf657309-71d9-4436-b94b-8ac0d2ca222b/SintelTrailer.ism/manifest(format=mpd-time-csf)")

