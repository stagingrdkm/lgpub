/*
 * If not stated otherwise in this file or this component's LICENSE file the
 * following copyright and licenses apply:
 *
 * Copyright 2020 RDK Management
 *
 * Licensed under the Apache License, Version 2.0 (the License);
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
 */

// initialization:
var thunderJS
var platform

thunderJS = ThunderJS({
  host: '127.0.0.1',
  port: 50050,
  debug: true
})

async function retrievePlatformName() {
  if (platform == null) {
    platform = await getDeviceName()
    platform = platform.split('-')[0]

    if (platform == 'raspberrypi') {
      platform = 'rpi'
    } else if (platform == 'brcm972180hbc') {
      platform = '7218c'
    }
  }
  return platform
}

async function getDeviceName() {
  let result = null
  try {
    result = await thunderJS.DeviceInfo.systeminfo()
  } catch (error) {
    console.log('Error on systeminfo: ', error)
  }

  return result == null ? "unknown" : result.devicename
}

async function getDacAppInstallUrl(app) {
  await retrievePlatformName()

  let url = ''
  if (app === 'wayland-egl-test') {
    url = 'http://rdk-tarballs-binary-storage.s3.eu-central-1.amazonaws.com/com.libertyglobal.app.waylandegltest/3.2.1/rpi3/rdk2020Q4/com.libertyglobal.app.waylandegltest_3.2.1_arm_linux_rpi3_rdk2020Q4.tar.gz'
  } else if (app === 'you.i') {
    url = 'http://rdk-tarballs-binary-storage.s3.eu-central-1.amazonaws.com/com.libertyglobal.app.youi/1.2.3/rpi3/rdk2020Q4/com.libertyglobal.app.youi_1.2.3_arm_linux_rpi3_rdk2020Q4.tar.gz'
  } else if (app === 'flutter') {
    url = 'http://rdk-tarballs-binary-storage.s3.eu-central-1.amazonaws.com/com.libertyglobal.app.flutter/0.0.1/rpi3/rdk2020Q4/com.libertyglobal.app.flutter_0.0.1_arm_linux_rpi3_rdk2020Q4.tar.gz'
  }

  if (platform === '7218c') {
    // TODO: temporary hack
    url = url.replace(/rpi3/g, '7218c')
  }

  return url
}

function reboot() {
  log('Calling: Controller.harakiri')
  thunderJS.Controller.harakiri()
    .then(function(result) {
      log('Success', result)
    })
    .catch(function(error) {
      log('Error', error)
    })
}

function listApps() {
  log('Calling: listApps')
  thunderJS.Packager.getInstalled()
    .then(function(result) {
      log('Success', result)
    })
    .catch(function(error) {
      log('Error', error)
    })
}

async function installDacApp(app, lfs) {
  log('Calling: installDacApp '+app)
  thunderJS.Packager.install(
      { "pkgId": "pkg-"+app, "type": "DAC", "url": await getDacAppInstallUrl(app) } )
    .then(function(result) {
      log('Success', result)
    })
    .catch(function(error) {
      log('Error', error)
    })
}

function removeDacApp(app) {
  log('Calling: installDacApp '+app)
  thunderJS.Packager.remove(
      { "pkgId": "pkg-"+app } )
    .then(function(result) {
      log('Success', result)
    })
    .catch(function(error) {
      log('Error', error)
    })
}

function startDacApp(app) {
  log('Calling: startDacApp '+app)
  thunderJS["org.rdk.RDKShell"].launchApplication(
      { "client": app, "mimeType": "application/dac.native", "uri": "pkg-"+app } )
    .then(function(result) {
      log('Success', result)
    })
    .catch(function(error) {
      log('Error', error)
    })
}

function stopDacApp(app) {
  log('Calling: stopDacApp '+app)
  thunderJS["org.rdk.RDKShell"].kill(
      { "client": app } )
    .then(function(result) {
      log('Success', result)
    })
    .catch(function(error) {
      log('Error', error)
    })
}

function startWebApp() {
  log('Calling: startWebApp')
  thunderJS["org.rdk.RDKShell"].launch( 
      { "callsign": "WebTest", "uri": "http://www.google.com", "type": "HtmlApp"} )
    .then(function(result) {
      log('Success', result)
    })
    .catch(function(error) {
      log('Error', error)
    })
}

function stopWebApp() {
  log('Calling: stopWebApp')
  thunderJS["org.rdk.RDKShell"].destroy( 
      { "callsign": "WebTest" } )
    .then(function(result) {
      log('Success', result)
    })
    .catch(function(error) {
      log('Error', error)
    })
}

function log(msg, content) {
  var el = document.getElementById('log')
  var entry = '<p class="font-bold">' + msg + '</p>'

  if (content) {
    entry += '<pre class="border mt-4 mb-8 text-sm">' + JSON.stringify(content, null, 2) + '</pre>'
  }

  entry += '<hr class="border-b" />'

  el.innerHTML = entry
}
