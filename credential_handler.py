from credential_storage import CredentialStorage

class CredentialHandler:
    def run(self) -> str:
        input:list[int] = CredentialStorage().pwd
        retStr:str = ""
        for i in range(len(input)):
            input[i] -= 17
            input[i] /= 13
            retStr += chr(int (input[i]))
        return retStr
    
    def generatelist(self, input:str):
        output:list[int] = []
        for char in input:
            output.append(ord(char)*13+17)
        print(output)

if __name__ == '__main__':
    input = input("Input a string to convert: ")
    cred:CredentialHandler = CredentialHandler()
    cred.generatelist(input)