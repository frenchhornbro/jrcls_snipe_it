from .fsa import FSA

class TotalQuantity(FSA):
    
    def __init__(self) -> None:
        self.testStr: str = '"qty":'