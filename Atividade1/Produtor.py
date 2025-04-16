import socket
from xml.etree import ElementTree as ET
import time

def createPXML(id,name, place, year):
    pessoa = ET.Element('pessoa')
    pessoa.set('id', str(id))

    ET.SubElement(pessoa, 'nome').text = str(name)
    ET.SubElement(pessoa, 'lugar').text = str(place)
    ET.SubElement(pessoa, 'ano').text = str(year)

    return ET.tostring(pessoa, encoding='utf-8')

def multicast_produtor():
    MULTICAST_GROUP = '224.1.1.1'
    PORT = 5007
    TTL = 1

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL,TTL)

    data = [
        {'id': 27852857868, 'name': 'Brenda Fernandes', 'place': 'Naucalpan', 'year': 1990},
        {'id': 76867357881, 'name': 'Hector Herreira', 'place': 'Iztapalapa', 'year': 1991},
        {'id': 47723388101, 'name': 'Juan Plata', 'place': 'Ecatepec', 'year': 1993}
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