from socketserver import ThreadingMixIn
from http.server import HTTPServer
import logging

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True
    
    def __init__(self, server_address, RequestHandlerClass):
        super().__init__(server_address, RequestHandlerClass)
        logging.info(f"Servidor threadado iniciado em {server_address}")