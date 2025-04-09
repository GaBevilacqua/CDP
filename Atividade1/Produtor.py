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

    sock = socket.socket(socket.AL_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL,TTL)
