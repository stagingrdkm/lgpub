# One Middleware WS API Test Suite

## Introduction

This test suite covering Thunder Framework (aka Metrological WPEFramework) and plugins.



## Installation

1. Clone the test suite to your local setup.
```
git clone ssh://git@bitbucket.upc.biz:7999/onemt/wsapi-test-scripts.git
cd ./wsapi-test-scripts/
```

2. Install docker:
```
sudo apt-get install docker
```

3. Build docker image
```
docker build -t test_framework .
```

4. Run docker container
```
docker run -it test_framework /bin/bash
```

5. Configure tests in dockek containter
```
cd /test_framework/UnitTests/
vim ./thunder_config.json       <- Thunder plugins flags
```

6. Run tests in dockek containter
```
python3.6 ./test_thunder_wsapi.py <CPE IP address> /test_framework/UnitTests/thunder_config.json
```
