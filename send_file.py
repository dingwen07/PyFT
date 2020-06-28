import socket
import json
import struct
import os
import hashlib
import multiprocessing

file_name = 'v.flv'
file_folder = './send/'
file_path = file_folder + file_name

def transmit(cnn, addr, file_info):
    print(str(addr) + ' Connected')
    try:
        file_size = file_info['file_size']
        header_bytes = json.dumps(file_info).encode()
        transmit_size = 0
        cnn.send(struct.pack('I', len(header_bytes)))
        cnn.recv(1024)
        cnn.send(header_bytes)
        with open(file_path, 'rb') as f:
            print(str(addr) + ' Sending ' + str(file_size) + ' bytes...')
            while True:
                send_data = f.read(16384)
                if not send_data:
                    break
                cnn.send(send_data)
                transmit_size += len(send_data)
    except Exception as e:
        print(str(addr) + ' Disconnected')
    finally:
        print(str(addr) + ' Done. ' + str(transmit_size) + ' bytes transmitted.')
        cnn.close()

if __name__ == "__main__":
    if not os.path.exists(file_folder):
        os.makedirs(file_folder)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 23333 ))
    s.listen(5)
    print('Starting service for ' + file_name + '...')
    file_size = os.path.getsize(file_path)
    file_hash = hashlib.sha1(open(file_path,'rb').read()).hexdigest()
    header = {
        'file_name': file_name,
        'file_size': file_size,
        'file_hash': file_hash
    }
    print('Service started')

    while True:
        try:
            cnn, addr = s.accept()
            m = multiprocessing.Process(target=transmit, args=(cnn, addr, header,))
            m.daemon = True
            m.start()
        except Exception as e:
            print(e)
