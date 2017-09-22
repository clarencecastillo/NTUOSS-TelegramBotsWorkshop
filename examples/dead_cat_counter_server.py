#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer

dead_cats = 0

class DeadCatCounterServer(BaseHTTPRequestHandler):

    def do_GET(self):
        global dead_cats
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        message = "OK"
        if (self.path == '/kitty'):
            dead_cats += 1
        elif (self.path == '/dead_cats'):
            message = str(dead_cats)
        self.wfile.write(bytes(message, "utf8"))
        return


print('starting server...')
server_address = ('127.0.0.1', 8081)
httpd = HTTPServer(server_address, DeadCatCounterServer)
print('running server...')
httpd.serve_forever()
