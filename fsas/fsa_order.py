from .fsa import FSA

class Order(FSA):
    
    def __init__(self) -> None:
        self.testStr: str = '"order_number":'