# Mobile Apps Automation Framework
Python based automation framework for performing automation for various mobile applications.


### Introduction

* This is a Python 3 based automation framework for performing automation for various mobile applications.
* The framework uses a data-driven design where configuration is read from YAML file which are specific to each application.
* Currently automation for the following device type is supported:
    - Android


### Sample usage

$ python run.py --app facebook


### Development

# Clone the git repo and follow the steps below on any linux machine.

    git clone https://github.com/icgowtham/py_appium.git
    cd py_appium

# Setup Python virtual environment (Note: One time setup)

    make setup-env
    source venv3/bin/activate


### Compliance

To validate compliance, complexity, etc:

    make compliance <code_path>


### TODO
* Add unit tests.
* Enhance code coverage.


### MORE INFO
* http://appium.io/docs/en/about-appium/appium-clients/
