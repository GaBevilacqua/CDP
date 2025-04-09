import socket
import struct
from xml.etree import ElementTree as ET
import time

def createPXML(id,name, place, year):
    #Criando uma pessoa e atribuindo um identficador a ela
    pessoa = ET.Element('pessoa')
    pessoa.set('id', str(id))

    #Toda pessoa tem um nome, lugar e ano
    ET.SubElement(pessoa, 'nome').text = name
    ET.SubElement(pessoa, 'lugar').text = place
    ET.SubElement(pessoa, 'ano').text = year

    return ET.tostring(pessoa, encoding='utf-8')

def multicast_produtor():
    MULTICAST_GROUP = '224.1.1.1'
    PORT = 5007
    TTL = 1

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL,TTL)

    data = [
        {'id': 123456789, 'name': 'Smith', 'place': 'Londres', 'year': 1984},
        {'id': 987654321, 'name': 'João', 'place': 'São Paulo', 'year': 1990},
        {'id': 555555555, 'name': 'Maria', 'place': 'Lisboa', 'year': 1988}
    ]

    try:
        for byte in data:
            xml_d = createPXML(
                byte['id'],
                byte['name'],
                byte['place'],
                byte['year']
            )
            sock.sendto(xml_d, (MULTICAST_GROUP, PORT))
            print(f"Enviado: {xml_d.decode('utf-8')}")
            time.sleep(2)
    finally:
        sock.close()

if __name__ == '__main__':
    multicast_produtor()