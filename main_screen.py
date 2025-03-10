from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QGridLayout, QLabel, QSpacerItem, QSizePolicy, QMessageBox
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap

class MainScreen(QWidget):
    def __init__(self,client_socket):
        super().__init__()
        self.client = client_socket
        self.init_ui()

    def init_ui(self):
        self.resize(800, 800)

        main_layout = QVBoxLayout()
        # all player status
        player_info_layout = QGridLayout()
        self.player_infos = []
        self.players_data = [
            {"name": "None", "money": 0, "status": "None"} for i in range(5)
        ]
        for i, player in enumerate(self.players_data):
            info = QLabel(self)
            info.setAlignment(Qt.AlignCenter)
            info.setStyleSheet(
                "font-size: 12px; background-color: lightgray; border: 1px solid black; padding: 5px;"
            )
            info.setText(
                f"{player['name']}\n${player['money']}\n{player['status']}"
            )
            self.player_infos.append(info)
            player_info_layout.addWidget(info, 0, i, Qt.AlignCenter)

        main_layout.addLayout(player_info_layout)

        # pot current player
        info_label_layout = QGridLayout()

        self.pot_label = QLabel("Pot: $0", self)
        self.pot_label.setAlignment(Qt.AlignLeft)
        self.pot_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.current_player_label = QLabel("Waiting ...", self)
        self.current_player_label.setAlignment(Qt.AlignRight)
        self.current_player_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        info_label_layout.addWidget(self.pot_label, 0, 1)
        info_label_layout.addWidget(self.current_player_label, 0, 2)

        main_layout.addLayout(info_label_layout)
        # add five server card
        top_card_layout = QGridLayout()
        self.top_cards = []

        self.server_card_1 = QLabel(self)
        self.server_card_2 = QLabel(self)
        self.server_card_3 = QLabel(self)
        self.server_card_4 = QLabel(self)
        self.server_card_5 = QLabel(self)

        self.server_card_1.setPixmap(QPixmap("images/gray_back.png").scaled(60, 90, Qt.KeepAspectRatio))
        self.server_card_2.setPixmap(QPixmap("images/gray_back.png").scaled(60, 90, Qt.KeepAspectRatio))
        self.server_card_3.setPixmap(QPixmap("images/gray_back.png").scaled(60, 90, Qt.KeepAspectRatio))
        self.server_card_4.setPixmap(QPixmap("images/gray_back.png").scaled(60, 90, Qt.KeepAspectRatio))
        self.server_card_5.setPixmap(QPixmap("images/gray_back.png").scaled(60, 90, Qt.KeepAspectRatio))

        top_card_layout.addWidget(self.server_card_1, 0, 0, Qt.AlignCenter)
        top_card_layout.addWidget(self.server_card_2, 0, 1, Qt.AlignCenter)
        top_card_layout.addWidget(self.server_card_3, 0, 2, Qt.AlignCenter)
        top_card_layout.addWidget(self.server_card_4, 0, 3, Qt.AlignCenter)
        top_card_layout.addWidget(self.server_card_5, 0, 4, Qt.AlignCenter)

        main_layout.addLayout(top_card_layout)

        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # add player card
        bottom_card_layout = QGridLayout()
        self.card_1 = QLabel(self)
        self.card_2 = QLabel(self)

        self.card_1.setPixmap(QPixmap("images/gray_back.png").scaled(100, 150, Qt.KeepAspectRatio))
        self.card_2.setPixmap(QPixmap("images/gray_back.png").scaled(100, 150, Qt.KeepAspectRatio))

        bottom_card_layout.addWidget(self.card_1, 0, 0, Qt.AlignCenter)
        bottom_card_layout.addWidget(self.card_2, 0, 1, Qt.AlignCenter)

        main_layout.addLayout(bottom_card_layout)

        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        button_layout = QGridLayout()

        self.money_label = QLabel("$: 0", self)
        self.money_label.setAlignment(Qt.AlignLeft)
        self.money_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        button_layout.addWidget(self.money_label, 0, 0)
        # add buttom
        self.fold_button = QPushButton("fold", self)
        self.fold_button.clicked.connect(self.fold)
        button_layout.addWidget(self.fold_button, 0, 1)

        self.call_button = QPushButton("call", self)
        self.call_button.clicked.connect(self.call)
        button_layout.addWidget(self.call_button, 0, 2)

        self.raise_button = QPushButton("raise", self)
        self.raise_button.clicked.connect(self.raise_)
        button_layout.addWidget(self.raise_button, 0, 3)

        self.allin_button = QPushButton("all in", self)
        self.allin_button.clicked.connect(self.allin)
        button_layout.addWidget(self.allin_button, 0, 4)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
    
    def update_card_3(self, card_value_1, card_value_2, card_value_3):
        pixmap1 = QPixmap(f"images/{card_value_1}.png").scaled(60, 90, Qt.KeepAspectRatio)
        pixmap2 = QPixmap(f"images/{card_value_2}.png").scaled(60, 90, Qt.KeepAspectRatio)
        pixmap3 = QPixmap(f"images/{card_value_3}.png").scaled(60, 90, Qt.KeepAspectRatio)
        self.server_card_1.setPixmap(pixmap1)
        self.server_card_2.setPixmap(pixmap2)
        self.server_card_3.setPixmap(pixmap3)

    def update_card_4(self, card):
        pixmap = QPixmap(f"images/{card}.png").scaled(60, 90, Qt.KeepAspectRatio)
        self.server_card_4.setPixmap(pixmap)

    def update_card_5(self, card):
        pixmap = QPixmap(f"images/{card}.png").scaled(60, 90, Qt.KeepAspectRatio)
        self.server_card_5.setPixmap(pixmap)
    
    def update_player_two_card(self, card1, card2):
        pixmap1 = QPixmap(f"images/{card1}.png").scaled(100, 150, Qt.KeepAspectRatio)
        pixmap2 = QPixmap(f"images/{card2}.png").scaled(100, 150, Qt.KeepAspectRatio)
        self.card_1.setPixmap(pixmap1)
        self.card_2.setPixmap(pixmap2)

    def update_pot(self, pot_value):
        self.pot_label.setText(f"Pot: ${pot_value}")

    def update_current_player(self, current_turn , id):
        if id == current_turn:
            self.current_player_label.setText("Your trun !")
        else:
            self.current_player_label.setText("Waiting ...")

    def update_player_info(self, player_index, money, status):
        count = 0
        status_sign = ""
        for i in range(6):
            if i == player_index-1:
                continue
            if status[i] == 0:
                status_sign = "fold"
            elif status[i] == 1:
                status_sign = "call"
            elif status[i] == 2:
                status_sign = "raise"
            elif status[i] == 3:
                status_sign = "allin"
            elif status[i] == -1:
                status_sign = "None"
            self.players_data[count].update({
                "name": i+1,
                "money": money[i],
                "status": status_sign
            })
            self.player_infos[count].setText(
                f"{i+1}\n${money[i]}\n{status_sign}"
            )
            count += 1

        self.money_label.setText(f"${money[player_index-1]}")
    
    def show_winner(self,id):
        # 建立一個警告視窗
        warning_box = QMessageBox()
        warning_box.setIcon(QMessageBox.Warning)
        warning_box.setWindowTitle('warning')
        warning_box.setText(f'winner is player {id}')
        warning_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        
        # 顯示對話框並捕獲使用者選擇
        response = warning_box.exec_()

        if response == QMessageBox.Ok:
            print("使用者選擇了 OK")
        elif response == QMessageBox.Cancel:
            print("使用者選擇了 Cancel")

    def show_rank(self,rank):
        warning_box = QMessageBox()
        warning_box.setIcon(QMessageBox.Warning)
        warning_box.setWindowTitle('rank')
        warning_box.setText(f'Your rank is : {rank}')
        warning_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        response = warning_box.exec_()

        if response == QMessageBox.Ok:
            print("使用者選擇了 OK")
        elif response == QMessageBox.Cancel:
            print("使用者選擇了 Cancel")

    def show_server_over(self):
        # 建立一個警告視窗
        warning_box = QMessageBox()
        warning_box.setIcon(QMessageBox.Warning)
        warning_box.setWindowTitle('warning')
        warning_box.setText('server is not running')
        warning_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        
        # 顯示對話框並捕獲使用者選擇
        response = warning_box.exec_()

        if response == QMessageBox.Ok:
            print("使用者選擇了 OK")
        elif response == QMessageBox.Cancel:
            print("使用者選擇了 Cancel")

    def update_card(self, card_index, card_value):
        if 0 <= card_index < len(self.top_cards):
            self.top_cards[card_index].setText(card_value)

    def update_personal_cards(self, card1, card2):
        self.card_1.setText(card1)
        self.card_2.setText(card2)

    def fold(self):
        print("fold")
        self.client.send_message({"status": "fold"})

    def call(self):
        print("call")
        self.client.send_message({"status": "call"})

    def raise_(self):
        print("raise")
        self.client.send_message({"status": "raise"})

    def allin(self):
        print("allin")
        self.client.send_message({"status": "all_in"})