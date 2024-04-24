from src.logger.Logger import GlobalObject


class Recipe(GlobalObject):
    def __init__(self, input={}, output={}):
        super().__init__()
        self.input_resources = input
        self.output_resources = output
