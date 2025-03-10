from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtCore import pyqtSignal


class LoginScreen(QWidget):
    login_successful = pyqtSignal()
    def __init__(self,client_socket):
        super().__init__()
        self.client = client_socket
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("user name")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("login", self)
        self.login_button.clicked.connect(self.check_login)
        layout.addWidget(self.login_button)

        self.login_button = QPushButton("register", self)
        self.login_button.clicked.connect(self.check_register)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        self.client.send_message({"status": "login" , "username": username, "password": password})

    def check_register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        self.client.send_message({"status": "register", "username": username, "password": password})
    
    def login_s(self):
        self.login_successful.emit()

