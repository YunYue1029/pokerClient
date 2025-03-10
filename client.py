import socket
import json
import time

PORT = 8888
HOST = '127.0.0.1'

class Client_Socket:
    def __init__(self):
        self.host = HOST
        self.port = PORT
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

    def send_message(self, message):
        try:
            self.client_socket.send(json.dumps(message).encode('utf-8'))
        except Exception as e:
            print(f"Error sending message: {e}")

    def receive_message(self):
        try:
            data = self.client_socket.recv(1024).decode('utf-8')
            if not data:
                time.sleep(1.0)
                return self.receive_message()
            data = json.loads(data)
        except json.JSONDecodeError:
            self.client_socket.send(json.dumps({"status": "error", "message": "Invalid data format."}).encode('utf-8'))
        return data
    def receive_messages_add(self):
        """接收消息並放入佇列，處理粘包"""
        buffer = ""  # 緩存未處理的數據
        try:
            while True:
                data = self.player.socket.recv(1024).decode('utf-8')
                if not data:
                    continue
                
                # 將數據添加到緩存
                buffer += data
                
                # 根據分隔符分割消息
                while "\n" in buffer:
                    # 分離出完整的消息
                    message, buffer = buffer.split("\n", 1)
                    try:
                        # 將 JSON 解析後放入佇列
                        parsed_message = json.loads(message)
                        self.message_queue.put(parsed_message)
                    except json.JSONDecodeError:
                        print(f"Failed to decode message: {message}")
        except Exception as e:
            print(f"Error receiving message: {e}")
    
    def stop(self):
        try:
            disconnect_message = {"status": "disconnect"}
            self.send_message(disconnect_message)
            self.socket.close()
        except Exception as e:
            print(f"Error during disconnection: {e}")
        self.client_socket.close()
        