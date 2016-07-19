__author__ = 'defrance'


#!/usr/bin/python3

import http.server

PORT = 8888
server_address = ("", PORT)

server = http.server.HTTPServer
handler = http.server.CGIHTTPRequestHandler
handler.cgi_directories = ["/"]
print(("Serving files at port :", PORT))

httpd = server(server_address, handler)
httpd.serve_forever()
