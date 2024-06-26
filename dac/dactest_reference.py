#!/usr/bin/env python3
#
# Copyright (c) 2023, LIBERTY GLOBAL all rights reserved.
#
# pip3 install colorama websocket-client
import json
import os
import random
import sys
import time

from colorama import Fore, init
from websocket import create_connection

# LGI ONEMW uses "application/vnd.rdk-app.dac.native"
# but RDKShell,Rdkservices, Refapp use "application/dac.native""
# see here https://github.com/rdkcentral/RDKShell/blob/611b68c488bd8f34d4f358781c83d09472b42128/application.h#L25
MIMETYPE = "application/dac.native"
RESIDENT_APP_ID = "residentapp"


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
    result = do_wscmd(ws_thunder, {"method": "LISA.1.getList", "params":
        {"type": MIMETYPE}}, log=True)
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


def lisa_install_app(ws_thunder):
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
    if not version:
        lisa_uninstall_app_orphan(ws_thunder, id)
        return

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


def is_app_installed(id, version, installed_apps):
    for app in installed_apps:
        if app['id'] == id:
            for installed_app in app['installed']:
                if installed_app['version'] == version:
                    return True
    return False


def is_app_running(id, rdkshell_apps):
    for appid in rdkshell_apps:
        if appid == id:
            return True
    return False


def rdkshell_start_app(ws_thunder, id, version):
    cmd = {"method": "org.rdk.RDKShell.1.launchApplication", "params":
        {"client": id, "mimeType": "application/dac.native", "uri": id + ";" + version + ";" + MIMETYPE}
           }
    result = do_wscmd(ws_thunder, cmd)
    return result


def rdkshell_stop_app(ws_thunder, id):
    cmd = {"method": "org.rdk.RDKShell.1.kill", "params":
        {"client": id}
           }
    result = do_wscmd(ws_thunder, cmd)
    return result


def rdkshell_movefront_app(ws_thunder, id):
    cmd = {"method": "org.rdk.RDKShell.1.moveToFront", "params":
        {"client": id}
           }
    result = do_wscmd(ws_thunder, cmd)
    return result


def rdkshell_focus_app(ws_thunder, id):
    cmd = {"method": "org.rdk.RDKShell.1.setFocus", "params":
        {"client": id}
           }
    result = do_wscmd(ws_thunder, cmd)
    return result

def rdkshell_setvisibility_app(ws_thunder, id, visible):
    cmd = {"method": "org.rdk.RDKShell.1.setVisibility", "params":
        {"client": id, "visible": visible}
           }
    result = do_wscmd(ws_thunder, cmd)
    return result


def rdkshell_apps_info(ws_thunder):
    result = do_wscmd(ws_thunder, {"method": "org.rdk.RDKShell.1.getClients"}, log=True)
    return result['clients'] if 'clients' in result else []


def which_app(apps, cmd):
    if len(cmd) <= 1:
        return {}
    try:
        idx = int(cmd[1:])
    except:
        print(Fore.RED + "Bad input")
        return {}
    if idx < 0 or idx >= len(apps):
        print(Fore.RED + "Bad input")
        return {}
    return apps[idx]


def print_menu(apps, rdkshell_apps):
    clear()
    print(Fore.LIGHTYELLOW_EX + "Installed apps (!=running, O=orphan) : ")
    cnt = 0
    for app in apps:
        id = app['id']
        installed_app = {}
        if 'installed' in app:
            installed_apps = app['installed']
            if len(installed_apps) > 0:
                installed_app = installed_apps[0]
        version = installed_app['version'] if 'version' in installed_app else ""
        name = installed_app['appName'] if 'appName' in installed_app else ""
        prefix = ("!" if is_app_running(id, rdkshell_apps) else " ")
        prefix += (" " if version else "O")
        print(prefix + " " + str(cnt).ljust(3) + " : " + (id + " " + version).ljust(40) + " = " + name)
        cnt += 1
    print_log()
    print(
        Fore.LIGHTYELLOW_EX + "R  : refresh               " + Fore.LIGHTRED_EX + "Q  : quit     " + Fore.LIGHTBLUE_EX + "C : clear log")
    print(Fore.LIGHTYELLOW_EX + "I  : install app onto STB  Ux : uninstall app from STB")
    print(Fore.LIGHTYELLOW_EX + "Sx : start app on STB      Tx : stop app on STB        Mx : metadata of app")
    return input("Your wish? --> ").upper()


def main():
    global ws_thunder, logs
    init(autoreset=True)
    if len(sys.argv) <= 1:
        print(Fore.LIGHTYELLOW_EX + "Usage: ")
        print(Fore.LIGHTYELLOW_EX + "test.py stb_ipaddress")
        exit(0)
    stb_ip = sys.argv[1]
    logs = []
    ws_thunder = "ws://" + stb_ip + ":9998/jsonrpc"

    print("Trying to connect to STB at " + stb_ip)
    print(Fore.LIGHTRED_EX + "Make sure box listens to thunder port and allows it (iptables)")
    print("Connecting to Thunder " + ws_thunder + " ...")
    ws_thunder = create_connection(ws_thunder)

    while True:
        apps = lisa_list_installed_apps(ws_thunder)
        rdkshell_apps = rdkshell_apps_info(ws_thunder)

        cmd = print_menu(apps, rdkshell_apps)
        app = which_app(apps, cmd)

        id = app['id'] if 'id' in app else ""
        installed_app = {}
        if 'installed' in app:
            installed_apps = app['installed']
            if len(installed_apps) > 0:
                installed_app = installed_apps[0]
        version = installed_app['version'] if 'version' in installed_app else ""

        if cmd == "R" or cmd == "":
            continue
        elif cmd == "Q":
            print(Fore.LIGHTYELLOW_EX + "See you later...")
            exit(0)
        elif cmd == "I":
            lisa_install_app(ws_thunder)
        elif cmd[0] == "S" and id:
            rdkshell_start_app(ws_thunder, id, version)
            print(Fore.LIGHTYELLOW_EX + "Attempted start, waiting a bit before focus...")
            time.sleep(3)
            rdkshell_setvisibility_app(ws_thunder, RESIDENT_APP_ID, False)
            rdkshell_movefront_app(ws_thunder, id)
            rdkshell_focus_app(ws_thunder, id)
        elif cmd[0] == "T" and id:
            rdkshell_stop_app(ws_thunder, id)
            rdkshell_setvisibility_app(ws_thunder, RESIDENT_APP_ID, True)
            rdkshell_focus_app(ws_thunder, RESIDENT_APP_ID)
        elif cmd[0] == "U" and id:
            lisa_uninstall_app(ws_thunder, id, version)
        elif cmd[0] == "M" and app:
            metadata = lisa_get_metadata_app(ws_thunder, id, version)
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
