import socket
from threading import Thread
from zlib import compress

from mss import mss



class Client:
    def __init__(self,host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        thread = Thread(target=self.retreive_screenshot)
        thread.start()

    def sendMsg(self,msg):
        self.sock.send(msg) 

    def retreive_screenshot(self):
        with mss() as sct:
           
            # The region to capture
            rect = {'top': 0, 'left': 0, 'width': 1900, 'height': 1000}

            while 'recording':
                # Capture the screen
                img = sct.grab(rect)
                # Tweak the compression level here (0-9)
                pixels = compress(img.rgb, 3)

                # Send the size of the pixels length
                size = len(pixels)
                size_len = (size.bit_length() + 7) // 8
                self.sendMsg(bytes([size_len]))

                # Send the actual pixels length
                size_bytes = size.to_bytes(size_len, 'big')
                self.sendMsg(size_bytes)

                # Send pixels
                self.sendMsg(pixels)


def main():
    try:
        client = Client('0.0.0.0',5000)
    except EOFError:
        print("aguarde "  , EOFError)
        
    
        

      


if __name__ == '__main__':
    main()