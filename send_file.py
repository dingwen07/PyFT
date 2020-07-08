import socket
import json
import struct
import os
import hashlib
import multiprocessing

file_path = './send/Windows.iso'
file_name = os.path.basename(file_path)

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
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 23333 ))
    s.listen(5)
    print('Starting service for {} ...'.format(file_name))
    file_size = os.path.getsize(file_path)
    print('File size: {} bytes'.format(str(file_size)))
    with open(file_path, 'rb') as f:
        file_hash = hashlib.md5()
        '''
        while chunk := f.read(16384):
            file_hash.update(chunk)
        '''
        while True:
            chunk = f.read(16384)
            if not chunk:
                break
            file_hash.update(chunk)
        file_hash = file_hash.hexdigest()
    print('File hash: {}'.format(file_hash))
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
