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


class OCICONTAINER_resumeContainer:
    method = "org.rdk.OCIContainer.1.resumeContainer"
    __doc__ = "Resume a previously paused container"

    def __init__(self, containerId):
        self.params = {}
        self.params["containerId"] = containerId

    def set(self, containerId):
        self.params = {}
        self.params["containerId"] = containerId
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method, "params": self.params}
        return ws.send(jsonobj, *args, **kwargs)


class OCICONTAINER_stopContainer:
    method = "org.rdk.OCIContainer.1.stopContainer"
    __doc__ = "Stop a currently running container"

    def __init__(self, containerId):
        self.params = {}
        self.params["containerId"] = containerId

    def set(self, containerId):
        self.params = {}
        self.params["containerId"] = containerId
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method, "params": self.params}
        return ws.send(jsonobj, *args, **kwargs)


class OCICONTAINER_executeCommand:
    method = "org.rdk.OCIContainer.1.executeCommand"
    __doc__ = "Execute a command inside a running container. The path to the executable must resolve within the container's namespace."

    def __init__(self, containerId, options, command ):
        self.params = {}
        self.params["containerId"] = containerId
        self.params["options"] = options
        self.params["command"] = command

    def set(self, containerId, options, command):
        self.params = {}
        self.params["containerId"] = containerId
        self.params["options"] = options
        self.params["command"] = command

        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method, "params": self.params}
        return ws.send(jsonobj, *args, **kwargs)


class OCICONTAINER_getContainerState:
    method = "org.rdk.OCIContainer.1.getContainerState"
    __doc__ = "Get the state of a currently running container."

    def __init__(self, containerId):
        self.params = {}
        self.params["containerId"] = containerId

    def set(self, containerId):
        self.params = {}
        self.params["containerId"] = containerId
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method, "params": self.params}
        return ws.send(jsonobj, *args, **kwargs)


class OCICONTAINER_startContainerFromDobbySpec:
    method = "org.rdk.OCIContainer.1.startContainerFromDobbySpec"
    __doc__ = "Starts a new container from a legacy Dobby json specification"

    def __init__(self, containerId, dobbySpec):
        self.params = {}
        self.params["containerId"] = containerId
        self.params["dobbySpec"] = dobbySpec

    def set(self, dobbySpec, containerId):
        self.params = {}
        self.params["containerId"] = containerId
        self.params["dobbySpec"] = dobbySpec

        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method, "params": self.params}
        return ws.send(jsonobj, *args, **kwargs)


class OCICONTAINER_listContainers:
    method = "org.rdk.OCIContainer.1.listContainers"
    __doc__ = "List all running OCI containers Dobby knows about."

    def __init__(self):
        self.params = {}

    def set(self):
        self.params = {}
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method}
        return ws.send(jsonobj, *args, **kwargs)


class OCICONTAINER_pauseContainer:
    method = "org.rdk.OCIContainer.1.pauseContainer"
    __doc__ = "Pause a currently running container"

    def __init__(self, containerId):
        self.params = {}
        self.params["containerId"] = containerId

    def set(self, containerId):
        self.params = {}
        self.params["containerId"] = containerId
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method, "params": self.params}
        return ws.send(jsonobj, *args, **kwargs)


class OCICONTAINER_getContainerInfo:
    method = "org.rdk.OCIContainer.1.getContainerInfo"
    __doc__ = "Gets information about a running container such as CPU, memory and GPU uage (GPU not supported on Xi6)"

    def __init__(self, containerId):
        self.params = {}
        self.params["containerId"] = containerId

    def set(self, containerId):
        self.params = {}
        self.params["containerId"] = containerId
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method, "params": self.params}
        return ws.send(jsonobj, *args, **kwargs)


class OCICONTAINER_startContainer:
    method = "org.rdk.OCIContainer.1.startContainer"
    __doc__ = "Starts a new container from an existing OCI bundle."

    def __init__(self, containerId, bundlePath):
        self.params = {}
        self.params["containerId"] = containerId
        self.params["bundlePath"] = bundlePath

    def set(self, containerId, bundlePath):
        self.params = {}
        self.params["containerId"] = containerId
        self.params["bundlePath"] = bundlePath
        return self

    def call(self, ws, *args, **kwargs):
        jsonobj = {"jsonrpc": "2.0", "id": 0, "method": self.method, "params": self.params}
        return ws.send(jsonobj, *args, **kwargs)
