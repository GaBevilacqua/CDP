import socket
import struct
from xml.etree import ElementTree as ET

def converterPXML(xml_str):
    try:
        root = ET.fromstring(xml_str)
        person_id = root.get('id')
        name = root.find('nome').text
        place = root.find('place').text
        year = root.find('ano').text
        
        return {
            'id': person_id,
            'name': name.strip() if name else None,
            'place': place.strip() if place else None,
            'year': year.strip() if year else None
        }
    except Exception as e:
        print(f"Erro ao parsear XML: {e}")
        return None
    

def multicast_receiver():
    MULTICAST_GROUP = '224.1.1.1'
    PORT = 5007
    # Cria socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Vincula ao servidor
    sock.bind(('', PORT))

    # Entra no grupo multicast
    mreq = struct.pack('4sL', socket.inet_aton(MULTICAST_GROUP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    
    print("Aguardando mensagens multicast...")
    
    try:
        while True:
            # Recebe dados
            data, address = sock.recvfrom(4096)
            print(f"\nRecebido de {address}:")
            
            # Desserializa e processa o XML
            person_data = converterPXML(data.decode('utf-8'))
            if person_data:
                print("Dados da pessoa:")
                print(f"ID: {person_data['id']}")
                print(f"Nome: {person_data['name']}")
                print(f"Local: {person_data['place']}")
                print(f"Ano: {person_data['year']}")
                
    except KeyboardInterrupt:
        print("Encerrando consumidor...")
    finally:
        sock.close()

if __name__ == '__main__':
    multicast_receiver()
