import socket
import threading
from . config import host, port
from algorithm import RSA, functionList as fl
from datetime import datetime

import os

# get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
key_dir = os.path.join(current_dir, 'key')
privKey_path = os.path.join(current_dir, 'key', 'key.pri')
pubKey_path = os.path.join(current_dir, 'key', 'key.pub')

import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

pubKey = fl.read_key_file(privKey_path)
privKey = fl.read_key_file(pubKey_path)

# get the current date and time
current_time = datetime.now()
formatted_time = current_time.strftime('%H:%M')

class Client:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        msg = tkinter.Tk()
        msg.withdraw()

        self.nickname = simpledialog.askstring('Enter nickname', 'Enter your nickname:', parent=msg)

        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):
        self.win = tkinter.Tk()

        screen_height = self.win.winfo_screenheight()
        window_height = int(screen_height * 0.8)
        self.win.geometry(f'400x{window_height}')

        self.win.configure(bg="lightgray")

        self.chat_label = tkinter.Label(self.win, text="Chat:", bg="lightgray")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')

        button_frame = tkinter.Frame(self.win, bg="lightgray")
        button_frame.pack(pady=5)

        self.send_button = tkinter.Button(button_frame, text='Send', command=self.write)
        
        self.send_button.config(font=('Arial', 12))
        self.send_button.pack(side='left', padx=20, pady=5)

        self.decrypt_button = tkinter.Button(button_frame, text='Decrypt', command=self.decrypt)
        self.decrypt_button.config(font=('Arial', 12))
        self.decrypt_button.pack(side="left", padx=10, pady=5)

        self.msg_label = tkinter.Label(self.win, text="Message:", bg="lightgray")
        self.msg_label.config(font=("Arial", 12))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.input_area.pack(padx=20, pady=5)

        self.gui_done = True
        self.win.protocol("WM_DELETE_WINDOW", self.stop)
        self.win.mainloop()

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')

            except ConnectionAbortedError:
                print('An error occured while connecting to the server! Your connection has been terminated.')
                break

            except Exception as e:
                print('Error: {e}')
                self.sock.close()
                break

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)
    
    def write(self):
        plaintext = self.input_area.get('1.0', 'end')
        enc = RSA.rsa_encrypt(plaintext, pubKey)

        message = f"{self.nickname} (ENC): {enc}\n"
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')

    def decrypt(self):
        self.text_area.config(state='normal')
        latest_msg = self.text_area.get('1.0', tkinter.END)
        self.text_area.config(state='disabled')

        # Find the index of the last space
        last_space_index = latest_msg.rfind(' ')
        cipher = latest_msg[last_space_index + 1:]

        dec = RSA.rsa_decrypt(cipher, privKey)

        dec_msg = f'Decrypted message: {dec}\n\n'
        # test_msg = f'Latest message: {cipher}\n\n'

        self.text_area.config(state='normal')
        # self.text_area.insert('end', test_msg)
        self.text_area.insert('end', dec_msg)
        self.text_area.yview('end')
        self.text_area.config(state='disabled')

client = Client(host, port)