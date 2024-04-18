from src.Objects.Resources.Resources import Resources
from src.logger.Logger import Logger


class discharge_defense_equipment_controller(Resources):
    id: int = 0

    def __init__(self) -> None:
        Soil.id += 1
        self.__id = Soil.id
        super().__init__()
        self._is_burnable = False
        self._skin = '/sprites/my_rect_sprites/discharge_defense_equipment_controller.png'

        Logger.add_info(f'Soil is initialized with (id - {self.__id})')