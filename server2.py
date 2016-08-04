__author__ = 'defrance'
import http.server

if __name__ == '__main__' :
    PORT = 8888
    server_address = ("", PORT)

    server = http.server.HTTPServer
    handler = http.server.CGIHTTPRequestHandler
    handler.cgi_directories = ["/"]
    print("Serving files at port "+ str(PORT))

    httpd = server(server_address, handler)
    httpd.serve_forever()
