# Tampere University of Technology
#
# DESCRIPTION
# Launches the localhost server
#
# AUTHOR
# Yannick DEFRANCE


#!/usr/bin/python3

import http.server

if __name__ == __main__ :
    PORT = 8888
    server_address = ("", PORT)

    server = http.server.HTTPServer
    handler = http.server.CGIHTTPRequestHandler
    handler.cgi_directories = ["/"]
    print(("Serving files at port :", PORT))

    httpd = server(server_address, handler)
    httpd.serve_forever()
