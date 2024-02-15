from .fsa import FSA

class Null(FSA):
    
    def __init__(self) -> None:
        self.testStr: str = 'null'