"""
Monitor de sincronização automática de arquivos.
"""

import os
import hashlib
import time
import logging
from typing import Optional

class SyncMonitor:
    def __init__(self, stub, protocol_mode: str = 'R', interval: int = 5):
        self.stub = stub
        self.protocol_mode = protocol_mode
        self.interval = interval
        self.running = False
        self.slave_file = 'slave.txt'
        self._init_file()
        self.last_hash = self._calculate_file_hash()

    def _init_file(self):
        """Garante que o arquivo slave existe."""
        if not os.path.exists(self.slave_file):
            with open(self.slave_file, 'w') as f:
                f.write('')
            logging.info(f"Arquivo {self.slave_file} criado")

    def _calculate_file_hash(self) -> Optional[str]:
        """Calcula o hash SHA-256 do arquivo slave."""
        try:
            with open(self.slave_file, 'r') as f:
                return hashlib.sha256(f.read().encode()).hexdigest()
        except IOError as e:
            logging.error(f"Erro ao ler arquivo: {str(e)}")
            return None

    def _sync(self):
        """Executa uma sincronização completa."""
        try:
            server_version = self.stub.check_master_version()
            if server_version.get('content_hash') != self.last_hash:
                content = self.stub.get_file_content()
                with open(self.slave_file, 'w') as f:
                    f.write(content)
                self.last_hash = self._calculate_file_hash()
                logging.info("Sincronização concluída")
                
        except Exception as e:
            logging.error(f"Erro na sincronização: {str(e)}")

    def start(self):
        """Inicia o monitoramento periódico."""
        self.running = True
        logging.info(f"Iniciando monitor (Intervalo: {self.interval}s)")
        
        try:
            while self.running:
                self._sync()
                for _ in range(self.interval):
                    if not self.running:
                        break
                    time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """Para o monitoramento."""
        self.running = False
        logging.info("Monitor encerrado")

    def manual_sync(self, content: str):
        """Sincronização manual."""
        try:
            response = self.stub.update_file_content(content, self.protocol_mode)
            with open(self.slave_file, 'w') as f:
                f.write(content)
            self.last_hash = self._calculate_file_hash()
            logging.info(f"Sincronização manual: {response.get('message')}")
        except Exception as e:
            logging.error(f"Erro na sincronização manual: {str(e)}")
            raise