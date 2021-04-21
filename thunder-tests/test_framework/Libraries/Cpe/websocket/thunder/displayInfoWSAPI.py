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


class DISPLAYINFO_portname:
    method = "DisplayInfo.1.portname"
    __doc__ = "Provides access to the video output port on the CPE used for connection to TV."

    def __init__(self):
        self.params = {}

    def set(self):
        self.params = {}
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method}
        return ws.send(jsonobj, *args, **kwargs)


class DISPLAYINFO_totalgpuram:
    method = "DisplayInfo.1.totalgpuram"
    __doc__ = "Provides access to the total GPU DRAM memory (in bytes)."

    def __init__(self):
        self.params = {}

    def set(self):
        self.params = {}
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method}
        return ws.send(jsonobj, *args, **kwargs)


class DISPLAYINFO_verticalfreq:
    method = "DisplayInfo.1.verticalfreq"
    __doc__ = "Provides access to the vertical Frequency."

    def __init__(self):
        self.params = {}

    def set(self):
        self.params = {}
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method}
        return ws.send(jsonobj, *args, **kwargs)


class DISPLAYINFO_widthincentimeters:
    method = "DisplayInfo.1.widthincentimeters"
    __doc__ = "Horizontal size in centimeters."

    def __init__(self):
        self.params = {}

    def set(self):
        self.params = {}
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method}
        return ws.send(jsonobj, *args, **kwargs)


class DISPLAYINFO_height:
    method = "DisplayInfo.1.height"
    __doc__ = "Provides access to the vertical resolution of TV."

    def __init__(self):
        self.params = {}

    def set(self):
        self.params = {}
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method}
        return ws.send(jsonobj, *args, **kwargs)


class DISPLAYINFO_stbcapabilities:
    method = "DisplayInfo.1.stbcapabilities"
    __doc__ = "Provides access to the HDR formats supported by CPE."

    def __init__(self):
        self.params = {}

    def set(self):
        self.params = {}
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method}
        return ws.send(jsonobj, *args, **kwargs)


class DISPLAYINFO_width:
    method = "DisplayInfo.1.width"
    __doc__ = "Provides access to the horizontal resolution of TV."

    def __init__(self):
        self.params = {}

    def set(self):
        self.params = {}
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method}
        return ws.send(jsonobj, *args, **kwargs)


class DISPLAYINFO_isaudiopassthrough:
    method = "DisplayInfo.1.isaudiopassthrough"
    __doc__ = "Provides access to the current audio passthrough status on HDMI."

    def __init__(self):
        self.params = {}

    def set(self):
        self.params = {}
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method}
        return ws.send(jsonobj, *args, **kwargs)


class DISPLAYINFO_connected:
    method = "DisplayInfo.1.connected"
    __doc__ = "Provides access to the current HDMI connection status."

    def __init__(self):
        self.params = {}

    def set(self):
        self.params = {}
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method}
        return ws.send(jsonobj, *args, **kwargs)


class DISPLAYINFO_tvcapabilities:
    method = "DisplayInfo.1.tvcapabilities"
    __doc__ = "Provides access to the HDR formats supported by TV."

    def __init__(self):
        self.params = {}

    def set(self):
        self.params = {}
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method}
        return ws.send(jsonobj, *args, **kwargs)


class DISPLAYINFO_freegpuram:
    method = "DisplayInfo.1.freegpuram"
    __doc__ = "Provides access to the free GPU DRAM memory (in bytes)."

    def __init__(self):
        self.params = {}

    def set(self):
        self.params = {}
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method}
        return ws.send(jsonobj, *args, **kwargs)


class DISPLAYINFO_edid:
    method = "DisplayInfo.1.edid"
    __doc__ = "TV's Extended Display Identification Data"

    def __init__(self, length):
        self.params = {}
        self.params["length"] = length

    def set(self, length):
        self.params = {}
        self.params["length"] = length
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method, "params": self.params}
        return ws.send(jsonobj, *args, **kwargs)


class DISPLAYINFO_heightincentimeters:
    method = "DisplayInfo.1.heightincentimeters"
    __doc__ = "Vertical size in centimeters."

    def __init__(self):
        self.params = {}

    def set(self):
        self.params = {}
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method}
        return ws.send(jsonobj, *args, **kwargs)


class DISPLAYINFO_hdrsetting:
    method = "DisplayInfo.1.hdrsetting"
    __doc__ = "Provides access to the HDR format in use."

    def __init__(self):
        self.params = {}

    def set(self):
        self.params = {}
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method}
        return ws.send(jsonobj, *args, **kwargs)


class DISPLAYINFO_set_hdcpprotection:
    method = "DisplayInfo.1.hdcpprotection"
    __doc__ = "Provides access to the HDCP protocol used for transmission: HdcpUnencrypted, Hdcp1X, Hdcp2X, HdcpAuto"

    def __init__(self, hdcp_protocol):
        self.params = hdcp_protocol

    def set(self, hdcp_protocol):
        self.params = hdcp_protocol
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method, "params": self.params}
        return ws.send(jsonobj, *args, **kwargs)

class DISPLAYINFO_get_hdcpprotection:
    method = "DisplayInfo.1.hdcpprotection"
    __doc__ = "Provides access to the HDCP protocol used for transmission: HdcpUnencrypted, Hdcp1X, Hdcp2X, HdcpAuto"

    def __init__(self):
        self.params = {}

    def set(self):
        self.params = {}
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method}
        return ws.send(jsonobj, *args, **kwargs)

