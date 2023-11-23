#!/usr/bin/env python3
#
# Copyright (c) 2023, Liberty Global Service B.V. all rights reserved.
#
# required deps: pip3 install requests colorama websocket-client
import sys
import os
import json
import random
import time
import requests  # pip3 install requests
from colorama import Fore, init  # pip3 install colorama
import websocket  # pip3 install websocket-client
from requests.auth import HTTPBasicAuth

# ####### CONFIG SECTION , change config here
ASMS_PLATFORM = "" ## if not set then default below is used
ASMS_FIRMWARE = "" ## if not set then default below is used
ASMS_USERNAME = ""
ASMS_PASSWORD = ""
MAX_LOG_LINES = 10
MAX_CHARS_PER_LOG_LINE = 512
SKIP_AUTO_DETECT_DAC_CONFIG = False
# #################################################

# ONEMW ########
DEFAULT_ASMS_PLATFORM_ONEMW = "VIP7002W"
DEFAULT_ASMS_FIRMWARE_ONEMW = "0.1.3-70bb2a370ec7f7e3a1c4a95c6f51924dc55712cf-dbg"
MIMETYPE_ONEMW = "application/vnd.rdk-app.dac.native"
ASMS_MAINTAINER_ONEMW = "lgi-dac"
ASMS_URL_ONEMW = "http://appstore-metadata-service.labci.ecx.appdev.io"
# Swagger http://appstore-metadata-service.labci.ecx.appdev.io/swagger-ui/index.html?configUrl=/v3/api-docs/swagger-config

# RDK ##########
RESIDENT_APP_ID = "residentapp"
DEFAULT_ASMS_PLATFORM_RDK = "rpi3"
DEFAULT_ASMS_FIRMWARE_RDK = "1.0.0-f4b0603d7d93dfa10ed932ddb0f324d334bc40f9-dbg"
MIMETYPE_RDK = "application/dac.native"
ASMS_MAINTAINER_RDK = "rdk"
ASMS_URL_RDK = "http://rdkm-asms-external-1156877020.eu-central-1.elb.amazonaws.com:8080"
# Swagger http://rdkm-asms-external-1156877020.eu-central-1.elb.amazonaws.com:8080/swagger-ui/index.html?configUrl=/v3/api-docs/swagger-config
#The same ASMS but with basic auth:
#ASMS_URL_RDK = "https://asms.default.consult-red.net"
# Swagger https://asms.default.consult-red.net/swagger-ui/index.html?configUrl=/v3/api-docs/swagger-config

# ONEMW PLATFORMS AND FIRMWARES
# 2008C-STB
#   yocto 3.1 - with /tmp/rialto-0 path:
#     FIRMWARE = "0.1.1-00b7e2b8621a78adc2f1845abafdd89c2969e189-dbg"
#   yocto 3.1 - with /var/run/rialto/{id} path and extra rialtoaccess GID:
#     FIRMWARE = "0.1.3-837c064a511bcc637a9410f6064868c3311ed3f4-dbg"
#
# VIP7002W
#   yocto 3.1 - with /tmp/rialto-0 path:
#     FIRMWARE = "0.1.1-2ca0e8774ba96c08b78b621afe5991dd4a397e1b-dbg"
#   yocto 3.1 - with /var/run/rialto/{id} path and extra rialtoaccess GID:
#     FIRMWARE = "0.1.3-70bb2a370ec7f7e3a1c4a95c6f51924dc55712cf-dbg"
#
# VIP7002W RDK6 WLPL (westeros)
#   yocto 3.1 - with /var/run/rialto/{id} path and extra rialtoaccess GID:
#     FIRMWARE = "0.1.3-971d695bdfab6fb310e3f493b33bcce35d80a53e-dbg"

