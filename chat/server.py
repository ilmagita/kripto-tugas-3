import threading
import socket
from . config import host, port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()     # server is now on listening method

clients = []
nicknames = []

# broadcast method
def broadcast(message):
    for client in clients:
        try:
            client.send(message.encode('utf-8'))
        except Exception as e:
            print('There was an error in broadcasting the message {}: {}'.format(message, e))

# handle method
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message.decode('utf-8'))
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]

            broadcast(f'{nickname} has left the chat.')
            broadcast(f'Online: {nicknames}')
            print(f'{nickname} has terminated the connection.')
            nicknames.remove(nickname)
            break

# receive method
def receive():
    while True:
        client, address = server.accept()
        print(f'New connection accepted from client in {str(address)}')

        if client:
            client.send('NICK'.encode('utf-8'))             # sends NICK to signal client to send its nickname
            nickname = client.recv(1024).decode('utf-8')
            nicknames.append(nickname)
            clients.append(client)

            print(f'New client added: {nickname}')
            broadcast(f'{nickname} joined the chat.')
            client.send('You have connected to the server!'.encode('utf-8'))
            client.send(f'\nCurrently online: {nicknames}'.encode('utf-8'))

            thread = threading.Thread(target=handle, args=(client,))
            thread.start()
        else:
            print('Failed to accept connection.')

print("Server started!")
print("Server is listening...")
receive()