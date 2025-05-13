import sys
import os
import logging
import argparse
from pathlib import Path
from http.server import HTTPServer

# Configuração crucial de paths
sys.path.append(str(Path(__file__).parent.parent))

# Agora importe os módulos locais
from server.dispatcher import RequestDispatcher
from server.threads import ThreadedHTTPServer
from server.file_handler import FileHandler

def configure_logging():
    """Configura o sistema de logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('server.log')
        ]
    )

def run_server(host: str = 'localhost', port: int = 8000):
    configure_logging()
    
    # Configuração absoluta dos caminhos
    base_dir = os.path.dirname(os.path.abspath(__file__))
    RequestDispatcher.file_handler = FileHandler(os.path.join(base_dir, 'master.txt'))
    RequestDispatcher.users_file = os.path.join(base_dir, 'users.json')
    
    server = ThreadedHTTPServer((host, port), RequestDispatcher)
    
    logging.info(f"Servidor iniciado em http://{host}:{port}")
    logging.info(f"Master file: {os.path.join(base_dir, 'master.txt')}")
    logging.info(f"Users file: {os.path.join(base_dir, 'users.json')}")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info("Servidor encerrado")
        server.server_close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Servidor RMI')
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    
    run_server(args.host, args.port)