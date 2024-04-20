import socket
import threading
from . import config
from datetime import datetime

import sys

### TODO: bikin sys.path.append ini ilang pake packaging import module things gue ga bisa mikir
# sys.path.append('../algorithm') 

from algorithm import functionList as fl, rsa

# algorithm
pubKey = fl.read_key_file('algorithm/ilma.pub')
privKey = fl.read_key_file('algorithm/ilma.pri')

# Get the current date and time
current_time = datetime.now()

# Format the date and time into YYYY-MM-DD HH:MM format
formatted_time = current_time.strftime('%H:%M')

nickname = input('Choose a nickname: ')

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((config.host, config.port))
except Exception as e:
    print(f'An error occured: {e}')
    print(f'Have you started the server yet?')

def receive():
    # for receive thread
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print('An error occured while connecting to the server! Your connection has been terminated.')
            client.close()
            break

def write():
    # for writing thread
    while True:
        plaintext = input(f'{nickname}, enter your message: ')
        encrypted_message = rsa.rsa_encrypt(plaintext, pubKey)
        message = '{} {}: {}'.format(formatted_time, nickname, encrypted_message)
        client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()