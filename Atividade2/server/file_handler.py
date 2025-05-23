import os
import hashlib
import logging
from typing import Dict, Any

class FileHandler:
    def __init__(self, file_path: str):
        self.file_path = os.path.abspath(file_path)
        self._ensure_file_exists()
        logging.info(f"FileHandler configurado para: {self.file_path}")

    def _ensure_file_exists(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                f.write('')
            logging.info(f"Arquivo criado: {self.file_path}")

    def read_content(self) -> str:
        with open('master.txt', 'r') as f:
            return f.read()

    def write_content(self, content: str):
        with open(self.file_path, 'w') as f:
            f.write(content)

    def get_version_info(self) -> Dict[str, Any]:
        content = self.read_content()
        return {
            'content_hash': hashlib.sha256(content.encode()).hexdigest(),
            'last_modified': os.path.getmtime(self.file_path),
            'size': len(content.encode('utf-8'))
        }