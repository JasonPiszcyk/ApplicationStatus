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
import multiprocessing


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
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))


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
    _webserver = HTTPServer((hostname, port), BasicWebServer)
    print("Server started http://%s:%s" % (hostname, port))

    try:
        _webserver.serve_forever()
    except KeyboardInterrupt:
        pass

    _webserver.server_close()
    print("Server stopped.")



#
# start_web_server
#
def start_web_server(hostname="localhost", port=8180, forking=True):
    '''
    Start the web server (forking if required)

    Parameters:
        hostname: The hostname/ip address for the server
        port: The port to listen on
        forking: If true, fork a new process to run the web server

    Return Value:
        Process: The process running the web server. None if not forked.
    '''
    # See if we need to fork the server
    if forking:
        _webserver_process = multiprocessing.Process(
            target=run_web_server, kwargs={ "hostname": hostname, "port": port })
        _webserver_process.start()

    else:
        _webserver_process = None
        run_web_server(hostname=hostname, port=port)

    return _webserver_process


#
# stop_web_server
#
def stop_web_server(process=None, timeout=60):
    '''
    Stop the web server (if forked)

    Parameters:
        process: The process that was forked to run the web server

    Return Value:
        none
    '''
    if not process: return
    if timeout < 0: timeout = 0
    if timeout > 600: timeout = 600

    # Try to end the web server
    try:
        process.terminate()
    except:
        pass

    # Join and close the process to clean it up
    process.join(timeout=timeout)
    process.close()


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

