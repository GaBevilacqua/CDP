import socket
import struct
from xml.etree import ElementTree as ET

class MulticastReceiver:
    def __init__(self):
        self.people = []  
        self.root = ET.Element('pessoas')  

    def converterPXML(self, xml_str):
        try:
            person_element = ET.fromstring(xml_str)
            self.root.append(person_element)
            person_data = {
                'id': person_element.get('id'),
                'name': person_element.find('nome').text,
                'place': person_element.find('lugar').text,
                'year': person_element.find('ano').text
            }
            self.people.append(person_data)
            return person_data
            
        except Exception as e:
            print(f"Erro no XML: {e}")
            return None

    def save_final_xml(self, filename='arquivo.xml'):
        tree = ET.ElementTree(self.root)
        tree.write(filename, encoding='utf-8', xml_declaration=True)

    def run(self):
        MULTICAST_GROUP = '224.1.1.1'
        PORT = 5007
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', PORT))

        mreq = struct.pack('4sL', socket.inet_aton(MULTICAST_GROUP), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        
        print("Em espera...")
        
        try:
            while True:
                data, address = sock.recvfrom(4096)
                print(f"\nRecebido de {address}:")
                
                person_data = self.converterPXML(data.decode('utf-8'))
                if person_data:
                    print("Dados da pessoa:")
                    print(f"ID: {person_data['id']}")
                    print(f"Nome: {person_data['name']}")
                    print(f"Local: {person_data['place']}")
                    print(f"Ano: {person_data['year']}")
                    
        except KeyboardInterrupt:
            print("\nEncerrando.. .")
            if self.people:
                self.save_final_xml()
        finally:
            sock.close()

if __name__ == '__main__':
    receiver = MulticastReceiver()
    receiver.run()