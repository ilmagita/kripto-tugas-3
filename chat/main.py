from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QApplication
from PyQt5 import uic
from datetime import datetime
import sys
import os
import threading

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('chat/windows/main.ui', self)

        # connection slots
        self.sendFileButton.clicked.connect(self.open_filetransfer)
        self.textChatButton.clicked.connect(self.start_chat)
        
        
    def open_filetransfer(self):
        os.system('python -m chat.filetransfer')
    
    def start_chat(self):
        server_thread = threading.Thread(target=self.start_server)
        server_thread.start()
        
        client1_thread = threading.Thread(target=self.start_client1)
        client1_thread.start()
        
        client2_thread = threading.Thread(target=self.start_client2)
        client2_thread.start()
        
    def start_server(self):
        os.system('python -m chat.server')
    
    def start_client1(self):
        os.system('python -m chat.client')
         
    def start_client2(self):
        os.system('python -m chat.client') 
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
