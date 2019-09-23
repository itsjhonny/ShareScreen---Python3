import socket
from threading import Thread
from zlib import compress

from mss import mss
import wx


class Client:
    def __init__(self,host, port):          
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  
    def connectServer(self):
        while 1:
            try:
                self.sock.connect((self.host, self.port))
                self.startThread()
                break            
            except:
                pass
            

    def startThread(self):
        app = wx.App(False) 
        self.screenWidth = wx.GetDisplaySize()[0]  
        self.screenHeight = wx.GetDisplaySize()[1]        
        thread = Thread(target=self.retreive_screenshot)
        thread.start()
        
       

    def sendMsg(self,msg):
        self.sock.send(msg) 

    def retreive_screenshot(self):
        with mss() as sct:
           
            # Area da tela capturada
            rect = {'top': 0, 'left': 0, 'width': self.screenWidth, 'height': self.screenHeight}

            while 'recording':
                # Capture the screen
                img = sct.grab(rect)
                # Tweak the compression level here (0-9)
                pixels = compress(img.rgb, 5)

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
    client = Client('10.1.50.201',5000)
    client.connectServer()


    
        
    
        

      


if __name__ == '__main__':
    main()