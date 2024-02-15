from .fsa import FSA

class ReorderAtQuantity(FSA):
    
    def __init__(self) -> None:
        self.testStr: str = '"min_amt":'