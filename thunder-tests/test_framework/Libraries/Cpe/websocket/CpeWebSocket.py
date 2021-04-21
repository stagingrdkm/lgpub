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
import socket
import websocket
import time
import threading
import Libraries.Cpe.websocket.CallResult as CallResult

class CpeWebSocket:
    def __init__(self, ip_address, handler = None):
        try:
            self.ip_address = ip_address
            self.url = 'ws://' + self.ip_address
            self.handler = handler

            if "9998/jsonrpc" in self.url:
                self.conn = websocket.create_connection(self.url, subprotocols=["notification"], timeout=5)
            else:
                self.conn = websocket.create_connection(self.url, timeout=5)

            self.id = 0
            self._recv_loop_running = True
            self.mutex = threading.Lock()
            self._recv_thread = threading.Thread(target=self._recvLoop)
            self._recv_thread.setDaemon(True)
            self._recv_thread.start()
        except Exception as ex:
            raise RuntimeError("Error: while getting CpeWebSocket connection to " + self.url + " >>" + str(ex) +"<<")

    def _recvData(self, timeout, allow_timeout=False):
        resp = None
        try:
            self.conn.settimeout(timeout=timeout)
            resp = self.conn.recv()
        except websocket.WebSocketTimeoutException as ex:
            if allow_timeout is True:
                pass
            else:
                self.mutex.release()
                raise RuntimeError("Websocket data timed out: " + str(ex))
        except Exception as ex:
            self.mutex.release()
            raise RuntimeError("Websocket exception: " + str(ex))

        return resp

    def _recvLoop(self):
        while self._recv_loop_running:
            self.mutex.acquire()
            jsresp = self._recvData(timeout=1, allow_timeout=True)
            self.mutex.release()
            if jsresp is not None:
                resp = json.loads(jsresp)
#                print ('loop recv <- ws:('+ self.ip_address+ '):'+ str(resp))

                if 'method' in resp and self.handler is not None:
                    self.handler.handle(resp)

            time.sleep(1)

    def stopRecvLoop(self):
        if self._recv_loop_running:
            self._recv_loop_running = False
            self._recv_thread.join()

    def send(self, js, signalName=None, signalValidator=None, timeout=15):
        self.mutex.acquire()
        sent_id = self.id
        js['id'] = sent_id
        self.id += 1

        print ('send -> ws:('+self.ip_address+'):'+ str(js))
        msg = json.dumps(js, separators=(',', ':'))

        self.conn.send(msg)
        exp = time.time() + timeout

        response = None
        signalDone = True
        if signalName is not None:
            signalDone = False

        while True:
            jsresp = self._recvData(timeout=timeout)
            resp = json.loads(jsresp)

            print ('recv <- ws:('+self.ip_address+'):'+ str(resp))

            if 'method' in resp and self.handler is not None:
                self.handler.handle(resp)

            if 'id' in resp and resp['id'] == sent_id:
                response = resp
                if 'error' in resp:
                    break
                if signalDone:
                    break

            if signalName is not None and 'method' in resp and resp['method'] == signalName:
                if signalValidator is not None:
                    signalDone = signalValidator(resp)
                else:
                    signalDone = True

            if response is not None and signalDone:
                break

            if exp < time.time():
                print ('recv <- ws('+self.ip_address+'): Timeout reached')
                self.mutex.release()
                raise RuntimeError("Websocket data timed out")
        self.mutex.release()
        return response

    def call(self, obj, *args, **kwargs):
        call_result = ""
        call_result = CallResult.call(self, obj, *args, **kwargs)
        return call_result


    def close(self):
        self.stopRecvLoop()
        self.conn.close()
