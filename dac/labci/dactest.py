#!/usr/bin/env python3
#
# Copyright (c) 2023, Liberty Global Service B.V. all rights reserved.
#
# required deps: pip3 install requests colorama websocket-client
import sys, os
import json
import random
import time
import requests  # pip3 install requests
from colorama import Fore, Back, Style, init  # pip3 install colorama
from websocket import create_connection  # pip3 install websocket-client

ASMS = "http://appstore-metadata-service.labci.ecx.appdev.io"
MIMETYPE = "application/vnd.rdk-app.dac.native"

# 2008C-STB
#   yocto 3.1 - with /tmp/rialto-0 path:
#     FIRMWARE = "0.1.1-00b7e2b8621a78adc2f1845abafdd89c2969e189-dbg"
#   yocto 3.1 - with /var/run/rialto/{id} path:
#     FIRMWARE = "0.1.2-3dc2c997ea95ccf4107acc4e4526d4e3fed7b4e4-dbg"

#
# VIP7002W
#   yocto 3.1 - with /tmp/rialto-0 path:
#     FIRMWARE = "0.1.1-2ca0e8774ba96c08b78b621afe5991dd4a397e1b-dbg"
#   yocto 3.1 - with /var/run/rialto/{id} path:
#     FIRMWARE = "0.1.2-911ef4b6f2833999b15cbd3255d468dcf0e15e63-dbg"

PLATFORM = "VIP7002W"
FIRMWARE = "0.1.1-2ca0e8774ba96c08b78b621afe5991dd4a397e1b-dbg"


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def log_line(line):
    global logs
    logs.append(line)
    if len(logs) > 10:
        logs.pop(0)


def print_log():
    global logs
    for line in logs:
        print(line)


def asms_stb_list_apps():
    global asms_reachable

    if 'asms_reachable' in globals() and not asms_reachable:
        return []

    print("Getting apps from ASMS ...")
    params = {
        'type': MIMETYPE,
        'platform': 'arm:v7:linux'
    }
    # log_line(Fore.LIGHTBLACK_EX + "SENDING:  " + ASMS + "/apps : "+ json.dumps(params))
    try:
        r = requests.get(ASMS + "/apps", params=params, timeout=3)
        asms_reachable = True
    except:
        asms_reachable = False
        return []

    # log_line(Fore.LIGHTBLACK_EX + "RECEIVED: " + json.dumps(r.json()))
    apps = r.json()['applications']
    apps.sort(key=lambda x: x['id'])

    return apps


def asms_stb_app_details(id, version):
    params = {
        'platformName': PLATFORM,
        'firmwareVer': FIRMWARE
    }
    log_line(Fore.LIGHTBLACK_EX + "SENDING:  " + ASMS + "/apps/" + requests.utils.quote(
        id + ":" + version) + " : " + json.dumps(params))
    r = requests.get(ASMS + "/apps/" + requests.utils.quote(id + ":" + version), params=params)
    log_line(Fore.LIGHTBLACK_EX + "RECEIVED: " + json.dumps(r.json()))
    return r.json()


def asms_stb_app_url(id, version):
    return asms_stb_app_details(id, version)['header']['url']


def asms_maintainer_delete_app(id, version):
    log_line(Fore.LIGHTBLACK_EX + "SENDING:  DELETE " + ASMS + "/maintainers/" + requests.utils.quote(
        "lgi-dac") + "/apps/" + requests.utils.quote(id + ":" + version))
    r = requests.delete(
        ASMS + "/maintainers/" + requests.utils.quote("lgi-dac") + "/apps/" + requests.utils.quote(id + ":" + version))
    log_line(Fore.LIGHTBLACK_EX + "RECEIVED: " + str(r.status_code) + " " + r.text)


