import os
from pyfiglet import Figlet
import socket, cv2, pickle, struct
import imutils


os.system("cls")


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
        try:
            self.server_Socket.bind((self.server_Ip, self.server_Port))
            print("[+] BIND SUCCESS ✅")
            self.server_Socket.listen(1)
            print(f"[+] SERVER LISTENING AT {self.server_Ip}:{self.server_Port} ✅")
        except Exception as ex:
            print("[+] SOMETHING WENT WRONG .. ")

    def start(
        self,
    ):
        while True:
            try:
                client_Socket, addr = self.server_Socket.accept()
                print("[+] Connected to : ", addr)
                if client_Socket:
                    vid = cv2.VideoCapture(1)
                    while vid.isOpened():
                        ret, image = vid.read()
                        image = imutils.resize(image, width=320)
                        img_serialize = pickle.dumps(image)
                        message = struct.pack("Q", len(img_serialize)) + img_serialize
                        client_Socket.sendall(message)
                        cv2.imshow("Video from Server", image)
                        if (
                            cv2.waitKey(1) & 0xFF == 27
                        ):  # Exit when the 'Esc' key is pressed
                            print("[+] CLOSING THE SERVER ..")
                            client_Socket.close()
                            exit(1)
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
