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

class TestThunderPlayerInfoWSAPI(unittest.TestCase):

    def setUp(self):
        self.__cpe_ip = sys.argv[1]
        self.__thunder_handler = ThunderWSAPI()
        self.__thunder_handler.open_ws_connection(self.__cpe_ip + ":9998/jsonrpc")
        self.__thunder_handler.controller_activate_plugin("PlayerInfo")


    def tearDown(self):
        self.__thunder_handler.close_ws_connection()


    def test_G1_verify_playerinfo_plugin(self):

        with self.subTest(msg="Fail while checking: PlayerInfo plugin"):
            codecs_list = ["VideoH263", "VideoH264", "VideoH265","VideoMpeg", "VideoVp8", "VideoVp9"]
            msg_prefix="Method: playerinfo_videocodecs"
            result = self.__thunder_handler.playerinfo_videocodecs()
            self.assertFalse("error" in result, msg_prefix +" return error")
            self.assertEqual(len(result['result']), len(codecs_list), msg_prefix + " return unexpected number of video codecs")
            for codec in codecs_list:
                self.assertTrue(codec in result['result'], msg_prefix + " didn't return video codec: " + codec)

        with self.subTest(msg="Fail while checking: PlayerInfo plugin"):
            codecs_list = ["AudioAac", "AudioAc3", "AudioAc3Plus", "AudioDts", "AudioMpeg1", "AudioMpeg2",
                "AudioMpeg3", "AudioMpeg4", "AudioOpus", "AudioVorbisOgg"]  # exclude "AudioUndefined",
            msg_prefix="Method: playerinfo_audiocodecs"
            result = self.__thunder_handler.playerinfo_audiocodecs()
            self.assertFalse("error" in result, msg_prefix +" return error")
            self.assertEqual(len(result['result']), len(codecs_list), msg_prefix + " return unexpected number of audio codecs")
            for codec in codecs_list:
                self.assertTrue(codec in result['result'], msg_prefix + " didn't return audio codec: " + codec)

        with self.subTest(msg="Fail while checking: PlayerInfo plugin"):

            pfx="FMP"
            pid="MyPlayer"
            url="http://wowzaec2demo.streamlock.net/vod/_definst_/ElephantsDream/smil:ElephantsDream.smil/manifest_mvtime.mpd"


            self.assertFalse("error" in result, pfx +" return error")
            self.__thunder_handler.controller_activate_plugin("OCDM")
            self.__thunder_handler.controller_activate_plugin("org.rdk.FireboltMediaPlayer")

            result = self.__thunder_handler.fmp_create(pid)
            result = self.__thunder_handler.fmp_load(pid, url, False)
            self.assertFalse("error" in result, pfx + " return error")
            result = self.__thunder_handler.fmp_play(pid)
            self.assertFalse("error" in result, pfx + " return error")

            time.sleep(5)


            validate_list = ["Resolution480I", "Resolution480P", "Resolution576I", "Resolution576P", "Resolution720P",
                "Resolution1080I", "Resolution1080P", "Resolution2160P30", "Resolution2160P60"]  # exclude "ResolutionUnknown"
            msg_prefix="Method: playerinfo_resolution"
            result = self.__thunder_handler.playerinfo_resolution()
            self.assertFalse("error" in result, msg_prefix +" return error")
            self.assertTrue(result['result'] in validate_list , msg_prefix + " return unexpected value: " + str(result['result']))




            result = self.__thunder_handler.fmp_stop(pid)
            self.assertFalse("error" in result, pfx +" return error at stop")
            result = self.__thunder_handler.fmp_release(pid)
            self.assertFalse("error" in result, pfx +" return error at release")



        with self.subTest(msg="Fail while checking: PlayerInfo plugin"):
            msg_prefix="Method: playerinfo_isaudioequivalenceenabled"
            result = self.__thunder_handler.playerinfo_isaudioequivalenceenabled()
            self.assertFalse("error" in result, msg_prefix +" return error")
            self.assertTrue(type(result['result']) is bool, msg_prefix + " result is not boolen value")

        with self.subTest(msg="Fail while checking: PlayerInfo plugin"):
            msg_prefix="Method: playerinfo_dolby_atmosmetadata"
            result = self.__thunder_handler.playerinfo_dolby_atmosmetadata()
            self.assertFalse("error" in result, msg_prefix +" return error")
            self.assertTrue(type(result['result']) is bool, msg_prefix + " result is not boolen value")

        with self.subTest(msg="Fail while checking: PlayerInfo plugin"):
            validate_list = ["Mono", "Stereo", "Surround", "Passthru"]  # exclude "Unknown"
            msg_prefix="Method: playerinfo_dolby_soundmode"
            result = self.__thunder_handler.playerinfo_dolby_soundmode()
            self.assertFalse("error" in result, msg_prefix +" return error")
            self.assertTrue(result['result'] in validate_list , msg_prefix + " return unexpected value: " + str(result['result']))

        with self.subTest(msg="Fail while checking: PlayerInfo plugin"):
            msg_prefix="Method: playerinfo_dolby_enableatmosoutput"
            result = self.__thunder_handler.playerinfo_dolby_enableatmosoutput(True)
            self.assertFalse("error" in result, msg_prefix +" return error")
            result = self.__thunder_handler.playerinfo_dolby_enableatmosoutput(False)
            self.assertFalse("error" in result, msg_prefix +" return error")

        with self.subTest(msg="Fail while checking: PlayerInfo plugin"):
            validate_list = ["DigitalPcm", "DigitalPlus", "DigitalAc3", "Auto", "Ms12"]
            msg_prefix="Method: playerinfo_dolby_get_mode"
            result = self.__thunder_handler.playerinfo_dolby_get_mode()
            self.assertFalse("error" in result, msg_prefix +" return error")
            self.assertTrue(result['result'] in validate_list , msg_prefix + " return unexpected value: " + str(result['result']))

            for dolby_mode in validate_list:
                result = self.__thunder_handler.playerinfo_dolby_set_mode(dolby_mode)
                msg_prefix="Method: playerinfo_dolby_set_mode"
                self.assertFalse("error" in result, msg_prefix +" return error")
                result = self.__thunder_handler.playerinfo_dolby_get_mode()
                msg_prefix="Method: playerinfo_dolby_get_mode"
                self.assertEqual(result['result'], dolby_mode, msg_prefix + " return " + str(result['result']) + " instead of " + dolby_mode)

