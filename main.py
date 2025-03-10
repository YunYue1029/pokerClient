import sys
import threading
from PyQt5.QtWidgets import QApplication, QStackedWidget
from PyQt5.QtCore import pyqtSignal
from login_screen import LoginScreen
from main_screen import MainScreen
from client import Client_Socket

class MainApp(QStackedWidget):
    update_pot_signal = pyqtSignal(int)
    update_player_info_signal = pyqtSignal(int, list, list)
    update_current_turn_signal = pyqtSignal(int,int)
    winner_signal = pyqtSignal(int)
    server_over_signal = pyqtSignal()
    show_rank_signal = pyqtSignal(str)
    update_player_two_card_signal = pyqtSignal(str, str)
    update_card_3_signal = pyqtSignal(str,str,str)
    update_card_4_signal = pyqtSignal(str)
    update_card_5_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.player = Client_Socket()

        self.init_ui()
        threading.Thread(target=self.run, daemon=True).start()

        self.player_id = 0
        self.my_status = 0
        self.player_money = [0]*6
        self.player_status = [0]*6
        self.pot = 0
        self.game_round = ""
        self.current_turn = 0

        self.card_1 = ''
        self.card_2 = ''
        self.server_card = [''] * 5

    def init_ui(self):
        self.login_screen = LoginScreen(self.player)
        self.main_screen = MainScreen(self.player)

        self.addWidget(self.login_screen)
        self.addWidget(self.main_screen)
        self.setCurrentWidget(self.login_screen)
        self.login_screen.login_successful.connect(self.show_main_screen)

        self.update_pot_signal.connect(self.main_screen.update_pot)
        self.update_player_info_signal.connect(self.main_screen.update_player_info)
        self.update_current_turn_signal.connect(self.main_screen.update_current_player)
        self.update_player_two_card_signal.connect(self.main_screen.update_player_two_card)
        self.update_card_3_signal.connect(self.main_screen.update_card_3)
        self.update_card_4_signal.connect(self.main_screen.update_card_4)
        self.update_card_5_signal.connect(self.main_screen.update_card_5)

        self.winner_signal.connect(self.main_screen.show_winner)
        self.server_over_signal.connect(self.main_screen.show_server_over)
        self.show_rank_signal.connect(self.main_screen.show_rank)

    def show_main_screen(self):
        self.setCurrentWidget(self.main_screen)

    def run(self):
        try:
            while True:
                message = self.player.receive_message()
                if not message:
                    continue
                print(message)
                if 'status' in message:
                    status = message.get("status")
                else:
                    continue
                if status == "server_stop":
                    print("Server requested to stop.")
                    self.main_screen.show_server_over()
                    self.close()
                    break
                if status == "login_success":
                    self.player_id = message.get("id")
                    break
            print("login success")
            self.show_main_screen()
            while True:
                while True:
                    message = self.player.receive_message()
                    print(message)
                    if not message:
                        continue
                    status = message.get("status")
                    if status == 'wait_for_player':
                        continue
                    if status == "server_stop":
                        print("Server requested to stop.")
                        self.server_over_signal.emit()
                        self.close()
                        break
                    if status == "game_start":
                        self.player_status = message.get("player_status")
                        self.player_money = message.get("player_money")
                        break
                print(self.player_id)
                while True:
                    message = self.player.receive_message()
                    print(message)
                    if not message:
                        continue
                    status = message.get("status")

                    if 'player_money' in message:
                        self.player_money = message.get("player_money")
                    if 'player_status' in message:
                        self.player_status = message.get("player_status")
                        self.my_status = self.player_status[self.player_id-1]
                    if 'pot' in message:
                        self.pot = message.get("pot")
                        self.update_pot_signal.emit(self.pot)
                    
                    self.update_player_info_signal.emit(self.player_id, self.player_money, self.player_status)
                    if status == "server_stop":
                        print("Server requested to stop.")
                        self.server_over_signal.emit()
                        self.close()
                        break
                    elif status == 'wait':
                        print("wait")
                        self.current_turn = message.get("player")
                        self.update_current_turn_signal.emit(self.current_turn,self.player_id)
                    elif status == 'round_0':
                        self.game_round = 0
                        self.current_turn = self.player_id
                        self.update_current_turn_signal.emit(self.current_turn,self.player_id)
                        self.card_1 = message.get("card_1")
                        self.card_2 = message.get("card_2")
                        self.update_player_two_card_signal.emit(self.card_1, self.card_2)
                    elif status == 'round_1':
                        self.game_round = 1
                        self.current_turn = self.player_id
                        self.update_current_turn_signal.emit(self.current_turn,self.player_id)
                        print("choose")
                        while True:
                            if self.my_status == 3:
                                break
                            elif self.my_status == 0:
                                break
                            message = self.player.receive_message()
                            if message.get("status") == 'OK':
                                break
                    elif status == 'round_2':
                        self.game_round = 2
                        self.current_turn = self.player_id
                        self.update_current_turn_signal.emit(self.current_turn,self.player_id)
                        self.server_card[0] = message.get("server_card_1")
                        print(self.server_card[0])
                        self.server_card[1] = message.get("server_card_2")
                        self.server_card[2] = message.get("server_card_3")
                        self.update_card_3_signal.emit(self.server_card[0], self.server_card[1], self.server_card[2])
                    elif status == 'round_3':
                        self.game_round = 3
                        self.current_turn = self.player_id
                        self.update_current_turn_signal.emit(self.current_turn,self.player_id)
                        print("choose")
                        while True:
                            if self.my_status == 3:
                                break
                            elif self.my_status == 0:
                                break
                            message = self.player.receive_message()
                            if message.get("status") == 'OK':
                                break
                    elif status == 'round_4':
                        self.game_round = 4
                        self.current_turn = self.player_id
                        self.update_current_turn_signal.emit(self.current_turn,self.player_id)
                        self.server_card[3] = message.get("server_card_4")
                        self.update_card_4_signal.emit(self.server_card[3])
                    elif status == 'round_5':
                        self.game_round = 5
                        self.current_turn = self.player_id
                        self.update_current_turn_signal.emit(self.current_turn,self.player_id)
                        print("choose")
                        while True:
                            if self.my_status == 3:
                                break
                            elif self.my_status == 0:
                                break
                            message = self.player.receive_message()
                            if message.get("status") == 'OK':
                                break
                    elif status == 'round_6':
                        self.game_round = 6
                        self.current_turn = self.player_id
                        self.update_current_turn_signal.emit(self.current_turn,self.player_id)
                        self.server_card[4] = message.get("server_card_5")
                        self.update_card_5_signal.emit(self.server_card[4])
                    elif status == 'round_7':
                        self.game_round = 7
                        self.current_turn = self.player_id
                        self.update_current_turn_signal.emit(self.current_turn,self.player_id)
                        print("choose")
                        while True:
                            if self.my_status == 3:
                                break
                            elif self.my_status == 0:
                                break
                            message = self.player.receive_message()
                            if message.get("status") == 'OK':
                                break
                    elif status == 'round_8':
                        self.game_round = 8
                        self.current_turn = self.player_id
                        self.update_current_turn_signal.emit(self.current_turn,self.player_id)
                        rank = message.get("hand_rank")
                        if rank == '0':
                            self.show_rank_signal.emit("Hight card")
                            print("High card")
                        elif rank == 'P':
                            self.show_rank_signal.emit("One pair")
                            print("One pair")
                        elif rank == '2P':
                            self.show_rank_signal.emit("two pair")
                            print("Two pair")
                        elif rank == '3':
                            self.show_rank_signal.emit("Three of a kind")
                            print("Three of a kind")
                        elif rank == 'S':
                            self.show_rank_signal.emit("Stright")
                            print("Straight")
                        elif rank == 'FL':
                            self.show_rank_signal.emit("Flush")
                            print("Flush")
                        elif rank == 'H':
                            self.show_rank_signal.emit("Full House")
                            print("Full house")
                        elif rank == 'F':
                            self.show_rank_signal.emit("Four of a kind")
                            print("Four of a kind")
                        elif rank == 'FS':
                            self.show_rank_signal.emit("Straight flush")
                            print("Straight flush")
                        else:
                            print("None")
                    elif status == 'check_winner':
                        print("check_winner")
                        winner = message.get("winner")
                        if winner == self.player_id:
                            print("You win")
                            self.winner_signal.emit(winner)
                        else:
                            self.winner_signal.emit(winner)
                            print(f"Winner is {winner}")
                        
                        break

                    print(self.game_round)
                    print(self.current_turn)
                    print(self.card_1)
                    print(self.card_2)
                    print(self.server_card)

                print("reset")
                self.card_1 = ''
                self.card_2 = ''
                self.server_card = [''] * 5
                self.update_card_3_signal.emit('gray_back', 'gray_back', 'gray_back')
                self.update_card_4_signal.emit('gray_back')
                self.update_card_5_signal.emit('gray_back')
                
        except Exception as e:
            print(f"Error receiving message: {e}")

    def closeEvent(self, event):
        try:
            self.player.send_message({"status":"fold"})
            self.player.stop()
            print("Disconnected from server.")
        except Exception as e:
            print(f"Error during disconnection: {e}")
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.setWindowTitle("Poker")
    main_app.setGeometry(100, 100, 400, 300)
    main_app.show()
    sys.exit(app.exec_())