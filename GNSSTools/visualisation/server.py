# Tampere University of Technology
#
# DESCRIPTION
# Launches the localhost server
#
# AUTHOR
# Yannick DEFRANCE


#!/usr/bin/python3

import http.server

def serve_forever(hostname='', port=8888):
    """

    :param hostname:
    :param port:
    :return:
    """

    server_address = (hostname, port)
    server = http.server.HTTPServer
    handler = http.server.CGIHTTPRequestHandler
    handler.cgi_directories = ["/"]
    print("Serving files at port "+ str(port))

    httpd = server(server_address, handler)
    httpd.serve_forever()


if __name__ == '__main__' :
    PORT = 8888
    server_address = ("", PORT)
    serve_forever('', PORT)


