from src.logger.Logger import Logger, GlobalObject


class GameObject(GlobalObject):

    def __get_prototipe(self, prototipe) -> None:
        pass

    def __init__(self):
        super().__init__()

        Logger.add_info(f"GameObject created")

    def get_skin(self) -> str:
        pass

    def get_type(self) -> str:
        pass
