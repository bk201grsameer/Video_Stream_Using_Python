import os
from pyfiglet import Figlet
import socket, cv2, pickle, struct

os.system("cls")


class Terminal:
    def __init__(self) -> None:
        self.pyf = Figlet(font="puffy")
        a = self.pyf.renderText("[+] Video Chat Without MultiThreading .")
        b = self.pyf.renderText("[+] Client")
        os.system("color B")
        print(a)


class Client:
    def __init__(self) -> None:
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_Ip = "192.168.50.251"
        self.server_Port = 8001
        try:
            self.client_socket.connect((self.server_Ip, self.server_Port))
            print(f"[+] CONNECTION SUCCEDED TO {self.server_Ip}:{self.server_Port} ✅")
            data = b""
            metadata_size = struct.calcsize("Q")
            while True:
                while len(data) < metadata_size:
                    packet = self.client_socket.recv(4 * 1024)
                    if not packet:
                        break
                    data += packet
                packed_msg_size = data[:metadata_size]
                data = data[metadata_size:]
                msg_size = struct.unpack("Q", packed_msg_size)[0]
                while len(data) < msg_size:
                    data += self.client_socket.recv(4 * 1024)
                frame_data = data[:msg_size]
                data = data[msg_size:]
                frame = pickle.loads(frame_data)
                cv2.imshow("Receiving Video", frame)
                if cv2.waitKey(1) & 0xFF == 27:  # Exit when the 'Esc' key is pressed
                    print("[+] CLIENT CLOSED CONNECTION ")
                    break
            self.client_socket.close()
            exit()
        except Exception as ex:
            print(f"[+] CONNECTION FAILED TO {self.server_Ip}:{self.server_Port} ❌")


def main():
    try:
        terminal = Terminal()
        client = Client()
    except KeyboardInterrupt:
        print("[-] OPERATION CANCELLED ❌")


main()
