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

#
# Globals
#
BASE_URI="http://127.0.0.1:8180"


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
        new_request.standard_invalid_method_test(uri=f"{BASE_URI}/", valid_methods=["get"])

    def test_invalid_methods_any_path(self, new_request):
        # Nothing is allowed
        new_request.standard_invalid_method_test(uri=f"{BASE_URI}/any", valid_methods=[])



    #
    # Valid Requests
    #
    # def test_valid(self, api_session):
    #     # Access the method
    #     _req = api_session.get(uri=f"{api_session.BASE_URI}/{API_ENDPOINT}")

    #     # Validate the response
    #     assert _req
    #     assert "rows" in _req

    #     # Look for the login endpoint
    #     _found_endpoint = False
    #     for _entry in _req['rows']:
    #         assert "endpoint" in _entry
    #         if _entry['endpoint'] == "login":
    #             _found_endpoint = True

    #     # Ensure the endpoint was found
    #     assert _found_endpoint

