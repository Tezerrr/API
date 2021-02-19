import os

import pygame as pg
import sys, requests
from PIL import Image
from io import BytesIO

pg.init()
coords = input()
spn = input()
w = requests.get(f"https://static-maps.yandex.ru/1.x/?ll={coords}&spn={spn}&l=sat&z=20")
pg.display.set_caption('Маша_Редиска№1_Льоньа')
Image.open(BytesIO(w.content)).save('image.png')
w = pg.image.load('image.png')
size = w.get_size()
screen = pg.display.set_mode(size)

while True:
    screen.blit(w, (0, 0))
    for i in pg.event.get():
        if i.type == pg.QUIT:
            if "image.png":
                os.remove("image.png")
            sys.exit()
    pg.display.flip()