from PIL import Image

import os
directory_in_str = "/home/mihaham/RussianSraporioGame/sprites/my_rect_sprites"
directory_in_str_2 = "/sprites/my_rect_sprites"
output_directory = "/home/mihaham/RussianSraporioGame/src/Objects/Resources"
directory = os.fsencode(directory_in_str)
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".png"):
        filename = filename.replace("-","_")
        os.makedirs(f"src/Objects/Resources/{filename[:-4]}", exist_ok=True)
        with open(f"{output_directory}/{filename[:-4]}/{filename[:-4]}.py", "w") as file:

            file.write(f"from src.Objects.Resources.Resources import Resources\nfrom src.logger.Logger import Logger\n\n\nclass {filename[:-4]}(Resources):\n    id: int = 0\n\n    def __init__(self) -> None:\n        Soil.id += 1\n        self.__id = Soil.id\n        super().__init__()\n        self._is_burnable = False\n        self._skin = '{directory_in_str_2}/{filename}'\n\n        Logger.add_info(f'Soil is initialized with (id - {{self.__id}})')")