from PIL import Image

import os
directory_in_str = "/home/mihaham/RussianSraporioGame/sprites/graphics/icons/"
directory = os.fsencode(directory_in_str)
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".png"):
        im = Image.open(f'/home/mihaham/RussianSraporioGame/sprites/graphics/icons/{filename}')
        im.show()
        im_crop = im.crop((0, 0, 64, 64))
        im_crop.save(f'my_rect_sprites/{filename}')