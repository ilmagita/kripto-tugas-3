import socket
import threading
from . import config
from datetime import datetime

from algorithm import functionList as fl, rsa

# algorithm
pubKey = fl.read_key_file('algorithm/ilma.pub')
privKey = fl.read_key_file('algorithm/ilma.pri')

# get the current date and time
current_time = datetime.now()

# format the date and time into YYYY-MM-DD HH:MM format
formatted_time = current_time.strftime('%H:%M')

nickname = input('Choose a nickname: ')

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((config.host, config.port))
except Exception as e:
    print(f'An error occured: {e}')
    print(f'Have you started the server yet?')

def decrypt(message):
    content = (message.split())[-1]
    return rsa.rsa_decrypt(content, privKey)

def receive():
    # for receive thread
    while True:
        print('RECEIVE THREAD')
        try:
            message = client.recv(10240).decode('ascii')

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
    # sends an encryption message automatically
    while True:
        print('WRITING THREAD')
        plaintext = input(f'{nickname}, enter your message: ')
        encrypted_message = rsa.rsa_encrypt(plaintext, pubKey)
        message = '{} {} (ENC): {}'.format(formatted_time, nickname, encrypted_message)
        client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()