#!/usr/bin/env python3
'''
*
* test_webserver.py
*
* Copyright (c) 2025 Iocane Pty Ltd
*
* @author: Jason Piszcyk
* 
* Specific tests for webserver
*
'''
# System Imports
import pytest
from pytest import web_request
from src.application_status.application_status import Status

#
# Globals
#
BASE_URI="http://127.0.0.1:8180/"


###########################################################################
#
# The tests...
#
###########################################################################
#
# Status
#
class TestWebServer():
    #
    # Invalid methods
    #
    def test_invalid_methods_root_path(self, new_request):
        # / - GET is allowed
        new_request.standard_invalid_method_test(uri=f"{BASE_URI}", valid_methods=["get"])

    def test_invalid_methods_any_path(self, new_request):
        # Nothing is allowed
        new_request.standard_invalid_method_test(uri=f"{BASE_URI}any", valid_methods=[])



    #
    # Valid Requests
    #
    def test_valid(self, new_request):
        _var_name = "webvalue"
        _var_string = "web string"

        # Create a value
        Status.set_static(name=_var_name, value=_var_string)
        assert Status.get(name=_var_name) == _var_string

        # Get the value via the web interface
        _req = new_request.get(uri=f"{BASE_URI}")

        # Validate the response
        assert _req
        assert _var_name in _req
        assert _req[_var_name] == _var_string
