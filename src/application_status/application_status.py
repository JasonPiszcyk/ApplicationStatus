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
from threading import Thread, Lock, Event
import schedule
import time
import json


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
    #
    # __init__
    #
    def __init__(self, *args, **kwargs):
        ''' Init method for class '''
        super().__init__(*args, **kwargs)

        # Private Instance Attributes
        self.__lock = Lock()
        self.__stop_running_jobs = Event()
        self.__status_dict = {}
        self.__job_dict = {}

        self.update_thread = None
        self.webserver_thread = None
        self.webserver = None
        self.join_timeout = 30


    ###########################################################################
    #
    # Functions to schedule updates to status
    #
    ###########################################################################
    #
    # run_thread
    #
    @staticmethod
    def run_thread(func=None):
        '''
        Run the scheduled job in a thread

        Parameters:
            None

        Return Value:
            None
        '''
        assert func
        assert callable(func)

        _thread = Thread(target=func)
        _thread.start()


    #
    # run_updates
    #
    def run_updates(self):
        '''
        Run the update functions

        Parameters:
            None

        Return Value:
            None
        '''
        while not self.__stop_running_jobs.is_set():
            # Run any pending scheduled tasks
            schedule.run_pending()
            time.sleep(1)


    #
    # start_updates
    #
    def start_updates(self):
        '''
        Create the process to keep running the update functions

        Parameters:
            None

        Return Value:
            Process: The process running the web server. None if not forked.
        '''
        # Don't start another process if one already running
        if self.update_thread: return self.update_thread

        self.__stop_running_jobs.clear()
        self.update_thread = Thread(target=self.run_updates)
        self.update_thread.start()

        return self.update_thread


    #
    # stop_updates
    #
    def stop_updates(self):
        '''
        Stop and clean up the update process

        Parameters:
            None

        Return Value:
            None
        '''
        if not self.update_thread: return
        if self.join_timeout < 0: self.join_timeout = 0
        if self.join_timeout > 600: self.join_timeout = 600

        # Try to end the update process
        try:
            self.__stop_running_jobs.set()
        except:
            pass

        # Join and close the process to clean it up
        self.update_thread.join(timeout=self.join_timeout)
        self.update_thread = None


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
        _rest = name
        while _rest:
            # Split the name
            (_part, _, _rest) = _rest.partition(".")
            _tmp_name = f"{_tmp_name}.{_part}" if _tmp_name else _part

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
                        raise ValueError(f"Name has sub entries: {_tmp_name}")

                    self.__lock.acquire()
                    _entry[_part] = value
                    self.__lock.release()
                    _part = None

                else:
                    if not isinstance(_entry[_part], dict):
                        raise ValueError(f"Invalid nesting of values under: {_tmp_name}")

                    _entry = _entry[_part]

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

        _rest = name
        while _rest:
            # Split the name
            (_part, _, _rest) = _rest.partition(".")

            # Is the name in the status dict?
            if _part in _entry:
                _entry = _entry[_part]
            else:
                break

            if not _rest:
                # This should be the value
                _value = _entry

        # Return the entry
        return _value


    #
    # _delete_entry_from_dot
    #
    def _delete_entry_from_dot(self, name=None, subtree=False):
        '''
        Delete the entry based on a dot name

        Parameters:
            name: The entry name
            subtree: If True, also delete any child entries

        Return Value:
            value: True if successful, false if not found (exception raised on error)
        '''
        assert name

        _entry = self.__status_dict

        _rest = name
        _tmp_name = ""
        while _rest:
            # Split the name
            (_part, _, _rest) = _rest.partition(".")
            _tmp_name = f"{_tmp_name}.{_part}" if _tmp_name else _part

            # Is the name in the status dict?
            if _part in _entry:
                if not _rest:
                    # This should be the value
                    if isinstance(_entry[_part], dict):
                        # This is a subtree - Can we delete?
                        if subtree:
                            # Delete all the subtree entries
                            _entries = list(_entry[_part].keys())
                            for _key in _entries:
                                _subname = f"{_tmp_name}.{_key}" if _tmp_name else _key
                                self._delete_entry_from_dot(name=_subname, subtree=subtree)

                        else:
                            raise ValueError(f"Cannot delete subtree: {name}")

                    else:
                        self.__lock.acquire()

                        # Remove any schedules
                        if name in self.__job_dict:
                            schedule.cancel_job(self.__job_dict[name])
                            del self.__job_dict[name]

                        # Delete the value
                        del _entry[_part]

                        self.__lock.release()

                else:
                    # Move on to the next part
                    _entry = _entry[_part]

            else:
                # Does not exist
                return False

        # Return the entry
        return True


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

        # Set update interval to max of 1 hour
        if update > 3600: update = 3600

        # Create the entry with an empty value 
        self._set_entry_from_dot(name=name, value=None)

        # Create a function to update the value
        def update_status_value():
            _value = func()
            self._set_entry_from_dot(name=name, value=_value)

        # Schedule the function to update the value
        _job = schedule.every(update).seconds.do(self.run_thread, update_status_value)
        _job.run()
        self.__lock.acquire()
        self.__job_dict[name] = _job
        self.__lock.release()


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


    #
    # delete
    #
    def delete(self, name="", subtree=False):
        '''
        Delete a status entry

        Parameters:
            name: The entry name (dot format)
            subtree: If True, also delete any child entries

        Return Value:
            value: The value in the entry
        '''
        assert name

        return self._delete_entry_from_dot(name=name, subtree=subtree)


    #
    # export
    #
    def export(self):
        '''
        Export the status in JSON format

        Parameters:
            None

        Return Value:
            string: The status in JSON format
        '''
        try:
            return json.dumps(self.__status_dict)
        except:
            return ""


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
