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
import unittest

from UnitTests.test_thunder_controller_wsapi import *
from UnitTests.test_thunder_device_info_plugin import *
from UnitTests.test_thunder_display_info_plugin import *
from UnitTests.test_thunder_monitor_plugin import *
from UnitTests.test_thunder_ocdm_plugin import *
from UnitTests.test_thunder_oci_container_plugin import *
from UnitTests.test_thunder_player_info_plugin import *
from UnitTests.test_thunder_security_agent_plugin import *
from UnitTests.test_thunder_trace_control_plugin import *
from UnitTests.test_thunder_fmp_plugin import *
from UnitTests.test_thunder_webkitbrowser_plugin import *


if __name__ == "__main__":
    SUITE = unittest.TestSuite()
    loader = unittest.TestLoader()


    SUITE.addTest(loader.loadTestsFromTestCase(TestThunderControllerWSAPI))
    SUITE.addTest(loader.loadTestsFromTestCase(TestThunderDeviceInfoWSAPI))
#    SUITE.addTest(loader.loadTestsFromTestCase(TestThunderDisplayInfoWSAPI))
    SUITE.addTest(loader.loadTestsFromTestCase(TestThunderMonitorWSAPI))
#    SUITE.addTest(loader.loadTestsFromTestCase(TestThunderOcdmWSAPI))
#    SUITE.addTest(loader.loadTestsFromTestCase(TestThunderOciWSAPI))
#    SUITE.addTest(loader.loadTestsFromTestCase(TestThunderPlayerInfoWSAPI))
#    SUITE.addTest(loader.loadTestsFromTestCase(TestThunderSecurityAgentWSAPI))
    SUITE.addTest(loader.loadTestsFromTestCase(TestThunderTraceControlWSAPI))
#    SUITE.addTest(loader.loadTestsFromTestCase(TestThunderFmpWSAPI))
    SUITE.addTest(loader.loadTestsFromTestCase(TestThunderWebKitBrowserWSAPI))
    RESULT = unittest.TextTestRunner(verbosity=2).run(SUITE)
