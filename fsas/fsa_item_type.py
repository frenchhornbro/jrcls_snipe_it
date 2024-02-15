from .fsa import FSA

class ItemType(FSA):
    
    def __init__(self) -> None:
        self.testStr: str = '"name":'