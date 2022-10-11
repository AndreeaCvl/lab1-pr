import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import time
import random


# port for the server
hostName = "localhost"
serverPort = 8080

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
        self.send_response(200)
        self.end_headers()

        # receiving data via POST request from another server
        length = int(self.headers.get('Content-length', 0))
        data = json.loads(self.rfile.read(length).decode())

        received = data['int']
        print(received)


# function for producing random numbers
def produce():
    global headers
    global params

    # generating the numbers and sending them to the consumer server
    while True:
        data = {'int': random.randint(0, 1000)}
        requests.post("http://localhost:8081", headers=headers, params=params, json=data)
        time.sleep(3)


# creating 6 producer threads
producer_threads = [threading.Thread(target=produce) for i in range(6)]

# runner code
if __name__ == "__main__":

    # starting the threads
    for thread in producer_threads:
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
