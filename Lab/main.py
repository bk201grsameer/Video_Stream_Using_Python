from vidstream import CameraClient
from vidstream import StreamingServer
import threading
import time

def main():
    receiving = StreamingServer("192.168.50.251", 8001)
    sending = CameraClient("192.168.50.190", 8001)

    try:
        t1 = threading.Thread(target=receiving.start_server)
        t1.start()
        time.sleep(2)
        t2 = threading.Thread(target=sending.start_stream)
        t2.start()

        while input("") != "STOP":
            continue

        receiving.stop_server()
        sending.stop_stream()
    except KeyboardInterrupt:
        print("[+] OPERATION CANCELLED \n")


main()
