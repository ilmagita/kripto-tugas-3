import socket
import threading
from config import host, port
from datetime import datetime

# Get the current date and time
current_time = datetime.now()

# Format the date and time into YYYY-MM-DD HH:MM format
formatted_time = current_time.strftime('%H:%M')

nickname = input('Choose a nickname: ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

def receive():
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
    while True:
        message = '{} {}: {}'.format(formatted_time, nickname, input(''))
        client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()