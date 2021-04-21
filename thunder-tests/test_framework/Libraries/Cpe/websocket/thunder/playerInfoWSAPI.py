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


class PLAYERINFO_dolby_soundmode:
    method = "PlayerInfo.1.dolby_soundmode"
    __doc__ = "Get Sound Mode: Mono/Stereo/Surround"

    def __init__(self):
        self.params = {}

    def set(self):
        self.params = {}
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method}
        return ws.send(jsonobj, *args, **kwargs)


class PLAYERINFO_videocodecs:
    method = "PlayerInfo.1.videocodecs"
    __doc__ = "Get currnet playback Audio Codec: VideoUndefined, VideoH263, VideoH264, VideoH265, VideoH26510, VideoMpeg, VideoVp8, VideoVp9, VideoVp10"

    def __init__(self):
        self.params = {}

    def set(self):
        self.params = {}
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method}
        return ws.send(jsonobj, *args, **kwargs)


class PLAYERINFO_audiocodecs:
    method = "PlayerInfo.1.audiocodecs"
    __doc__ = "Get currnet playback Audio Codec: AudioUndefined, AudioAac, AudioAc3, AudioAc3Plus, AudioDts, AudioMpeg1, AudioMpeg2, AudioMpeg3, AudioMpeg4, AudioOpus, AudioVorbisOgg, AudioWav."

    def __init__(self):
        self.params = {}

    def set(self):
        self.params = {}
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method}
        return ws.send(jsonobj, *args, **kwargs)


class PLAYERINFO_resolution:
    method = "PlayerInfo.1.resolution"
    __doc__ = "Get current Video playback resolution."

    def __init__(self):
        self.params = {}

    def set(self):
        self.params = {}
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method}
        return ws.send(jsonobj, *args, **kwargs)


class PLAYERINFO_dolby_atmosmetadata:
    method = "PlayerInfo.1.dolby_atmosmetadata"
    __doc__ = "Atmos capabilities of Sink"

    def __init__(self):
        self.params = {}

    def set(self):
        self.params = {}
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method}
        return ws.send(jsonobj, *args, **kwargs)


class PLAYERINFO_dolby_set_mode:
    method = "PlayerInfo.1.dolby_mode"
    __doc__ = "Set Dolby Mode: DigitalPcm, DigitalPlus, DigitalAc3, Auto, Ms12"

    def __init__(self, dolby_mode):
        self.params = dolby_mode

    def set(self, dolby_mode):
        self.params = dolby_mode
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method, "params": self.params}
        return ws.send(jsonobj, *args, **kwargs)


class PLAYERINFO_dolby_get_mode:
    method = "PlayerInfo.1.dolby_mode"
    __doc__ = "Get Dolby Mode: DigitalPcm, DigitalPlus, DigitalAc3, Auto, Ms12"

    def __init__(self):
        self.params = {}

    def set(self):
        self.params = {}
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method}
        return ws.send(jsonobj, *args, **kwargs)


class PLAYERINFO_isaudioequivalenceenabled:
    method = "PlayerInfo.1.isaudioequivalenceenabled"
    __doc__ = "Checks Loudness Equivalence in platform."

    def __init__(self):
        self.params = {}

    def set(self):
        self.params = {}
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method}
        return ws.send(jsonobj, *args, **kwargs)


class PLAYERINFO_dolby_enableatmosoutput:
    method = "PlayerInfo.1.dolby_enableatmosoutput"
    __doc__ = "Enable/Disable Atmos Audio Output"

    def __init__(self, state):
        self.params = state

    def set(self, state):
        self.params = state
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method, "params": self.params}
        return ws.send(jsonobj, *args, **kwargs)
