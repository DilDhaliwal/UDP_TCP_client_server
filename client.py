#Dil Dhaliwal
# Import socket module
from socket import * 
import sys # In order to terminate the program
import struct
import random
import time
#serverName = '34.69.60.253'
serverName = '127.0.0.1'
#UDP
# Assign a port number
serverPort = 12000
# Bind the socket to server address and server port
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(3)

def check_server_response(response):
    data_len, pcode, entity = struct.unpack_from('!IHH', response)
    if pcode==555:
        response = response[8:]
        print(response.decode())
        sys.exit()
    return

# Make packet 
data = 'Hello World!!!'
# Padding data
if len(data) % 4 != 0:
    pad = len(data) + (4 - len(data) % 4)
    data = data.ljust(pad, '\0')
data_len = len(data)
pcode = 0
entity = 1
c_packet1 = struct.pack('!I H H', data_len, pcode, entity)
c_packet2 = data.encode('utf-8')
c_packet = c_packet1 + c_packet2
# Connect to server
#clientSocket.connect((serverName, serverPort))
# Send packet to server
clientSocket. sendto(c_packet, (serverName, serverPort))
# Receive packet from server
s_packet, serverAddress = clientSocket.recvfrom(2048)
check_server_response(s_packet)
# Unpack packet from server
s_packet_unpacked = struct.unpack('!I H H I I H H', s_packet)
#Stage A print packet from server 
print('------------ Starting Stage A  ------------')
print(f'Recieved packed from server: data_len: {s_packet_unpacked[0]} pcode: {s_packet_unpacked[1]} entity: {s_packet_unpacked[2]} repeat: {s_packet_unpacked[3]} udp port: {s_packet_unpacked[4]} len: {s_packet_unpacked[5]} codeA: {s_packet_unpacked[6]}')
print('------------ End of Stage A  ------------')
print('')


#Update udp_port
serverPort = s_packet_unpacked[4]
print('------------ Starting Stage B  ------------')
# Make packets
pad = 0
l_en = s_packet_unpacked[5]
repeat = s_packet_unpacked[3]
if l_en % 4 != 0:
    pad = (4 - (l_en % 4))
pcode = s_packet_unpacked[6]
entity = 1
if pad != 0:
    data = bytearray((l_en + pad) * '0', 'utf-8') 
else:
    data = bytearray(l_en * '0', 'utf-8')
data_len = len(data) + 4
l_en = len(data)
i = 0
while repeat > i:
    c_packet1 = struct.pack('!I H H I', data_len, pcode, entity, i)
    c_packet = c_packet1 + data
    # Send packet to server
    clientSocket.sendto(c_packet, (serverName, serverPort))
    # Receive and unpack packet from server
    received = False
    while True:
        try:
            s_packet, serverAddress = clientSocket.recvfrom(2048)
            break
        except:
            time.sleep(3)
            clientSocket.sendto(c_packet, (serverName, serverPort))
    i = i + 1
    check_server_response(s_packet)
    s_packet_unpacked = struct.unpack('!I H H I', s_packet)
    # Print packet from server
    print(f'Received acknowledgement packet from server: data_len: {s_packet_unpacked[0]} pcode: {s_packet_unpacked[1]} entity: {s_packet_unpacked[2]} acknumber: {s_packet_unpacked[3]}')
# Receive final packet from server for B and unpack
s_packet, serverAddress = clientSocket.recvfrom(2048)
s_packet_unpacked = struct.unpack('!I H H I I', s_packet)
print(f'Received final packet: data_len: {s_packet_unpacked[0]} pcode: {s_packet_unpacked[1]} entity: {s_packet_unpacked[2]} tcp_port: {s_packet_unpacked[3]} codeB: {s_packet_unpacked[4]}')
print('------------ End of Stage B  ------------')
clientSocket.close()


#TCP
# Assign a port number
serverPort = s_packet_unpacked[3]
# Bind the socket to server address and server port
time.sleep(4)
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))


print('')
print('------------ Starting Stage C  ------------')
print(f'connecting to server at tcp port {s_packet_unpacked[3]}')
#Receive packet 
s_packet = clientSocket.recv(1024)
s_packet_unpacked = struct.unpack('!I H H I I I s', s_packet)
data_decode = s_packet_unpacked[6].decode()
print(f'Received packet from server: data_len: {s_packet_unpacked[0]}  pcode: {s_packet_unpacked[1]} entity: {s_packet_unpacked[2]} repeat2: {s_packet_unpacked[3]} len2: {s_packet_unpacked[4]} codeC: {s_packet_unpacked[5]} char: {data_decode}')
print('------------ End of Stage C  ------------')


time.sleep(1)
repeat2 = s_packet_unpacked[3] 
data_len = s_packet_unpacked[4]  
if data_len % 4 != 0:
    data_len = data_len + (4 - (s_packet_unpacked[4] % 4))
data = data_decode * data_len
data_encoded = data.encode()
print('')
print('------------ Starting Stage D  ------------')
print(f'sending {data} to server for {repeat2} times')
entity = 1
pcode = s_packet_unpacked[5]
i = 0
for i in range(repeat2):
    c_packet1 = struct.pack('!I H H', data_len, pcode, entity)
    c_packet = c_packet1 + data_encoded
    clientSocket.send(c_packet)
    i = i + 1
    time.sleep(1)
s_packet = clientSocket.recv(1024)
s_packet_unpacked = struct.unpack(f'!I H H I', s_packet)
print(f'Received from server: data_len: {s_packet_unpacked[0]} pcode: {s_packet_unpacked[1]} entity: {s_packet_unpacked[2]} codeD: {s_packet_unpacked[3]}')
clientSocket.close()





