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


class CallResult:
    def __init__(self, result):
        self.result = result

    def expectResult(self):
        assert self.value('result') is not None
        return self

    def expectError(self):
        assert self.value('error') is not None
        return self

    def expectValue(self, value_name, value):
        curr_val = self.value(value_name)
        assert curr_val == value, "expected value for '" + value_name + "': '" + str(value) + "' got '" + str(curr_val) + "'"
        return self

    def getJson(self):
        return self.result

    def value(self, name=''):
        r = self.result
        if name != '':
            ln = name.split('.')
            while (len(ln) > 0) and (ln[0] in r):
                r = r[ln[0]]
                ln = ln[1:]

            assert len(ln) == 0, "key: '" + ln[0] + "' not found"
        return r


def call(ws, obj, *args, **kwargs):
    result = obj.call(ws, *args, **kwargs)
    cresult = CallResult(result)
    return cresult
