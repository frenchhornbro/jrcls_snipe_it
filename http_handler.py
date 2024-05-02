import requests
import json
from credential_storage import CredentialStorage
from logger import Logger

class HTTPHandler:
    def __init__(self) -> None:
        self.url:str = "https://jrcb-snipe-it.byu.edu/api/v1/consumables"
        creds:CredentialStorage = CredentialStorage()
        self.token:str = creds.apiToken
        self.logger:Logger = Logger()
        
    
    def getAsset(self) -> str:
        try:
            headers = {
                "accept": "application/json",
                "Authorization": f"{self.token}"
                }
            response = requests.get(self.url, headers=headers)
            json_str_input:str = str(response.text)
            return json_str_input
        except Exception as e:
            self.logger.log(f'ERROR:\t"{e}"')
    
    def patchAsset(self, id:int, currQty:int, ordered:str, productNum:str, model:str) -> bool:
        try:
            url = self.url + f"/{id}"
            payload = {
                "order_number": f"{ordered}",
                "remaining": currQty
            }
            headers = {
                "accept": "application/json",
                "Authorization": f"{self.token}",
                "content-type": "application/json"
                }
            encodedResponse = requests.patch(url, json=payload, headers=headers)
            decodedResponse = json.loads(encodedResponse.text)
            self.logger.log(f'UPDATE:\tID: {id}, Name: {model}, Model No: {productNum}: + {decodedResponse["messages"]}')
            return True

        except Exception as e:
            self.logger.log(f'ERROR:\t"{e}"')
            return False