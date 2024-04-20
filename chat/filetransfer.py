from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QApplication
from PyQt5 import uic
from datetime import datetime
import sys

from algorithm.functionList import *
from algorithm import RSA
from algorithm.RSA import privKey_path, pubKey_path

pubKey = read_key_file(privKey_path)
privKey = read_key_file(pubKey_path)

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('chat/windows/filetransfer.ui', self)

        # variable initialization
        self.encryptedState = False
        self.filePath = ''
        self.fileName = ''
        self.fileType = ''
        self.fileBaseName = ''
        self.text_contents_encrypted = ''

        # connection slots
        self.filePathBtn.clicked.connect(self.onFilePathBtnClicked)
        self.encryptFileBtn.clicked.connect(self.onEncryptBtnClicked)
        self.decryptFileBtn.clicked.connect(self.onDecryptBtnClicked)

    def onFilePathBtnClicked(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, 'Open File to be Encrypted')

        if file_path:
            self.filePathTextBox.setText(file_path)
            self.filePath = file_path
            self.fileName = get_file_name(file_path)
            self.fileType = get_file_type(file_path)
            self.fileBaseName = get_base_file_name(file_path)

            file_dialog.reject()

    def onEncryptBtnClicked(self):
        if self.filePath == '':
            msg = QMessageBox()
            msg.setText('File path must be defined!')
            msg.exec_()
            
        if self.fileType == '.txt':
            text_file_content = read_text_file(self.filePath)
            self.senderTextBox.setPlainText(f'Sending encrypted content: {text_file_content}')
            self.text_contents_encrypted = RSA.rsa_enc_text_file(self.filePath, pubKey)
            self.receivedTextBox.setPlainText(self.text_contents_encrypted)
            self.senderTextBox.verticalScrollBar().setValue(self.senderTextBox.verticalScrollBar().maximum())

    def onDecryptBtnClicked(self):
        if self.text_contents_encrypted == '':
            msg = QMessageBox()
            msg.setText("Haven't received a file yet!")
            msg.exec_()

        if self.fileType == '.txt':
            text_contents_decrypted = RSA.rsa_decrypt(self.text_contents_encrypted, privKey)
            self.receivedTextBox.appendPlainText(f'\n\n---------\nDecrypting content\n')
            self.receivedTextBox.appendPlainText(text_contents_decrypted)
            self.receivedTextBox.verticalScrollBar().setValue(self.receivedTextBox.verticalScrollBar().maximum())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