# RDK PLATFORMS AND FIRMWARES
# 7218c
#   yocto 3.1:
#     FIRMWARE = "1.0.0-54cd2714c76069b5550e7f4b60aafba9bb230c07-dbg"
# ah212
#   yocto 3.1:
#     FIRMWARE = "1.0.0-aaa9510325f054535768497092c973872d44fef3-dbg"
# ap222
#   yocto 3.1:
#     FIRMWARE = "1.0.0-8d58497b284a33438d8c3a6e727caba1ac6ff5c8-dbg"
# m393
#   yocto 3.1:
#     FIRMWARE = "1.0.0-897cf9072a6a5142b5c99054c8624a7ba0297f9a-dbg"
# rpi3
#   yocto 3.1:
#     FIRMWARE = "1.0.0-f4b0603d7d93dfa10ed932ddb0f324d334bc40f9-dbg"
# rpi4
#   yocto 3.1:
#     FIRMWARE = "1.0.0-e71889dc02521bfdc2f9f38f750b34224184c375-dbg"
# rtd1319
#   yocto 3.1:
#     FIRMWARE = "1.0.0-de43b2c138d739b6fc199deb2282c482935d73af-dbg"
class DacTool:
    def __init__(self, stb_ip):
        self.asms_reachable = None
        self.stb_ip = stb_ip
        self.ws_thunder = "ws://" + self.stb_ip + ":9998/jsonrpc"
        self.ws_awc = "ws://" + self.stb_ip + ":8083"
        self.logs = []
        self.mimetype = ''
        self.asms_url = ''
        self.asms_maintainer = ''
        self.asms_platform = ''
        self.asms_firmware_version = ''

    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

    def log_line(self, line):
        self.logs.append(line)
        if len(self.logs) > MAX_LOG_LINES:
            self.logs.pop(0)

    def print_log(self):
        for line in self.logs:
            if len(line) > MAX_CHARS_PER_LOG_LINE:
                print(line[:MAX_CHARS_PER_LOG_LINE] + " [...CUT OFF...]")
            else:
                print(line)

    def asms_stb_list_apps(self):
        if len(self.asms_url) == 0:
            self.asms_reachable = False
            return []
        if self.asms_reachable is not None and not self.asms_reachable:
            return []

        print("Getting apps from ASMS ...")
        params = {
            'type': self.mimetype,
            'platform': 'arm:v7:linux'
        }
        self.log_line(Fore.LIGHTBLACK_EX + "SENDING:  " + self.asms_url + "/apps : "+ json.dumps(params))
        try:
            r = requests.get(self.asms_url + "/apps", params=params, timeout=3, auth=HTTPBasicAuth(ASMS_USERNAME, ASMS_PASSWORD))
            self.asms_reachable = True
        except requests.exceptions.RequestException:
            self.asms_reachable = False
            return []

        if r.status_code == 401:
            print(Fore.LIGHTRED_EX + "Not authorized to access ASMS, please set correct ASMS_USERNAME and ASMS_PASSWORD")
            exit(-2)

        self.log_line(Fore.LIGHTBLACK_EX + "RECEIVED: " + json.dumps(r.json()))
        apps = r.json()['applications']
        apps.sort(key=lambda x: x['id'])

        return apps

    def asms_stb_app_details(self, id, version):
        params = {
            'platformName': self.asms_platform,
            'firmwareVer': self.asms_firmware_version
        }
        self.log_line(Fore.LIGHTBLACK_EX + "SENDING:  " + self.asms_url + "/apps/" + requests.utils.quote(
            id + ":" + version) + " : " + json.dumps(params))
        r = requests.get(self.asms_url + "/apps/" + requests.utils.quote(id + ":" + version), params=params, auth=HTTPBasicAuth(ASMS_USERNAME, ASMS_PASSWORD))
        self.log_line(Fore.LIGHTBLACK_EX + "RECEIVED: " + json.dumps(r.json()))
        return r.json()

    def asms_stb_app_url(self, id, version):
        return self.asms_stb_app_details(id, version)['header']['url']

    def asms_maintainer_delete_app(self, id, version):
        self.log_line(Fore.LIGHTBLACK_EX + "SENDING:  DELETE " + self.asms_url + "/maintainers/" + requests.utils.quote(
            self.asms_maintainer) + "/apps/" + requests.utils.quote(id + ":" + version))
        r = requests.delete(
            self.asms_url + "/maintainers/" + requests.utils.quote(
                self.asms_maintainer) + "/apps/" + requests.utils.quote(id + ":" + version), auth=HTTPBasicAuth(ASMS_USERNAME, ASMS_PASSWORD))
        self.log_line(Fore.LIGHTBLACK_EX + "RECEIVED: " + str(r.status_code) + " " + r.text)

    def asms_maintainer_create_app(self):
        id = input("id -> ")
        if id == "":
            print(Fore.RED + "Bad input")
            time.sleep(1)
            return
        name = input("name (default 'some app') -> ")
        if name == "":
            name = "some app"
        version = input("version (default '1.0.0') -> ")
        if version == "":
            version = "1.0.0"
        ociImageUrl = input("ociImageUrl (default 'docker://public.ecr.aws/a0v6o9z7/chocolate-doom:latest') -> ")
        if ociImageUrl == "":
            ociImageUrl = "docker://public.ecr.aws/a0v6o9z7/chocolate-doom:latest"
        icon = input("icon (default 'https://upload.wikimedia.org/wikipedia/en/5/57/Doom_cover_art.jpg') -> ")
        if icon == "":
            icon = "https://upload.wikimedia.org/wikipedia/en/5/57/Doom_cover_art.jpg"
        encryption = input("encryption (default false) -> ")
        if encryption.lower() == 't' or encryption.lower() == 'y' or encryption.lower() == 'true' or encryption == '1':
            encryption = True
        else:
            encryption = False

        body = {
            "header": {
                "icon": icon,
                "name": name,
                "description": name,
                "type": self.mimetype,
                "size": 13000000,
                "category": "application",
                "id": id,
                "version": version,
                "visible": True,
                "encryption": encryption,
                "ociImageUrl": ociImageUrl
            },
            "requirements": {
                "platform": {
                    "architecture": "arm",
                    "variant": "v7",
                    "os": "linux"
                },
                "hardware": {
                    "ram": "512M",
                    "dmips": "2000",
                    "persistent": "10M",
                    "cache": "200M"
                }
            },
            "maintainer": {
                "code": self.asms_maintainer
            },
            "versions": [
                {
                    "version": version,
                    "visible": True
                }
            ]
        }
        self.log_line(Fore.LIGHTBLACK_EX + "SENDING:  POST " + self.asms_url + "/maintainers/" + requests.utils.quote(
            self.asms_maintainer) + "/apps : " + json.dumps(body))
        r = requests.post(self.asms_url + "/maintainers/" + requests.utils.quote(self.asms_maintainer) + "/apps",
                          json=body, auth=HTTPBasicAuth(ASMS_USERNAME, ASMS_PASSWORD))
        self.log_line(Fore.LIGHTBLACK_EX + "RECEIVED: " + str(r.status_code) + " " + r.text)

    def do_wscmd(self, ws, cmd, log=True, throwonerror=False):
        cmd['id'] = random.randint(1, 1000000)
        cmd['jsonrpc'] = "2.0"
        cmdstring = json.dumps(cmd)
        if log:
            self.log_line(Fore.LIGHTBLACK_EX + "SENDING:  " + cmdstring)
        ws.send(cmdstring)
        result_string = result = ws.recv()
        if log:
            self.log_line(Fore.LIGHTBLACK_EX + "RECEIVED: " + result)
        result = json.loads(result)
        if 'id' not in result or result['id'] != cmd['id']:
            print(Fore.RED + "Bad reqid when waiting for ws result")
            return None
        elif 'error' in result and throwonerror:
            raise Exception('Error: '+ json.dumps(result['error']))
        elif 'error' in result:
            # in case of LISA.1.getProgress, an error is expected at the end, so ignore in that case
            if cmd['method'] != 'LISA.1.getProgress':
                self.log_line(Fore.LIGHTRED_EX + "RECEIVED: " + result_string)
        elif 'result' not in result:
            return None
        else:
            return result['result']

    def lisa_list_installed_apps(self):
        result = self.do_wscmd(self.ws_thunder, {"method": "LISA.1.getList"}, log=False)
        return result['apps'] if result and 'apps' in result else []

    def lisa_get_metadata_app(self, mimetype, id, version):
        result = self.do_wscmd(self.ws_thunder, {"method": "LISA.1.getMetadata", "params":
            {"id": id, "type": mimetype, "version": version}}, log=True)
        return result['auxMetadata'] if result and 'auxMetadata' in result else []

    def lisa_get_dac_config(self):
        result = self.do_wscmd(self.ws_thunder, {"method": "LISA.1.getMetadata", "params":
            {"id": "lisa.dac.config", "type": "application/LISA", "version": "0"}}, log=False)
        data = result['auxMetadata'] if result and 'auxMetadata' in result else []
        dacBundlePlatformNameOverride = None
        dacBundleFirmwareCompatibilityKey = None
        asmsUrl = None
        for entry in data:
            if entry["key"] == "dacBundlePlatformNameOverride":
                dacBundlePlatformNameOverride = entry["value"]
            elif entry["key"] == "dacBundleFirmwareCompatibilityKey":
                dacBundleFirmwareCompatibilityKey = entry["value"]
            elif entry["key"] == "asmsUrl":
                asmsUrl = entry["value"]
        return dacBundlePlatformNameOverride, dacBundleFirmwareCompatibilityKey, asmsUrl

    def lisa_progress(self, handle):
        cmd = {'method': 'LISA.1.getProgress', 'params': {'handle': handle}}
        return self.do_wscmd(self.ws_thunder, cmd, False)

    def lisa_install_app(self, id, version, name, url):
        cmd = {'method': 'LISA.1.install', 'params': {
            'id': id,
            'type': self.mimetype,
            'version': version,
            'url': url,
            'appName': name,
            'category': 'cat',
        }}
        self.lisa_do_operation_and_wait_on_progress(cmd)

    def lisa_install_app_manual(self):
        id = input("id -> ")
        if id == "":
            print(Fore.RED + "Bad input")
            time.sleep(1)
            return
        name = input("name (default 'some app') -> ")
        if name == "":
            name = "some app"
        version = input("version (default '1.0.0') -> ")
        if version == "":
            version = "1.0.0"
        url = input("url -> ")
        if url == "":
            print(Fore.RED + "Bad input")
            time.sleep(1)
            return
        cmd = {'method': 'LISA.1.install', 'params': {
            'id': id,
            'type': self.mimetype,
            'version': version,
            'url': url,
            'appName': name,
            'category': 'cat',
        }}
        self.lisa_do_operation_and_wait_on_progress(cmd)

    def lisa_uninstall_app(self, id, version):
        uninstallType = input("FULL (F) or  UPGRADE(U)?  (default F) -> ").upper()
        if uninstallType == "":
            uninstallType = "F"
        if uninstallType != "F" and uninstallType != "U":
            print(Fore.RED + "Bad input")
            time.sleep(1)
            return
        cmd = {'method': 'LISA.1.uninstall', 'params': {
            'id': id,
            'type': self.mimetype,
            'version': version,
            'uninstallType': ('full' if uninstallType == 'F' else 'upgrade'),
        }}
        self.lisa_do_operation_and_wait_on_progress(cmd)

    def lisa_uninstall_app_orphan(self, id):
        # when previously an "upgrade" uninstall was done, the data dir of the dac app
        # remains + some records in the DB
        # this happens to facilitate the upgrade of an app: afterwards you can install the
        # new version and then it has retained its persisted data
        # the function below is meant to remove this "orphaned" data dir + DB record, in case
        # you want to clean it up
        cmd = {"method": "LISA.1.uninstall", "params": {"id": id, "type": self.mimetype, "uninstallType": "full"}}
        self.lisa_do_operation_and_wait_on_progress(cmd)

    def lisa_do_operation_and_wait_on_progress(self, cmd):
        handle = self.do_wscmd(self.ws_thunder, cmd)
        if handle != "":
            progress = self.lisa_progress(handle)
            while progress is not None:
                print("--> %d%%" % progress)
                time.sleep(0.5)
                progress = self.lisa_progress(handle)

    def start_app(self, id, version):
        if self.ws_awc:
            self.awc_start_app(id)
            print(Fore.LIGHTYELLOW_EX + "Attempted start, waiting a bit before opacity+focus...")
            time.sleep(5)
            self.awc_opac_app(id)
            self.awc_focus_app(id)
        else:
            self.rdkshell_start_app(id, version)
            print(Fore.LIGHTYELLOW_EX + "Attempted start, waiting a bit before focus...")
            time.sleep(3)
            self.rdkshell_setvisibility_app(RESIDENT_APP_ID, False)
            self.rdkshell_movefront_app(id)
            self.rdkshell_focus_app(id)

    def stop_app(self, id):
        if self.ws_awc:
            self.awc_stop_app(id)
        else:
            self.rdkshell_stop_app(id)
            self.rdkshell_setvisibility_app(RESIDENT_APP_ID, True)
            self.rdkshell_focus_app(RESIDENT_APP_ID)

    def running_apps_info(self):
        if self.ws_awc:
            apps = []
            running_apps = self.awc_apps_info()
            for running_app in running_apps:
                appstate = running_app['appState'] if 'appState' in running_app else "No"
                app = {
                    'id': running_app['appId'],
                    'version': running_app['appVersion'],
                    'running': True if appstate == 'Started' else False
                }
                apps.append(app)
            return apps
        else:
            apps = []
            running_apps = self.rdkshell_apps_info()
            for running_app_id in running_apps:
                app = {
                    'id': running_app_id,
                    'version': '',
                    'running': True
                }
                apps.append(app)
            return apps

    # ONEMW ApplicationManager AWC functions #####
    def awc_start_app(self, id):
        cmd = {'method': 'com.libertyglobal.rdk.awc.1.start',
               'params': {'appId': id, 'appMimeType': self.mimetype}}
        result = self.do_wscmd(self.ws_awc, cmd)
        return result

    def awc_opac_app(self, id):
        cmd = {'method': 'com.libertyglobal.rdk.awc.1.setOpacity',
               'params': {'appId': id, 'opacity': 1.0}}
        result = self.do_wscmd(self.ws_awc, cmd)
        return result

    def awc_focus_app(self, id):
        cmd = {'method': 'com.libertyglobal.rdk.awc.1.setFocus',
               'params': {'appId': id}}
        result = self.do_wscmd(self.ws_awc, cmd)
        return result

    def awc_stop_app(self, id):
        cmd = {'method': 'com.libertyglobal.rdk.awc.1.stop',
               'params': {'appId': id, 'reason': 2}}
        result = self.do_wscmd(self.ws_awc, cmd)
        return result

    def awc_apps_info(self):
        result = self.do_wscmd(self.ws_awc, {"method": "com.libertyglobal.rdk.awc.1.getApplicationsInfo"}, log=False)
        return result['appInfo'] if 'appInfo' in result else []

    # RDKShell ApplicationManager functions
    def rdkshell_start_app(self, id, version):
        cmd = {'method': 'org.rdk.RDKShell.1.launchApplication',
               'params': {'client': id, 'mimeType': self.mimetype, 'uri': f'{id};{version};{self.mimetype}'}}
        result = self.do_wscmd(self.ws_thunder, cmd)
        return result

    def rdkshell_stop_app(self, id):
        cmd = {'method': 'org.rdk.RDKShell.1.kill', 'params': {'client': id}}
        result = self.do_wscmd(self.ws_thunder, cmd)
        return result

    def rdkshell_movefront_app(self, id):
        cmd = {'method': 'org.rdk.RDKShell.1.moveToFront',
               'params': {'client': id}}
        result = self.do_wscmd(self.ws_thunder, cmd)
        return result

    def rdkshell_focus_app(self, id):
        cmd = {'method': 'org.rdk.RDKShell.1.setFocus',
               'params': {'client': id}}
        result = self.do_wscmd(self.ws_thunder, cmd)
        return result

    def rdkshell_setvisibility_app(self, id, visible):
        cmd = {'method': 'org.rdk.RDKShell.1.setVisibility',
               'params': {'client': id, 'visible': visible}}
        result = self.do_wscmd(self.ws_thunder, cmd)
        return result

    def rdkshell_apps_info(self):
        result = self.do_wscmd(self.ws_thunder, {"method": "org.rdk.RDKShell.1.getClients"}, log=True)
        return result['clients'] if result and 'clients' in result else []

    def detect_rdkshell(self):
        result = self.do_wscmd(self.ws_thunder, {'method': 'Controller.1.status'}, log=False)
        if not result:
            return False
        for item in result:
            if item.get('callsign') == "org.rdk.RDKShell":
                return True
        return False

    @staticmethod
    def which_app(apps, cmd):
        if len(cmd) <= 1:
            return None
        try:
            idx = int(cmd[1:])
        except (TypeError, ValueError):
            print(Fore.RED + "Bad input")
            return None
        if not 0 <= idx < len(apps):
            print(Fore.RED + "Bad input")
            return None
        return apps[idx]

    def print_menu(self, apps):
        self.clear()
        if self.asms_reachable:
            print(
                Fore.LIGHTYELLOW_EX + f"PLATFORM {Fore.LIGHTBLUE_EX}{self.asms_platform}{Fore.LIGHTYELLOW_EX} - FIRMWARE {Fore.LIGHTBLUE_EX}{self.asms_firmware_version}{Fore.LIGHTYELLOW_EX}")
        err_asms = (Fore.LIGHTRED_EX + "!! ASMS NOT REACHABLE !!") if not self.asms_reachable else ""
        mode = Fore.LIGHTYELLOW_EX + "Mode " + Fore.LIGHTBLUE_EX + (
            "ONEMW (AWC) " if self.ws_awc else "RDK (RDKShell) ") + Fore.LIGHTYELLOW_EX
        print(Fore.LIGHTYELLOW_EX + f"{mode}Apps (A=ASMS app, I=installed, R=running, O=orphan) {err_asms} : ")
        cnt = 0
        for app in apps:
            prefix = ("A" if app['asms'] else ".")
            prefix += ("I" if app['installed'] else ".")
            prefix += ("R" if app['running'] else ".")
            prefix += ("O" if app['orphan'] else ".")
            prefix += " "
            print(
                prefix + str(cnt).ljust(3) + " : " + (app['id'] + " " + app['version']).ljust(40) + " = " + app['name'])
            cnt += 1

        self.print_log()
        print(
            Fore.LIGHTYELLOW_EX + "R  : refresh               " + Fore.LIGHTRED_EX + " Q  : quit     " + Fore.LIGHTBLUE_EX +
            "C : clear log")
        install_from_asms = ""
        if self.asms_reachable:
            print(Fore.LIGHTYELLOW_EX + f"A  : add new app to ASMS    Dx : remove app x from ASMS")
            install_from_asms = "Ix : install app from ASMS  "
        print(Fore.LIGHTYELLOW_EX + f"{install_from_asms}X : install from URL        Ux : uninstall app from STB")
        print(Fore.LIGHTYELLOW_EX + f"Sx : start app on STB       Tx : stop app on STB        Mx : metadata of app")
        return input("Your wish? --> ").upper()

    def get_apps(self):
        apps = self.asms_stb_list_apps()
        for app in apps:
            app['installed'] = False
            app['running'] = False
            app['asms'] = True
            app['orphan'] = False

        installed_apps = self.lisa_list_installed_apps()
        for app in installed_apps:
            found = False
            if 'installed' in app:
                for asms_app in apps:
                    if asms_app['id'] == app['id']:
                        for installed_version in app['installed']:
                            if installed_version['version'] == asms_app['version']:
                                asms_app['installed'] = True
                                found = True
                                break
                if not found:
                    for installed_version in app['installed']:
                        new_app = {'id': app['id'], 'version': installed_version['version'],
                                   'name': installed_version['appName'], 'installed': True, 'asms': False,
                                   'running': False, 'orphan': False}
                        apps.append(new_app)
            else:
                new_app = {'id': app['id'], 'version': '',
                           'name': '', 'installed': False, 'asms': False, 'running': False,
                           'orphan': True}
                apps.append(new_app)

        running_apps = self.running_apps_info()
        for running_app in running_apps:
            for app in apps:
                if running_app['id'] == app['id'] and (running_app['version'] == app['version']
                                                       or running_app['version'] == ''):
                    app['running'] = running_app['running']
                    break

        return sorted(apps, key=lambda x: (x['orphan'], not x['installed'], x['id']))

    def run(self):
        init(autoreset=True)

        print("Trying to connect to STB at " + self.stb_ip)
        print(Fore.LIGHTRED_EX + "Make sure box listens to thunder and awc ws ports and allows it (iptables)")
        print("Connecting to Thunder " + self.ws_thunder + " ...")
        self.ws_thunder = websocket.create_connection(self.ws_thunder)
        if not self.detect_rdkshell():
            print("Did not detect RDKShell. Connecting to AWC " + self.ws_awc + " ...")
            self.ws_awc = websocket.create_connection(self.ws_awc)
            self.mimetype = MIMETYPE_ONEMW
            self.asms_url = ASMS_URL_ONEMW
            self.asms_maintainer = ASMS_MAINTAINER_ONEMW
            self.asms_platform = ASMS_PLATFORM if len(ASMS_PLATFORM) > 0 else DEFAULT_ASMS_PLATFORM_ONEMW
            self.asms_firmware_version = ASMS_FIRMWARE if len(ASMS_FIRMWARE) > 0 else DEFAULT_ASMS_FIRMWARE_ONEMW
        else:
            print("Detected RDKShell!")
            self.mimetype = MIMETYPE_RDK
            self.asms_url = ASMS_URL_RDK
            self.asms_maintainer = ASMS_MAINTAINER_RDK
            self.asms_platform = ASMS_PLATFORM if len(ASMS_PLATFORM) > 0 else DEFAULT_ASMS_PLATFORM_RDK
            self.asms_firmware_version = ASMS_FIRMWARE if len(ASMS_FIRMWARE) > 0 else DEFAULT_ASMS_FIRMWARE_RDK
            self.ws_awc = None

        if not SKIP_AUTO_DETECT_DAC_CONFIG:
            dacBundlePlatformNameOverride, dacBundleFirmwareCompatibilityKey, asmsUrl = self.lisa_get_dac_config()
            if dacBundlePlatformNameOverride:
                self.asms_platform = dacBundlePlatformNameOverride
                print("ASMS_PLATFORM is overriden by LISA: " + Fore.LIGHTRED_EX + self.asms_platform)
            if dacBundleFirmwareCompatibilityKey:
                self.asms_firmware_version = dacBundleFirmwareCompatibilityKey
                print("ASMS_FIRMWARE is overriden by LISA: " + Fore.LIGHTRED_EX + self.asms_firmware_version)
            if asmsUrl:
                self.asms_url = asmsUrl
                print("ASMS_URL is overriden by LISA: " + Fore.LIGHTRED_EX + self.asms_url)

        time.sleep(2)
        while True:
            apps = self.get_apps()
            cmd = self.print_menu(apps)
            app = self.which_app(apps, cmd)

            if cmd == "R" or cmd == "":
                continue
            elif cmd == "Q":
                print(Fore.LIGHTYELLOW_EX + "See you later...")
                exit(0)
            elif cmd[0] == "D" and app:
                self.asms_maintainer_delete_app(app['id'], app['version'])
            elif cmd[0] == "I" and app and app['asms'] and not app['installed']:
                self.lisa_install_app(app['id'], app['version'], app['name'], self.asms_stb_app_url(app['id'], app['version']))
            elif cmd[0] == "X":
                self.lisa_install_app_manual()
            elif cmd[0] == "S" and app and app['installed'] and not app['running']:
                self.start_app(app['id'], app['version'])
            elif cmd[0] == "T" and app and app['running']:
                self.stop_app(app['id'])
            elif cmd[0] == "U" and app and app['installed']:
                self.lisa_uninstall_app(app['id'], app['version'])
            elif cmd[0] == "U" and app and app['orphan']:
                self.lisa_uninstall_app_orphan(app['id'])
            elif cmd == "A":
                self.asms_maintainer_create_app()
            elif cmd[0] == "M" and app:
                metadata = self.lisa_get_metadata_app(self.mimetype, app['id'], app['version'])
                for x in metadata:
                    print(Fore.LIGHTMAGENTA_EX + x['key'] + " = " + x['value'])
                if len(metadata) == 0:
                    print(Fore.LIGHTRED_EX + "No metadata present...")
                input("Press [ENTER] to continue...")
            elif cmd == "C":
                self.logs.clear()
            else:
                print(Fore.LIGHTYELLOW_EX + "Pardon?")
                time.sleep(1)


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print(Fore.LIGHTYELLOW_EX + "Usage: ")
        print(Fore.LIGHTYELLOW_EX + "test.py stb_ipaddress")
        exit(0)
    tool = DacTool(sys.argv[1])
    tool.run()
