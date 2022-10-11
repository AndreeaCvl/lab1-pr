# important imports
import json
import math
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import time

# port for the server
hostName = "localhost"
serverPort = 8081

# empty queue which will store received data
queue = []

# parameters for transmitting / receiving the data
headers = {'Content-Type': 'application/json'}
params = {'access_token': "params"}


# class MyServer which implements some http methods
class MyServer(BaseHTTPRequestHandler):

    # implements method for GET requests
    def do_GET(self):
        self.send_response(200)
        self.end_headers()

    # implements method for POST requests
    def do_POST(self):

        global queue

        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()

        # receiving data via POST request from another server
        length = int(self.headers.get('Content-length', 0))
        data = json.loads(self.rfile.read(length).decode())

        # adding the received element to a queue
        queue.append(data['int'])


# function which extracts the last element of the queue then sends it back to the producer server
def extract():
    global queue
    global headers
    global params

    while True:
        if len(queue) > 0:
            last = queue.pop()
            requests.post("http://localhost:8080", headers=headers, params=params, json={'int': math.sqrt(last)})
            time.sleep(3)
        else:
            # continue
            time.sleep(3)

        # printing the queue
        print(queue)


# initializing 3 extractor threads, with function extract as target
extractor_threads = [threading.Thread(target=extract) for i in range(3)]

# runner code
if __name__ == "__main__":

    # starting the threads
    for thread in extractor_threads:
        thread.start()

    # starting the web server
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
