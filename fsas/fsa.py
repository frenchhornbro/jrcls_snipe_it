class FSA:
    
    def __init__(self) -> None:
        self.testStr:str = ''
    
    def passesTest(self, currInput:str) -> bool:
        return self.__recursiveTest__(currInput, self.testStr)
    
    def numDel(self) -> int:
        return len(self.testStr)
    
    def __recursiveTest__(self, input:str, testStr:str) -> bool:
        if not testStr:
                return True
        if input and input[0] == testStr[0]:
            return self.__recursiveTest__(input[1:], testStr[1:])
        return False