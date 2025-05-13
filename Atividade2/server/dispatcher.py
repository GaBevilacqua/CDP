from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import time
import os
import logging
import hashlib
from common.auth import load_users

class RequestDispatcher(BaseHTTPRequestHandler):
    file_handler = None  
    users_file = 'users.json'
    
    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def _parse_request_data(self):
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length:
            return json.loads(self.rfile.read(content_length))
        return {}
    
    def _load_users(self) -> dict:
        try:
            if not os.path.exists(self.users_file):
                logging.error(f"Arquivo {self.users_file} não encontrado")
                return {}

            with open(self.users_file, 'r') as f:
                users = json.load(f)
                if not isinstance(users, dict):
                    raise ValueError("Formato inválido de users.json")
                return users
        except json.JSONDecodeError:
            logging.error(f"Erro ao decodificar {self.users_file}")
            return {}
        except Exception as e:
            logging.error(f"Erro ao carregar usuários: {str(e)}")
            return {}

    def _authenticate(self, auth_token: str) -> str:
        try:
            users = load_users(self.users_file)
            for username, password in users.items():
                if hashlib.sha256(f"{username}:{password}".encode()).hexdigest() == auth_token:
                    return username
            return None
        except Exception as e:
            logging.error(f"Erro na autenticação: {str(e)}")
            return None

    def _log_request(self, username: str, success: bool, message: str):
        log_entry = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'username': username,
            'client_ip': self.client_address[0],
            'success': success,
            'message': message
        }
        
        with open('sync.log', 'a') as log_file:
            log_file.write(json.dumps(log_entry) + '\n')
        
        status = "SUCCESS" if success else "FAILED"
        logging.info(f"[{status}] {username}@{self.client_address[0]}: {message}")
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        endpoint = parsed_path.path
        params = parse_qs(parsed_path.query)
        auth_token = params.get('auth_token', [''])[0]

        username = self._authenticate(auth_token)
        if not username:
            self._set_headers(401)
            self.wfile.write(json.dumps({
                'status': 'error',
                'message': 'Autenticação falhou'
            }).encode())
            return

        try:
            if endpoint == '/check_master_version':
                version_info = self.file_handler.get_version_info()
                self._set_headers()
                self.wfile.write(json.dumps({
                    'status': 'success',
                    'version_info': version_info
                }).encode())

            elif endpoint == '/get_file_content':
                content = self.file_handler.read_content()
                if content is None:
                    self._set_headers(404)
                    self.wfile.write(json.dumps({
                        'status': 'error',
                        'message': 'Arquivo master não encontrado'
                    }).encode())
                    return
                    
                self._set_headers()
                self.wfile.write(json.dumps({
                    'status': 'success',
                    'content': content,
                    'content_hash': hashlib.sha256(content.encode()).hexdigest()
                }).encode())

            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({
                    'status': 'error',
                    'message': 'Endpoint não encontrado'
                }).encode())

        except Exception as e:
            logging.error(f"Erro no GET {endpoint}: {str(e)}", exc_info=True)
            self._set_headers(500)
            self.wfile.write(json.dumps({
                'status': 'error',
                'message': f'Erro interno: {str(e)}'
            }).encode())

    def do_POST(self):
        try:
            parsed_path = urlparse(self.path)
            endpoint = parsed_path.path
            data = self._parse_request_data()

            logging.debug(f"POST recebido para {endpoint} com dados: {data}")

            auth_token = data.get('auth_token', '')
            username = self._authenticate(auth_token)
            if not username:
                self._set_headers(401)
                self.wfile.write(json.dumps({
                    'status': 'error',
                    'message': 'Token inválido'
                }).encode())
                return

            if endpoint == '/update_file_content':
                content = data.get('content', '')
                if not content:
                    self._set_headers(400)
                    self.wfile.write(json.dumps({
                        'status': 'error',
                        'message': 'Conteúdo não pode ser vazio'
                    }).encode())
                    return

                try:
                    self.file_handler.write_content(content)
                    self._log_request(username, True, 'Arquivo master atualizado')
                    self._set_headers(200)
                    self.wfile.write(json.dumps({
                        'status': 'success',
                        'message': 'Arquivo master atualizado',
                        'bytes_written': len(content),
                        'content_hash': hashlib.sha256(content.encode()).hexdigest()
                    }).encode())
                except Exception as e:
                    self._log_request(username, False, f'Falha ao atualizar: {str(e)}')
                    raise

            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({
                    'status': 'error',
                    'message': f'Endpoint {endpoint} não encontrado'
                }).encode())

        except Exception as e:
            logging.error(f"Erro no POST: {str(e)}", exc_info=True)
            self._set_headers(500)
            self.wfile.write(json.dumps({
                'status': 'error',
                'message': f'Erro interno: {str(e)}'
            }).encode())