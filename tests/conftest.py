#!/usr/bin/env python3
'''
*
* conftest.py
*
* Copyright (c) 2025 Iocane Pty Ltd
*
* @author: Jason Piszcyk
* 
* Testing Config
*
'''
import pytest
import time

from src.application_status.web_server import start_web_server, stop_web_server
from tests.web_request import Web_Request


###########################################################################
#
# Config
#
###########################################################################
def pytest_configure(config):
    pytest.web_request = Web_Request()


###########################################################################
#
# Fixtures
#
###########################################################################
#
# init_test
#
# @pytest.fixture(autouse=True)
# def init_test():
#     pytest.api_request.reset()


#
# new_request
#
@pytest.fixture(scope="function")
def new_request():
    _webserver = start_web_server()

    # Give the web server a chance to start
    time. sleep(1)

    yield pytest.web_request
    stop_web_server(thread=_webserver, timeout=15)
    # stop_web_server()
