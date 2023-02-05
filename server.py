#Dil Dhaliwal
# Import socket module
from socket import * 
import sys # In order to terminate the program
import struct
import random
import time
# Assign a port number
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
#Bind the socket to server address and server port
serverSocket.bind(('127.0.0.1', serverPort))
serverSocket.settimeout(3)

while True:
    #Receive packet from client
    c_packet, clientAddress = serverSocket.recvfrom(1024)
    #Unpack packet from client and print
    l_en = c_packet[3]
    c_packet_unpacked = struct.unpack(f'!I H H {l_en}s', c_packet)
    c_packet_data = c_packet_unpacked[3].decode()
    print(f'receiving from the client: data_length: {c_packet_unpacked[0]} code: {c_packet_unpacked[1]} entity: {c_packet_unpacked[2]} data: {c_packet_data}')
    #Make packet to send to client
    data_len = struct.calcsize('!I I H H')
    pcode = 0
    entity = 2
    repeat = random.randint(5, 20)
    l_en = random.randint(50, 100)
    udp_port = random.randint(20000, 30000)
    codeA = random.randint(100, 400)
    s_packet = struct.pack('!I H H I I H H', data_len, pcode, entity, repeat, udp_port, l_en, codeA)
    #Print packet for client
    print('------------ Starting Stage A  ------------')
    print(f'sending to the client: data_length: {data_len} code: {pcode} entity: {entity} repeat: {repeat} udp_port: {udp_port} len: {l_en} codeA: {codeA}')
    print(f'SERVER: Server ready on the new UDP port: {udp_port}')
    print('SERVER:------------ End of Stage A  ------------')
    print('')
    #Send packet to client 
    serverSocket.sendto(s_packet, clientAddress)
    break


serverPort = udp_port
serverSocket.close()
server2Socket = socket(AF_INET, SOCK_DGRAM)
server2Socket.bind(('127.0.0.1', serverPort))
if l_en % 4 == 0:
    l_en = l_en 
else:
    l_en = l_en + (4 - (l_en % 4))
print('SERVER:------------ Starting Stage B  ------------')
i = 0
while repeat > i:
    random_ack = random.randint(1, 100)
    # Receive, unpack, and print packet
    c_packet, clientAddress = server2Socket.recvfrom(2048)
    c_packet_unpacked = struct.unpack(f'!I H H I {l_en}s', c_packet)
    if random_ack > 50 and c_packet_unpacked[3] == i:
        entity = 2
        data_len = 4 
        pcode = c_packet_unpacked[1]
        s_packet = struct.pack('!I H H I', data_len, pcode, entity, i)
        server2Socket.sendto(s_packet, clientAddress)
        i = i + 1
        print(f'SERVER: received packet_id {c_packet_unpacked[3]} data_len {c_packet_unpacked[0]} pcode: {c_packet_unpacked[1]}')
    # Create packet and send to client
    # Send final packet to client for B 
data_len = struct.calcsize('!I I')
tcp_port = random.randint(20000, 30000)
codeB = random.randint(100, 400)
s_packet = struct.pack('!I H H I I', data_len, pcode, entity, tcp_port, codeB)
server2Socket.sendto(s_packet, clientAddress)
print(f'------------- B2: sending tcp_port {tcp_port} codeB {codeB}')
print('------------ End of Stage B  ------------')
server2Socket.close()


#TCP
# Create a TCP server socket
#(AF_INET is used for IPv4 protocols)
#(SOCK_STREAM is used for TCP)
serverSocket = socket(AF_INET, SOCK_STREAM)
# Assign a port number
serverPort = tcp_port
# Bind the socket to server address and server port
serverSocket.bind(('127.0.0.1', serverPort))
# Listen to at most 1 connection at a time
serverSocket.listen(5)


print('')
print('------------ Stating Stage C ------------')
# Server should be up and running and listening to the incoming connections
print(f'The server is ready to receive on tcp port: {tcp_port}')
while True:
    # Set up a new connection from the client
    connectionSocket, addr = serverSocket.accept()
    #Make packet and send to client
    pcode = codeB
    entity = 2
    repeat2 = random.randint(5, 20)
    len2 = random.randint(50, 100)
    codeC = random.randint(100, 400)
    data = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ').encode()
    data_len = len(data) + struct.calcsize('III')
    s_packet = struct.pack('!I H H I I I s', data_len, pcode, entity, repeat2, len2, codeC, data)
    print(f'Server Sending to the client: data_length: {data_len} code: {pcode} entity: {entity} repeat2: {repeat2} len2: {len2} codeC: {codeC}')
    connectionSocket.send(s_packet)
    break
print('------------ End of Stage C    ------------')


time.sleep(1)
if len2 % 4 != 0:
    len2 = len2 + (4 - (len2 % 4))
print('')
print('------------ Starting Stage D  ------------')
print('Starting to receive packets from client')
for i in range(repeat2):
    s_packet = connectionSocket.recv(1024)
    s_packet_unpacked = struct.unpack(f'!I H H {len2}s', s_packet)
    data = s_packet_unpacked[3].decode()
    print(f'i = {i} data_len: {s_packet_unpacked[0]} pcode: {s_packet_unpacked[1]} entity: {s_packet_unpacked[2]} data: {data}')
data_len = struct.calcsize('I')
pcode = codeC
entity = 2
codeD = random.randint(100, 400)
s_packet = struct.pack('!I H H I', data_len, pcode, entity, codeD)
connectionSocket.send(s_packet)
connectionSocket.close()
serverSocket.close()  
sys.exit()#Terminate the program after sending the corresponding data





