import socket
import json
import struct
import os
import hashlib
import multiprocessing

file_name = 'v.flv'
file_folder = './send/'
file_path = file_folder + file_name


if not os.path.exists(file_folder):
    os.makedirs(file_folder)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('extrawdw.net', 23333))
print('Starting service for ' + file_name + '...')
file_size = os.path.getsize(file_path)
file_hash = hashlib.md5(open(file_path,'rb').read()).hexdigest()
file_info = {
    'file_name': file_name,
    'file_size': file_size,
    'file_hash': file_hash
}
print('Service started')

try:
    file_size = file_info['file_size']
    header_bytes = json.dumps(file_info).encode()
    transmit_size = 0
    s.send(struct.pack('I', len(header_bytes)))
    s.recv(1024)
    s.send(header_bytes)
    with open(file_path, 'rb') as f:
        print('Sending ' + str(file_size) + ' bytes...')
        while True:
            send_data = f.read(16384)
            if not send_data:
                break
            s.send(send_data)
            transmit_size += len(send_data)
            print(str(transmit_size) + '/' + str(file_size))
except Exception as e:
    print('Disconnected')
finally:
    print('Done. ' + str(transmit_size) + ' bytes transmitted.')
    s.close()