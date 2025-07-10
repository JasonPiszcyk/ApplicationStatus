#!/usr/bin/env python3
'''
*
* test_appstatus.py
*
* Copyright (c) 2025 Iocane Pty Ltd
*
* @author: Jason Piszcyk
* 
* Specific tests for appstatus
*
'''
# System Imports
import pytest
from src.application_status.application_status import Status
import time

#
# Globals
#


###########################################################################
#
# The tests...
#
###########################################################################
#
# Status
#
class TestAppStatus():
    #
    # Basic Add of status entries
    #
    def test_basic_entries(self):
        _varstr = "A static variable in"

        for _name in ("staticVar", "nested.staticVar", "deeply.nested.staticVar"):
            assert Status.set_static(name=_name, value=f"{_varstr} {_name}")
            _value = Status.get(name=_name)
            assert _value == f"{_varstr} {_name}"


    #
    # Deletion of status entries
    #
    def test_delete_entries_subtree_false(self):
        _varstr = "A static variable in"

        for _name in ("deleteVar", "nested.deleteVar", "deeply.nested.deleteVar"):
            assert Status.set_static(name=_name, value=f"{_varstr} {_name}")
            _value = Status.get(name=_name)
            assert _value == f"{_varstr} {_name}"
            assert Status.delete(name=_name, subtree=False)
            _value = Status.get(name=_name)
            assert not _value 


    def test_delete_entries_subtree_true(self):
        _varstr = "A static variable in"

        for _name in ("deleteVar", "nested.deleteVar", "deeply.nested.deleteVar"):
            assert Status.set_static(name=_name, value=f"{_varstr} {_name}")
            _value = Status.get(name=_name)
            assert _value == f"{_varstr} {_name}"
            assert Status.delete(name=_name, subtree=True)
            _value = Status.get(name=_name)
            assert not _value 


    def test_delete_tree_subtree_false(self):
        _varstr = "A static variable in"

        # Create the nested entries
        for _name in ("nest1.level1.subtreeVar1", "nest1.level1.subtreeVar2", "nest1.level1.subtreeVar3",
                      "nest1.level2.subtreeVar1"):
            assert Status.set_static(name=_name, value=f"{_varstr} {_name}")
            _value = Status.get(name=_name)
            assert _value == f"{_varstr} {_name}"

        # Try to delete a node in hierarchy
        with pytest.raises(ValueError):
            Status.delete(name="nest1.level1", subtree=False)

    def test_delete_tree_subtree_true(self):
        _varstr = "A static variable in"

        # Create the nested entries
        for _name in ("nest1.level1.subtreeVar1", "nest1.level1.subtreeVar2", "nest1.level1.subtreeVar3",
                      "nest1.level2.subtreeVar1"):
            assert Status.set_static(name=_name, value=f"{_varstr} {_name}")
            _value = Status.get(name=_name)
            assert _value == f"{_varstr} {_name}"

        # Delete with subtree = True
        assert Status.delete(name="nest1.level1", subtree=True)
        assert not Status.get(name="nest1.level1")


    #
    # Invalid entries
    #
    def test_invalid_set_nested(self):
        _varstr = "A static variable in"

        assert Status.set_static(name="nested.value", value=f"{_varstr}")
        with pytest.raises(ValueError):
            Status.set_static(name="nested", value=f"{_varstr}")


    def test_invalid_add_nest_under_value(self):
        _varstr = "A static variable in"

        assert Status.set_static(name="nested2", value=f"{_varstr}")
        with pytest.raises(ValueError):
            Status.set_static(name="nested2.value", value=f"{_varstr}")


    #
    # Dynamic entries
    #
    def test_dynamic_entry(self):
        _wait_time = 2
        _var_name = "dynamicvalue"
        _var_string = "Dynamic Value"
        _var_string_change = "Something different"

        def update_string():
            return _var_string

        # Start the background update thread
        Status.start_updates()
        Status.set(name=_var_name, func=update_string, update=_wait_time)

        # Val should be set
        time.sleep(1)
        assert Status.get(name=_var_name) == _var_string

        # Change it
        Status.set_static(name=_var_name, value=_var_string_change)
        assert Status.get(name=_var_name) == _var_string_change

        # Wait for it to update and it should be back to original
        time.sleep(_wait_time + 1)
        assert Status.get(name=_var_name) == _var_string

        # Stop the background updates
        Status.stop_updates()
