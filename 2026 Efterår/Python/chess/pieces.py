import globals as GL

class Piece:
    def __init__(self, tp:str, plc:tuple):
        self._piece_type:str = tp
        self._placement:tuple = plc

    @property
    def piece_type(self):
        return self._piece_type

    @piece_type.setter
    def piece_type(self, tp:str):
        self._piece_type = tp

    @property
    def placement(self):
        return self._placement
    
    @placement.setter
    def placement(self, plc:tuple):
        self._placement = plc

def init_pieces():
    pass