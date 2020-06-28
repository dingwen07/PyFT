import socket
import json
import struct
import os
import hashlib

file_folder = './recv/'

if not os.path.exists(file_folder):
    os.makedirs(file_folder)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 23333 ))
s.listen(5)
cnn, addr = s.accept()

print('Connected, retrieving file information...')
stobj = cnn.recv(16)
header_size = struct.unpack('I', stobj)[0]
cnn.send('UNBLOCK'.encode())
header = json.loads(cnn.recv(header_size).decode())
file_size = header['file_size']
file_name = header['file_name']
file_hash = header['file_hash']
print('File name: ' + file_name)
print('File size: ' + str(file_size) + ' bytes')
print('File hash: ' + file_hash)
file_path = file_folder + file_name
while os.path.exists(file_path):
    file_name = file_name + '_1'
    file_path = file_folder + file_name
print('Saving to ' + file_path + '...')
print('Receiving...')
with open(file_path, 'wb') as f:
    transmit_size = 0
    while transmit_size < file_size:
        line = cnn.recv(16384)
        f.write(line)
        transmit_size = transmit_size + len(line)
print('Done. ' + str(transmit_size) + ' bytes transmitted.')
cnn.close()   
recv_file_sha256 = hashlib.sha1(open(file_path, 'rb').read()).hexdigest()
if recv_file_sha256 == file_hash:
    print('HASH VERIFICATION PASSED')
else:
    print('HASH VERIFICATION FAILED')
input()
