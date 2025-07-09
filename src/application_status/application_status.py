#!/usr/bin/env python3
'''
* application_status.py
*
* Copyright (c) 2025 Jason Piszcyk
*
* @author: Jason Piszcyk
* 
* Application Status Info
*
'''
from threading import Lock


#
# Constants
#


###########################################################################
#
# ApplicationStatus Class
#
###########################################################################
#
# ApplicationConfig
#
class ApplicationStatus():
    ''' Application Status '''
    # Private Class Attributes
    __lock = Lock()
    __status_dict = {}


    #
    # __init__
    #
    def __init__(self, *args, **kwargs):
        ''' Init method for class '''
        super().__init__(*args, **kwargs)


    ###########################################################################
    #
    # Helper/Convenience Functions
    #
    ###########################################################################
    #
    # _valid_entry_type
    #
    @staticmethod
    def _valid_entry_type(entry=None):
        '''
        Check the entry is a type we can handle correctly

        Parameters:
            entry: The entry

        Return Value:
            boolean: True if successful, false otherwise
        '''
        # Simple lookup of type
        if not entry: return True
        if isinstance(entry, str): return True
        if isinstance(entry, int): return True
        if isinstance(entry, float): return True
        if isinstance(entry, bool): return True
        if isinstance(entry, list): return True
        if isinstance(entry, tuple): return True

        # Not supported
        return False


    #
    # _set_entry_from_dot
    #
    def _set_entry_from_dot(self, name=None, value=None):
        '''
        Set the entry based on a dot name

        Parameters:
            name: The entry name
            value: The value for the entry

        Return Value:
            bool: True if successful, false otherwise
        '''
        assert name

        if not self._valid_entry_type(entry=value):
            raise ValueError(f"Values of type: {type(value)} are not supported") 

        _entry = self.__status_dict

        _tmp_name = ""
        _part = name
        while _part:
            # Split the name
            (_part, _, _rest) = _part.partition(".")
            tmp_name = f"{_tmp_name}.{_part}"

            if not _part in _entry:
                if not _rest:
                    # This is the entry to add the value to
                    self.__lock.acquire()
                    _entry[_part] = value
                    self.__lock.release()
                    _part = None

                else:
                    # Create a nested dict (as there is more to the dot path)
                    self.__lock.acquire()
                    _entry[_part] = {}
                    self.__lock.release()
                    _entry = _entry[_part]

            else:
                if not _rest:
                    # Make sure this is not a dict and then add the entry
                    if isinstance(_entry[_part], dict):
                        raise ValueError(f"Name has sub entries: {tmp_name}")

                    self.__lock.acquire()
                    _entry[_part] = value
                    self.__lock.release()
                    _part = None

                else:
                    if not isinstance(_entry[_part], dict):
                        raise ValueError(f"Invalid nesting of values under: {tmp_name}")

        # Return the entry
        return True


    #
    # _get_entry_from_dot
    #
    def _get_entry_from_dot(self, name=None):
        '''
        Get the entry based on a dot name

        Parameters:
            name: The entry name

        Return Value:
            value: The entry being requested
        '''
        assert name

        _entry = self.__status_dict
        _value = None

        _tmp_name = name
        while _tmp_name:
            # Split the name
            (_part, _, _rest) = _tmp_name.partition(".")

            # Is the name in the status dict?
            if _part in _entry:
                _entry = _entry[_part]
            else:
                break

            if _rest:
                _tmp_name = _rest
            else:
                # This should be the value
                _value = _entry
                _tmp_name = None

        # Return the entry
        return _value


    ###########################################################################
    #
    # Manage status info
    #
    ###########################################################################
    #
    # set_static
    #
    def set_static(self, name="", value=None):
        '''
        Set a static entry in the dict (won't be updated automatically)

        Parameters:
            name: The entry name (dot format)
            value: The value for the entry

        Return Value:
            boolean: True if successful, false otherwise (exception will be raised)
        '''
        return self._set_entry_from_dot(name=name, value=value)


    #
    # set
    #
    def set(self, name="", func=None, update=600):
        '''
        Set an entry in the dict

        Parameters:
            name: The entry name (dot format)
            func: The function to run to get the value for the entry
            update: How often to run the function

        Return Value:
            boolean: True if successful, false otherwise (exception will be raised)
        '''
        assert name
        assert func
        assert callable(func)
        assert update > 0

        _value = func()
        return self._set_entry_from_dot(name=name, value=_value)


    #
    # get
    #
    def get(self, name="", default=None):
        '''
        Get entry in the status dict

        Parameters:
            name: The entry name (dot format)
            default: A default value to use if not found

        Return Value:
            value: The value in the entry
        '''
        assert name

        _entry_value = self._get_entry_from_dot(name=name)
        if not _entry_value:
            _entry_value = default
        
        return _entry_value


###########################################################################
#
# Define the instance - Can be imported wherever needed:
#   from application_status import Status
#
###########################################################################
Status = ApplicationStatus()


###########################################################################
#
# In case this is run directly rather than imported...
#
###########################################################################
'''
Handle case of being run directly rather than imported
'''
if __name__ == "__main__":
    pass

