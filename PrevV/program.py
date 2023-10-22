import subprocess
import sys
from pytube import YouTube
import os


class Downloader:
    def __init__(self, url) -> None:
        self.yt = YouTube(url)
        self.title = self.yt.title
        self.views = self.yt.views

    def download(self):
        try:
            print("[+] DOWNLOAD STARTED....")
            vidstreams = self.yt.streams.get_highest_resolution()
            print("[+] DOWNLOADING....")
            vidstreams.download(os.getcwd())
            print("[+] DOWNLOAD COMPLETE....")
        except Exception as ex:
            print("[+] SOMETHING WENT WRONG WHILE DOWNLOADING....")

    def on_progress(self, stream, chunk, file_handle, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size) * 100
        print(f"Downloaded: {percentage:.2f}%")


def main():
    if len(sys.argv) != 2:
        print("[+] USAGE python program.py url")
        return
    url = sys.argv[1]
    downloader = Downloader(url)
    print("[+] TILE :", downloader.title)
    print("[+] Views :", downloader.views)
    downloader.download()
    pass


if __name__ == "__main__":
    main()
