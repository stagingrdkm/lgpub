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


import os.path, sys, json, time
import socket, websocket, threading

from Libraries.Cpe.websocket.thunder.controllerWSAPI import *
from Libraries.Cpe.websocket.thunder.deviceInfoWSAPI import *
from Libraries.Cpe.websocket.thunder.displayInfoWSAPI import *
from Libraries.Cpe.websocket.thunder.monitorWSAPI import *
from Libraries.Cpe.websocket.thunder.ocdmWSAPI import *
from Libraries.Cpe.websocket.thunder.fmpWSAPI import *
from Libraries.Cpe.websocket.thunder.ociContainerWSAPI import *
from Libraries.Cpe.websocket.thunder.packagerWSAPI import *
from Libraries.Cpe.websocket.thunder.playerInfoWSAPI import *
from Libraries.Cpe.websocket.thunder.securityAgentWSAPI import *
from Libraries.Cpe.websocket.thunder.traceControlWSAPI import *
from Libraries.Cpe.websocket.thunder.webKitBrowserWSAPI import *


from Libraries.Cpe.websocket.CpeWebSocket import CpeWebSocket


class ThunderWSAPI:

    def __init__(self):
        self._ws_session_handler = None

    def open_ws_connection(self, ip_address, handler = None):
        self._ws_session_handler = CpeWebSocket(ip_address, handler)

    def close_ws_connection(self):
        self._ws_session_handler.close()


    ########### Controller WS API ###########

    def controller_get_status(self):
        result = self._ws_session_handler.call(CONTROLLER_status()).getJson()
        return result

    def controller_register_event(self, event, id, signal_validator=None):
        if signal_validator is not None:
            result = self._ws_session_handler.call(CONTROLLER_register(event, id),id+"."+event,signal_validator).getJson()
        else:
            result = self._ws_session_handler.call(CONTROLLER_register(event, id)).getJson()
        return result

    def controller_unregister_event(self, event, id, signal_validator=None):
        if signal_validator is not None:
            result = self._ws_session_handler.call(CONTROLLER_unregister(event, id),id+"."+event,signal_validator).getJson()
        else:
            result = self._ws_session_handler.call(CONTROLLER_unregister(event, id)).getJson()
        return result

    def controller_activate_plugin(self, plugin_name, signal_validator=None):
        if signal_validator is not None:
            result = self._ws_session_handler.call(CONTROLLER_activate(plugin_name),"client.Controller.events.all",signal_validator).getJson()
        else:
            result = self._ws_session_handler.call(CONTROLLER_activate(plugin_name)).getJson()
        return result

    def controller_deactivate_plugin(self, plugin_name, signal_validator=None):
        if signal_validator is not None:
            result = self._ws_session_handler.call(CONTROLLER_deactivate(plugin_name),"client.Controller.events.all",signal_validator).getJson()
        else:
            result = self._ws_session_handler.call(CONTROLLER_deactivate(plugin_name)).getJson()
        return result

    def controller_storeconfig(self):
        result = self._ws_session_handler.call(CONTROLLER_storeconfig()).getJson()
        return result

    def controller_harakiri(self):
        result = self._ws_session_handler.call(CONTROLLER_harakiri()).getJson()
        return result


    ########### Device Info WS API ###########

    def deviceinfo_systeminfo(self):
        result = self._ws_session_handler.call(DEVICEINFO_systeminfo()).getJson()
        return result

    def deviceinfo_addresses(self):
        result = self._ws_session_handler.call(DEVICEINFO_addresses()).getJson()
        return result

    def deviceinfo_socketinfo(self):
        result = self._ws_session_handler.call(DEVICEINFO_socketinfo()).getJson()
        return result


    ########### Display Info WS API ###########

    def displayinfo_edid(self, length=0):
        result = self._ws_session_handler.call(DISPLAYINFO_edid(length)).getJson()
        return result

    def displayinfo_widthincentimeters(self):
        result = self._ws_session_handler.call(DISPLAYINFO_widthincentimeters()).getJson()
        return result

    def displayinfo_heightincentimeters(self):
        result = self._ws_session_handler.call(DISPLAYINFO_heightincentimeters()).getJson()
        return result

    def displayinfo_totalgpuram(self):
        result = self._ws_session_handler.call(DISPLAYINFO_totalgpuram()).getJson()
        return result

    def displayinfo_freegpuram(self):
        result = self._ws_session_handler.call(DISPLAYINFO_freegpuram()).getJson()
        return result

    def displayinfo_isaudiopassthrough(self):
        result = self._ws_session_handler.call(DISPLAYINFO_isaudiopassthrough()).getJson()
        return result

    def displayinfo_connected(self):
        result = self._ws_session_handler.call(DISPLAYINFO_connected()).getJson()
        return result

    def displayinfo_width(self):
        result = self._ws_session_handler.call(DISPLAYINFO_width()).getJson()
        return result

    def displayinfo_height(self):
        result = self._ws_session_handler.call(DISPLAYINFO_height()).getJson()
        return result

    def displayinfo_verticalfreq(self):
        result = self._ws_session_handler.call(DISPLAYINFO_verticalfreq()).getJson()
        return result

    def displayinfo_get_hdcpprotection(self):
        result = self._ws_session_handler.call(DISPLAYINFO_get_hdcpprotection()).getJson()
        return result

    def displayinfo_set_hdcpprotection(self, hdcp_protocol):
        result = self._ws_session_handler.call(DISPLAYINFO_set_hdcpprotection(hdcp_protocol)).getJson()
        return result

    def displayinfo_portname(self):
        result = self._ws_session_handler.call(DISPLAYINFO_portname()).getJson()
        return result

    def displayinfo_tvcapabilities(self):
        result = self._ws_session_handler.call(DISPLAYINFO_tvcapabilities()).getJson()
        return result

    def displayinfo_stbcapabilities(self):
        result = self._ws_session_handler.call(DISPLAYINFO_stbcapabilities()).getJson()
        return result

    def displayinfo_hdrsetting(self):
        result = self._ws_session_handler.call(DISPLAYINFO_hdrsetting()).getJson()
        return result


    ########### Monitor WS API ###########

    def monitor_restartlimits(self, callsign, restart):
        result = self._ws_session_handler.call(MONITOR_restartlimits(callsign, restart)).getJson()
        return result

    def monitor_resetstats(self, callsign):
        result = self._ws_session_handler.call(MONITOR_resetstats(callsign)).getJson()
        return result

    def monitor_status(self):
        result = self._ws_session_handler.call(MONITOR_status()).getJson()
        return result


    ########### OCDM WS API ###########

    def ocdm_drms(self):
        result = self._ws_session_handler.call(OCDM_drms()).getJson()
        return result

    def ocdm_keysystems(self, system_name):
        result = self._ws_session_handler.call(OCDM_keysystems(system_name)).getJson()
        return result


    ########### FireboltMediaPlayer WS API ###########

    def fmp_create(self, id):
        result = self._ws_session_handler.call(FMP_create(id)).getJson()
        return result

    def fmp_load(self, id, url, autoplay):
        result = self._ws_session_handler.call(FMP_load(id, url, autoplay)).getJson()
        return result

    def fmp_seek(self, id, positionSec):
        result = self._ws_session_handler.call(FMP_seek(id, positionSec)).getJson()
        return result

    def fmp_play(self, id):
        result = self._ws_session_handler.call(FMP_play(id)).getJson()
        return result

    def fmp_pause(self, id):
        result = self._ws_session_handler.call(FMP_pause(id)).getJson()
        return result

    def fmp_stop(self, id):
        result = self._ws_session_handler.call(FMP_stop(id)).getJson()
        return result

    def fmp_release(self, id):
        result = self._ws_session_handler.call(FMP_release(id)).getJson()
        return result

    def fmp_register_event(self, event, id):
        result = self._ws_session_handler.call(FMP_register(event, id)).getJson()
        return result


    ########### OCI Container WS API ###########

    def ocicontainer_listContainers(self):
        result = self._ws_session_handler.call(OCICONTAINER_listContainers()).getJson()
        return result

    def ocicontainer_getContainerInfo(self, containerId):
        result = self._ws_session_handler.call(OCICONTAINER_getContainerInfo(containerId)).getJson()
        return result

    def ocicontainer_getContainerState(self, containerId):
        result = self._ws_session_handler.call(OCICONTAINER_getContainerState(containerId)).getJson()
        return result

    def ocicontainer_pauseContainer(self, containerId):
        result = self._ws_session_handler.call(OCICONTAINER_pauseContainer(containerId)).getJson()
        return result

    def ocicontainer_stopContainer(self, containerId):
        result = self._ws_session_handler.call(OCICONTAINER_stopContainer(containerId)).getJson()
        return result

    def ocicontainer_resumeContainer(self, containerId):
        result = self._ws_session_handler.call(OCICONTAINER_resumeContainer(containerId)).getJson()
        return result

    def ocicontainer_startContainer(self, containerId, bundlePath):
        result = self._ws_session_handler.call(OCICONTAINER_startContainer(containerId, bundlePath)).getJson()
        return result

    def ocicontainer_startContainerFromDobbySpec(self, containerId, dobbySpec):
        result = self._ws_session_handler.call(OCICONTAINER_startContainerFromDobbySpec(containerId, dobbySpec)).getJson()
        return result

    def ocicontainer_executeCommand(self, containerId, options, command):
        result = self._ws_session_handler.call(OCICONTAINER_executeCommand(containerId, options, command)).getJson()
        return result


    ########### Packager WS API ###########

    def packager_install(self, pkgId, ptype, url):
        result = self._ws_session_handler.call(PACKAGER_install(pkgId, ptype, url)).getJson()
        return result

    def packager_remove(self, pkgId):
        result = self._ws_session_handler.call(PACKAGER_remove(pkgId)).getJson()
        return result

    def packager_get_installed(self):
        result = self._ws_session_handler.call(PACKAGER_getInstalled()).getJson()
        return result

    def packager_get_available_space(self):
        result = self._ws_session_handler.call(PACKAGER_getAvailableSpace()).getJson()
        return result


    ########### Player Info WS API ###########

    def playerinfo_videocodecs(self):
        result = self._ws_session_handler.call(PLAYERINFO_videocodecs()).getJson()
        return result

    def playerinfo_audiocodecs(self):
        result = self._ws_session_handler.call(PLAYERINFO_audiocodecs()).getJson()
        return result

    def playerinfo_resolution(self):
        result = self._ws_session_handler.call(PLAYERINFO_resolution()).getJson()
        return result

    def playerinfo_isaudioequivalenceenabled(self):
        result = self._ws_session_handler.call(PLAYERINFO_isaudioequivalenceenabled()).getJson()
        return result

    def playerinfo_dolby_atmosmetadata(self):
        result = self._ws_session_handler.call(PLAYERINFO_dolby_atmosmetadata()).getJson()
        return result

    def playerinfo_dolby_soundmode(self):
        result = self._ws_session_handler.call(PLAYERINFO_dolby_soundmode()).getJson()
        return result

    def playerinfo_dolby_enableatmosoutput(self, state):
        result = self._ws_session_handler.call(PLAYERINFO_dolby_enableatmosoutput(state)).getJson()
        return result

    def playerinfo_dolby_set_mode(self, dolby_mode):
        result = self._ws_session_handler.call(PLAYERINFO_dolby_set_mode(dolby_mode)).getJson()
        return result

    def playerinfo_dolby_get_mode(self):
        result = self._ws_session_handler.call(PLAYERINFO_dolby_get_mode()).getJson()
        return result


    ########### Security Agent WS API ###########

    def securityagent_createtoken(self, url, user, hash):
        result = self._ws_session_handler.call(SECURITYAGENT_createtoken(url, user, hash)).getJson()
        return result

    def securityagent_validate(self, token):
        result = self._ws_session_handler.call(SECURITYAGENT_validate(token)).getJson()
        return result


    ########### Trace Control WS API ###########

    def tracecontrol_status(self, module, category):
        result = self._ws_session_handler.call(TRACECONTROL_status(module, category)).getJson()
        return result

    def tracecontrol_set(self, module, category, state):
        result = self._ws_session_handler.call(TRACECONTROL_set(module, category, state)).getJson()
        return result


    ########### WebKitBrowser WS API ###########

    def webkitbrowser_bridgeevent(self, app = "WebKitBrowser"):
        result = self._ws_session_handler.call(WEBKITBROWSER_bridgeevent(app)).getJson()
        return result

    def webkitbrowser_bridgereply(self, app = "WebKitBrowser"):
        result = self._ws_session_handler.call(WEBKITBROWSER_bridgereply(app)).getJson()
        return result

    def webkitbrowser_localstorageenabled(self, app = "WebKitBrowser"):
        result = self._ws_session_handler.call(WEBKITBROWSER_localstorageenabled(app)).getJson()
        return result

    def webkitbrowser_useragent(self, app = "WebKitBrowser"):
        result = self._ws_session_handler.call(WEBKITBROWSER_useragent(app)).getJson()
        return result

    def webkitbrowser_headers(self, app = "WebKitBrowser"):
        result = self._ws_session_handler.call(WEBKITBROWSER_headers(app)).getJson()
        return result

    def webkitbrowser_httpcookieacceptpolicy(self, app = "WebKitBrowser"):
        result = self._ws_session_handler.call(WEBKITBROWSER_httpcookieacceptpolicy(app)).getJson()
        return result

    def webkitbrowser_languages(self, app = "WebKitBrowser"):
        result = self._ws_session_handler.call(WEBKITBROWSER_languages(app)).getJson()
        return result
