import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from UI_searching import Ui_MainWindow
import pygame as pg
import sys, requests
from PIL import Image
from io import BytesIO

pg.init()
all_sprites = pg.sprite.Group()

coords = list(map(float, input().split(',')))
z = int(input())
count_map = 0
type_maps = ['map', 'sat', 'sat,skl']


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pg.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def main():
    w = requests.get(f"https://static-maps.yandex.ru/1.x/?"
                     f"ll={','.join(list(map(str, coords)))}&z={z}&l={type_maps[count_map % 3]}")
    pg.display.set_caption('Маша_Редиска№1_Льоньа')
    Image.open(BytesIO(w.content)).save('image.png')
    return pg.image.load('image.png')

def qt_start_search():
    app = QApplication(sys.argv)
    ex = MySearch()
    ex.show()
    app.exec()

class MySearch(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Поиск')


class Search(pg.sprite.Sprite):
    def __init__(self):
        super(Search, self).__init__(all_sprites)
        self.image = load_image('search.png')
        self.rect = self.image.get_rect()
        self.rect.x = size[0]
        self.rect.y = 0

    def update(self, pos):
        if self.rect.collidepoint(pos):
            qt_start_search()


w = main()
size = w.get_size()
screen = pg.display.set_mode((size[0] + 50, size[1]))
Search()
while True:
    screen.blit(w, (0, 0))
    for i in pg.event.get():
        if i.type == pg.QUIT:
            if "image.png":
                os.remove("image.png")
            sys.exit()
        if i.type == pg.KEYDOWN:
            if i.key == pg.K_w and z > 0:
                z -= 1
                w = main()
            if i.key == pg.K_e and z < 23:
                z += 1
                w = main()
            if i.key == pg.K_LEFT and coords[0] > -180:
                coords = [coords[0] - (1 / z), coords[1]]
                w = main()
            if i.key == pg.K_RIGHT and coords[0] < 180:
                coords = [coords[0] + (1 / z), coords[1]]
                w = main()
            if i.key == pg.K_UP and coords[1] < 85:
                coords = [coords[0], coords[1] + (1 / z)]
                w = main()
            if i.key == pg.K_DOWN and coords[1] > -85:
                coords = [coords[0], coords[1] - (1 / z)]
                w = main()
            if i.key == pg.K_q:
                count_map += 1
                w = main()
        if i.type == pg.MOUSEBUTTONDOWN:
            all_sprites.update(i.pos)
    all_sprites.draw(screen)
    pg.display.flip()
