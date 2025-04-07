import socket
from time import sleep

targetIP = "192.168.5.100"
targetPORT = 50000

server = (targetIP,targetPORT);
udpClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = "setq_deg rarm 76.76 87.65 4.59 3.94 78.48 -4.69 -50.63"
encmess = message.encode()
sentBytesCount = udpClient.sendto(encmess, server)

message = "setq_deg head -3.10 31.37"
encmess = message.encode()
sentBytesCount = udpClient.sendto(encmess, server)