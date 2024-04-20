import threading
import socket
from . import config
from algorithm import functionList as fl, rsa

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((config.host, config.port))
server.listen()     # server is now on listening method

clients = []
nicknames = []

# broadcast method
def broadcast(message):
    for client in clients:
        try:
            client.send(message.encode('ascii'))
        except Exception as e:
            print('There was an error in broadcasting the message {}: {}'.format(message, e))

# handle method
def handle(client):
    while True:
        try:
            message = client.recv(1024)

            # # check if message is encrypted
            # parts = message.split(':')
            # parts = parts[0].split()
            # keyword = parts[-1]
            # latest_sender = parts[0]

            # if keyword == 'ENC':
            #     broadcast(f'{latest_sender} sent an encrypted message.')
            broadcast(message.decode('ascii'))

        except:
            # handles when a client leaves/terminates their connection
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]

            broadcast(f'{nickname} has left the chat.')
            broadcast(f'Online: {nicknames}')
            print(f'{nickname} has terminated the connection.')
            nicknames.remove(nickname)
            break

# receive method - receive new connections
def receive():
    while True:
        client, address = server.accept()
        print(f'New connection accepted from client in {str(address)}')

        if client:
            client.send('NICK'.encode('ascii'))             # sends NICK to signal client to send its nickname
            # client will send nickname (see client_rsa.py)

            nickname = client.recv(1024).decode('ascii')
            nicknames.append(nickname)
            clients.append(client)

            print(f'New client added: {nickname}')
            broadcast(f'{nickname} joined the chat.')
            client.send('You have connected to the RSA server!'.encode('ascii'))
            client.send(f'\nCurrently online: {nicknames}'.encode('ascii'))

            thread = threading.Thread(target=handle, args=(client,))
            thread.start()
        else:
            print('Failed to accept connection.')

print("RSA Server started!")
print("Server is listening...")
receive()