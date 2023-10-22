import os
from pyfiglet import Figlet
import socket, cv2, pickle, struct
import imutils
import threading
import sys

os.system("cls")
exit_flag = False


class Terminal:
    def __init__(self) -> None:
        self.pyf = Figlet(font="puffy")
        a = self.pyf.renderText("[+] Video Chat Without MultiThreading .")
        b = self.pyf.renderText("[+] Server")
        os.system("color E")
        print(a)
        print(b)


class Server:
    def __init__(self) -> None:
        self.server_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_Ip = "192.168.50.251"
        print(f"[+] SERVER IP :> {self.server_Ip}")
        self.server_Port = 8001
        self.socketsArr = []
        self.control_Thread = None

        try:
            self.server_Socket.bind((self.server_Ip, self.server_Port))
            print("[+] BIND SUCCESS ✅")
            self.server_Socket.listen(4)
            print(f"[+] SERVER LISTENING AT {self.server_Ip}:{self.server_Port} ✅")
        except Exception as ex:
            print("[+] SOMETHING WENT WRONG .. ")

    def handle_client(self):
        global exit_flag
        try:
            vid = cv2.VideoCapture(1)
            while vid.isOpened():
                ret, image = vid.read()
                image = imutils.resize(image, width=320)
                img_serialize = pickle.dumps(image)
                message = struct.pack("Q", len(img_serialize)) + img_serialize

                for client_Socket in self.socketsArr:
                    try:
                        client_Socket.sendall(message)
                    except Exception as ex:
                        print("[+] The connection to the socket is closed")
                        if client_Socket in self.socketsArr:
                            print("[+] Removing client socket")
                            self.socketsArr.remove(client_Socket)
                cv2.imshow("Video from Server", image)

                if cv2.waitKey(1) & 0xFF == 27:
                    print("[+] CLOSING THE SERVER ..")
                    for client_Socket in self.socketsArr:
                        client_Socket.close()
                    exit_flag = True
                    break

        except Exception as ex:
            print("[+] SOMETHING WENT WRONG")
            print(str(ex))

    def start(
        self,
    ):
        while True:
            self.server_Socket.settimeout(1)
            try:
                client_Socket, addr = self.server_Socket.accept()
                print("[+] Connected to : ", addr)
                self.socketsArr.append(client_Socket)
                if self.control_Thread == None:
                    self.control_Thread = threading.Thread(target=self.handle_client)
                    self.control_Thread.start()
            except socket.timeout:
                if exit_flag == True:
                    self.control_Thread.join()
                    print("[+] Exiting The Program\n")
                    sys.exit()
            except Exception as ex:
                print("[+] SOMETHING WENT WRONG")
                print(str(ex))


def main():
    try:
        terminal = Terminal()
        server = Server()
        server.start()
    except KeyboardInterrupt:
        print("[-] OPERATION CANCELLED ❌")


main()
