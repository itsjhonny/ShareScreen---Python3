import socket
from zlib import decompress
import os
import pygame
from pygame.locals import *

WIDTH = 1366
HEIGHT = 768


def recvall(conn, length):
    """ Retreive all pixels. """

    buf = b''
    while len(buf) < length:
        data = conn.recv(length - len(buf))
        if not data:
            return data
        buf += data
    return buf


def main(host='10.1.50.201', port=5000):
    pygame.init()
    screen = pygame.display.set_mode((800,600),HWSURFACE|DOUBLEBUF|RESIZABLE)
    clock = pygame.time.Clock()
    watching = True
    changed = False    

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    orig = (host, port)
    sock.bind(orig)
    sock.listen(1)
       
    while 'connected':
        conn, cliente = sock.accept()
        print ('Concetado por', cliente)
        try:
            while watching:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        watching = False
                        break 
                    elif event.type == pygame.VIDEORESIZE:
                        print("screen rezise")
                        screen=pygame.display.set_mode(event.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE)
                        changed = True               

                # Retreive the size of the pixels length, the pixels length and pixels
                size_len = int.from_bytes(conn.recv(1), byteorder='big')

                size = int.from_bytes(recvall(conn, size_len), byteorder='big')
                pixels = decompress(recvall(conn, size))

                # Create the Surface from raw pixels
                img = pygame.image.fromstring(pixels, (WIDTH, HEIGHT), 'RGB')

                # Display the picture
                screen.blit(img, (0, 0))
                pygame.display.flip()
                clock.tick(60)
        finally:
            sock.close()


if __name__ == '__main__':
    main()