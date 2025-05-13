import sys
import os
from pathlib import Path

# Adiciona o diretório raiz do projeto ao PYTHONPATH
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)
    
from http.server import HTTPServer
from dispatcher import RequestDispatcher
from threads import ThreadedHTTPServer
import argparse
import logging

def configure_logging():
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
    

    RequestDispatcher.file_handler = logging.FileHandler('master.txt')
    RequestDispatcher.users_file = os.path.join(os.path.dirname(__file__), 'users.json')
    server = ThreadedHTTPServer((host, port), RequestDispatcher)
    
    logging.info(f"Servidor RMI iniciado em http://{host}:{port}")
    logging.info(f"Arquivo master: master.txt")
    logging.info(f"Arquivo de usuários: users.json")
    logging.info(f"Log de sincronização: sync.log")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info("Servidor encerrado por interrupção")
        server.server_close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Servidor de sincronização de arquivos RMI')
    parser.add_argument('--host', default='localhost', help='Endereço do host')
    parser.add_argument('--port', type=int, default=8000, help='Porta do servidor')
    args = parser.parse_args()
    
    run_server(args.host, args.port)