def asms_maintainer_create_app():
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
    ociImageUrl = input("ociImageUrl (default 'docker://registry.lgi.io/dac/doom:latest') -> ")
    if ociImageUrl == "":
        ociImageUrl = "docker://registry.lgi.io/dac/doom:latest"

    body = {
        "header": {
            "icon": "https://www.chocolate-doom.org/wiki/images/7/77/Chocolate-logo.png",
            "name": name,
            "description": name,
            "type": MIMETYPE,
            "size": 13000000,
            "category": "application",
            "id": id,
            "version": version,
            "visible": True,
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
            "code": "lgi-dac",
            "name": "Liberty Global",
            "address": "Liberty Global B.V., Boeing Avenue 53, 1119 PE Schiphol Rijk, The Netherlands",
            "homepage": "https://www.libertyglobal.com",
            "email": "sverkoyen.contractor@libertyglobal.com"
        },
        "versions": [
            {
                "version": version,
                "visible": True
            }
        ]
    }
    log_line(Fore.LIGHTBLACK_EX + "SENDING:  POST " + ASMS + "/maintainers/" + requests.utils.quote(
        "lgi-dac") + "/apps : " + json.dumps(body))
    r = requests.post(ASMS + "/maintainers/" + requests.utils.quote("lgi-dac") + "/apps", json=body)
    log_line(Fore.LIGHTBLACK_EX + "RECEIVED: " + str(r.status_code) + " " + r.text)


def do_wscmd(ws, cmd, log=True):
    cmd['id'] = random.randint(1, 1000000)
    cmd['jsonrpc'] = "2.0"
    cmdstring = json.dumps(cmd)
    if log:
        log_line(Fore.LIGHTBLACK_EX + "SENDING:  " + cmdstring)
    ws.send(cmdstring)
    result = ws.recv()
    if log:
        log_line(Fore.LIGHTBLACK_EX + "RECEIVED: " + result)
    result = json.loads(result)
    if 'id' not in result or result['id'] != cmd['id']:
        print(Fore.RED + "Bad reqid when waiting for ws result")
        return None
    if 'result' not in result:
        return None
    else:
        return result['result']


def lisa_list_installed_apps(ws_thunder):
    result = do_wscmd(ws_thunder, {"method": "LISA.1.getList"}, log=False)
    return result['apps'] if 'apps' in result else []


def lisa_get_metadata_app(ws_thunder, id, version):
    result = do_wscmd(ws_thunder, {"method": "LISA.1.getMetadata", "params":
        {"id": id, "type": MIMETYPE, "version": version}}, log=True)
    return result['auxMetadata'] if 'auxMetadata' in result else []


def lisa_progress(ws_thunder, handle):
    cmd = {"method": "LISA.1.getProgress", "params":
        {"handle": handle}
           }
    return do_wscmd(ws_thunder, cmd, False)


def lisa_install_app(ws_thunder, id, version, url):
    ## fix the url
    # url = url.replace("rdk-tarballs-binary-storage.s3.eu-central-1.amazonaws.com", "appstore-caching-service.labci.ecx.appdev.io")
    # url = url.replace("rdk-tarballs-binary-storage.s3.eu-central-1.amazonaws.com", "localhost:81/common-service/appstore-caching-service")
    ## fix the _ -> -
    # url = url.replace("_","-")

    cmd = {"method": "LISA.1.install", "params":
        {"id": id, "type": MIMETYPE, "version": version,
         "url": url, "appName": "name", "category": "cat"
         }
           }
    handle = do_wscmd(ws_thunder, cmd)
    if handle != "":
        progress = lisa_progress(ws_thunder, handle)
        while progress != None:
            print("--> %d%%" % progress)
            time.sleep(0.5)
            progress = lisa_progress(ws_thunder, handle)


def lisa_install_app_manual(ws_thunder):
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
    cmd = {"method": "LISA.1.install", "params":
        {"id": id, "type": MIMETYPE, "version": version,
         "url": url, "appName": name, "category": "cat"
         }
           }
    handle = do_wscmd(ws_thunder, cmd)
    if handle != "":
        progress = lisa_progress(ws_thunder, handle)
        while progress is not None:
            print("--> %d%%" % progress)
            time.sleep(0.5)
            progress = lisa_progress(ws_thunder, handle)


