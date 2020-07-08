def gen_file(file_name, size=2048):
    with open(file_name, 'wb') as f:
        f.seek(size - 1)
        f.write(' '.encode('utf8'))


file_name = '1.txt'
file_size = 30000000000
gen_file(file_name, file_size)
