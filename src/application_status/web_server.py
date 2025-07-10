#!/usr/bin/env python3
'''
* web_server.py
*
* Copyright (c) 2025 Jason Piszcyk
*
* @author: Jason Piszcyk
* 
* Application Status Info
*
'''
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

from .application_status import Status


#
# Constants
#


###########################################################################
#
# BasicWebServer Class
#
###########################################################################
class BasicWebServer(BaseHTTPRequestHandler):
    '''
    A very basic web server to return the status information
    '''
    def do_GET(self):
        '''
        Perform the get action

        Parameters:
            None

        Return Value:
            None
        '''
        # Only allow request to the root path
        if self.path != "/":
            self.send_response(405)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            return

        # Create the response
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(Status.export(), "utf-8"))


###########################################################################
#
# Web Server control
#
###########################################################################
#
# run_web_server
#
def run_web_server(hostname="localhost", port=8180):
    '''
    Run the web server (call from start_web_server)

    Parameters:
        hostname: The hostname/ip address for the server
        port: The port to listen on

    Return Value:
        None
    '''
    Status.webserver = HTTPServer((hostname, port), BasicWebServer)

    try:
        Status.webserver.serve_forever()
    except KeyboardInterrupt:
        pass

    Status.webserver.server_close()



#
# start_web_server
#
def start_web_server(hostname="localhost", port=8180, threaded=True):
    '''
    Start the web server (threaded if required)

    Parameters:
        hostname: The hostname/ip address for the server
        port: The port to listen on
        threaded: If true, start a new thread to run the web server

    Return Value:
        Process: The process running the web server. None if not forked.
    '''
    # See if we need to start a new thread
    if threaded:
        Status.webserver_thread = Thread(target=run_web_server,
                kwargs={ "hostname": hostname, "port": port })
        Status.webserver_thread.start()

    else:
        Status.webserver_thread = None
        run_web_server(hostname=hostname, port=port)

    return Status.webserver_thread


#
# stop_web_server
#
def stop_web_server(thread=None, timeout=60):
    '''
    Stop the web server (if run in a thread)

    Parameters:
        thread: The thread that was started to run the web server

    Return Value:
        none
    '''
    if not thread: thread = Status.webserver_thread
    if timeout < 0: timeout = 0
    if timeout > 600: timeout = 600

    # Try to end the web server
    Status.webserver.shutdown()

    # Join and close the process to clean it up
    thread.join(timeout=timeout)
    Status.webserver = None
    Status.webserver_thread = None


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