def lisa_uninstall_app(ws_thunder, id, version):
    uninstallType = input("FULL (F) or  UPGRADE(U)? -> ").upper()
    if uninstallType != "F" and uninstallType != "U":
        print(Fore.RED + "Bad input")
        time.sleep(1)
        return
    cmd = {"method": "LISA.1.uninstall", "params":
        {"id": id, "type": MIMETYPE, "version": version,
         "uninstallType": ("full" if uninstallType == "F" else "upgrade")}
           }
    handle = do_wscmd(ws_thunder, cmd)
    if handle != "":
        progress = lisa_progress(ws_thunder, handle)
        while progress is not None:
            print("--> %d%%" % progress)
            time.sleep(0.5)
            progress = lisa_progress(ws_thunder, handle)


def lisa_uninstall_app_orphan(ws_thunder, id):
    # when previously an "upgrade" uninstall was done, the data dir of the dac app
    # remains + some records in the DB
    # this happens to facilitate the upgrade of an app: afterwards you can install the
    # new version and then it has retained its persisted data
    # the function below is meant to remove this "orphaned" data dir + DB record, in case
    # you want to clean it up
    cmd = {"method": "LISA.1.uninstall", "params": {"id": id, "type": MIMETYPE, "uninstallType": "full"}}
    handle = do_wscmd(ws_thunder, cmd)
    if handle != "":
        progress = lisa_progress(ws_thunder, handle)
        while progress is not None:
            print("--> %d%%" % progress)
            time.sleep(0.5)
            progress = lisa_progress(ws_thunder, handle)

def awc_start_app(ws_awc, id):
    cmd = {"method": "com.libertyglobal.rdk.awc.1.start", "params":
        {"appId": id, "appMimeType": MIMETYPE}
           }
    result = do_wscmd(ws_awc, cmd)
    return result


def awc_opac_app(ws_awc, id):
    cmd = {"method": "com.libertyglobal.rdk.awc.1.setOpacity", "params":
        {"appId": id, "opacity": 1.0}
           }
    result = do_wscmd(ws_awc, cmd)
    return result


def awc_focus_app(ws_awc, id):
    cmd = {"method": "com.libertyglobal.rdk.awc.1.setFocus", "params":
        {"appId": id}
           }
    result = do_wscmd(ws_awc, cmd)
    return result


def awc_stop_app(ws_awc, id):
    cmd = {"method": "com.libertyglobal.rdk.awc.1.stop", "params":
        {"appId": id, "reason": 2}
           }
    result = do_wscmd(ws_awc, cmd)
    return result


def awc_apps_info(ws_awc):
    result = do_wscmd(ws_awc, {"method": "com.libertyglobal.rdk.awc.1.getApplicationsInfo"}, log=False)
    return result['appInfo'] if 'appInfo' in result else []


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


def print_menu(apps):
    global asms_reachable
    clear()
    if asms_reachable:
        print(Fore.LIGHTYELLOW_EX + f"PLATFORM {Fore.LIGHTBLUE_EX}{PLATFORM}{Fore.LIGHTYELLOW_EX} - FIRMWARE {Fore.LIGHTBLUE_EX}{FIRMWARE}{Fore.LIGHTYELLOW_EX}")
    err_asms = (Fore.LIGHTRED_EX + "!! ASMS NOT REACHABLE !!") if not asms_reachable else ""
    print(Fore.LIGHTYELLOW_EX + f"Apps (A=ASMS app, I=installed, R=running, O=orphan) {err_asms} : ")
    cnt = 0
    for app in apps:
        prefix = ("A" if app['asms'] else ".")
        prefix += ("I" if app['installed'] else ".")
        prefix += ("R" if app['running'] else ".")
        prefix += ("O" if app['orphan'] else ".")
        prefix += " "
        print(prefix + str(cnt).ljust(3) + " : " + (app['id'] + " " + app['version']).ljust(40) + " = " + app['name'])
        cnt += 1

    print_log()
    print(
        Fore.LIGHTYELLOW_EX + "R  : refresh               " + Fore.LIGHTRED_EX + " Q  : quit     " + Fore.LIGHTBLUE_EX +
        "C : clear log")
    install_from_asms = ""
    if asms_reachable:
        print(Fore.LIGHTYELLOW_EX + f"A  : add new app to ASMS    Dx : remove app x from ASMS")
        install_from_asms = "Ix : install app from ASMS  "
    print(Fore.LIGHTYELLOW_EX + f"{install_from_asms}X : install from URL        Ux : uninstall app from STB")
    print(Fore.LIGHTYELLOW_EX + f"Sx : start app on STB       Tx : stop app on STB        Mx : metadata of app")
    return input("Your wish? --> ").upper()


