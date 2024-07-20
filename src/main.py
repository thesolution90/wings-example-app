'''
Test Applikation für die Integration von GitLab mit Trello
'''
import http.server
import socketserver
from http import HTTPStatus
import threading


class Handler(http.server.SimpleHTTPRequestHandler):
    '''
    Logik innerhalb des Get Requests
    '''
    def do_GET(self):
        self.send_response(HTTPStatus.OK)
        self.end_headers()
        self.wfile.write(b'Hello world!')


class ServerThread(threading.Thread):
    '''
    Hier ist der Webserver definiert
    '''
    def __init__(self):
        super().__init__()
        self.server = socketserver.TCPServer(('localhost', 5000), Handler)

    def run(self):
        '''Starten des Webservers'''
        self.server.serve_forever()

    def shutdown(self):
        '''Stoppen des Servers'''
        self.server.shutdown()

# Starten des Webservers
if __name__ == '__main__':
    httpd = socketserver.TCPServer(('', 5000), Handler)
    httpd.serve_forever()