def get_apps():
    global ws_awc, ws_thunder
    apps = asms_stb_list_apps()
    for app in apps:
        app['installed'] = False
        app['running'] = False
        app['asms'] = True
        app['orphan'] = False

    installed_apps = lisa_list_installed_apps(ws_thunder)
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
                               'name': installed_version['appName'], 'installed': True, 'asms': False, 'running': False, 'orphan': False}
                    apps.append(new_app)
        else:
            new_app = {'id': app['id'], 'version': '',
                       'name': '', 'installed': False, 'asms': False, 'running': False,
                       'orphan': True}
            apps.append(new_app)

    running_apps = awc_apps_info(ws_awc)
    for running_app in running_apps:
        for app in apps:
            if running_app['appId'] == app['id'] and running_app['appVersion'] == app['version']:
                appstate = running_app['appState'] if 'appState' in running_app else "No"
                app['running'] = True if appstate == 'Started' else False
                break

    return sorted(apps, key=lambda x: (x['orphan'], not x['installed'], x['id']))


def main():
    global ws_awc, ws_thunder, logs
    init(autoreset=True)
    if len(sys.argv) <= 1:
        print(Fore.LIGHTYELLOW_EX + "Usage: ")
        print(Fore.LIGHTYELLOW_EX + "test.py stb_ipaddress")
        exit(0)
    stb_ip = sys.argv[1]
    logs = []
    ws_thunder = "ws://" + stb_ip + ":9998/jsonrpc"
    ws_awc = "ws://" + stb_ip + ":8083"

    print("Trying to connect to STB at " + stb_ip)
    print(Fore.LIGHTRED_EX + "Make sure box listens to thunder and awc ws ports and allows it (iptables)")
    print("Connecting to Thunder " + ws_thunder + " ...")
    ws_thunder = create_connection(ws_thunder)
    print("Connecting to AWC " + ws_awc + " ...")
    ws_awc = create_connection(ws_awc)

    while True:
        apps = get_apps()

        cmd = print_menu(apps)
        app = which_app(apps, cmd)

        if cmd == "R" or cmd == "":
            continue
        elif cmd == "Q":
            print(Fore.LIGHTYELLOW_EX + "See you later...")
            exit(0)
        elif cmd[0] == "D" and app:
            asms_maintainer_delete_app(app['id'], app['version'])
        elif cmd[0] == "I" and app and app['asms'] and not app['installed']:
            lisa_install_app(ws_thunder, app['id'], app['version'], asms_stb_app_url(app['id'], app['version']))
        elif cmd[0] == "X":
            lisa_install_app_manual(ws_thunder)
        elif cmd[0] == "S" and app and app['installed'] and not app['running']:
            awc_start_app(ws_awc, app['id'])
            print(Fore.LIGHTYELLOW_EX + "Attempted start, waiting a bit before opacity+focus...")
            time.sleep(5)
            awc_opac_app(ws_awc, app['id'])
            awc_focus_app(ws_awc, app['id'])
        elif cmd[0] == "T" and app and app['running']:
            awc_stop_app(ws_awc, app['id'])
        elif cmd[0] == "U" and app and app['installed']:
            lisa_uninstall_app(ws_thunder, app['id'], app['version'])
        elif cmd[0] == "U" and app and app['orphan']:
            lisa_uninstall_app_orphan(ws_thunder, app['id'])
        elif cmd == "A":
            asms_maintainer_create_app()
        elif cmd[0] == "M" and app:
            metadata = lisa_get_metadata_app(ws_thunder, app['id'], app['version'])
            for x in metadata:
                print(Fore.LIGHTMAGENTA_EX + x['key'] + " = " + x['value'])
            if len(metadata) == 0:
                print(Fore.LIGHTRED_EX + "No metadata present...")
            input("Press [ENTER] to continue...")
        elif cmd == "C":
            logs.clear()
        else:
            print(Fore.LIGHTYELLOW_EX + "Pardon?")
            time.sleep(1)


if __name__ == "__main__":
    main()
