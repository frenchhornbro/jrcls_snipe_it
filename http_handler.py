import requests

class HTTPHandler:
    def __init__(self) -> None:
        self.url:str = "https://jrcb-snipe-it.byu.edu/api/v1/consumables"
        self.token:str = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzOTMiLCJqdGkiOiIyMWNmY2ExNzFjZjQ3OGQ1MzY0OTI4Mjk1MjRkY2JkOWQ1NTE4OGVjNTkzOGRlODRhN2YxYTM4Yjc4OGY4M2QwYzcyNmYwOTU1MmM3MWZmNyIsImlhdCI6MTcwOTIzNzAxOCwibmJmIjoxNzA5MjM3MDE4LCJleHAiOjIwMjQ4NTYyMTgsInN1YiI6IjY4MCIsInNjb3BlcyI6W119.gwtsjkWZ30kBVSIObK7fQBpoPdjJkxaxtMr2gBtqeWrQL5gi1u9ZsT4eZkZw0eiGqZkd2oQU4GxbV94bYcf01cSyY9r28gMufou7L1DEABM8fuv_pObsZ8SITKueEO5xF143BTTol-9JXbE3X--BSNYMsYgL6QWPs4q-NsHVPdiEE_nMaQZj5fCWZRYPspCfuvS6D6JG2IOIMZcs7ioueAHfvA_ekW8lj5JUAdiPuQi7hJ3bxVpEADF2RwvPf9gROxVCp2GY_XCLRye-9EIZvwYFJJmJM6906anJB0WooymM7sKC5RahZi43Md59pyi6VZHW71qwBeq9qJNQVV_lDYY64low4jlB7SL77CZcWQt46CANL3acVDSaKA5yndchM2Eir0tOcmWKLGo-EZev4KhUtyVPAWfNOHbZvD4xNqiSMqCaxX8IAA-yDykOXxlxNnUmED6VFxF_L9sj2uq2TKH8d2P3_6yj5XF2ySYDnkwvm2bgA-thy2gSkrXmrlxM8uIJdc_tQD_WRp8ojmyJe4fu6rnWbiM-jR_rOATJZYkwDrFAT6Ri-_mqKk6ms2zqmr4RN05K-uOh5GjNSeCiZWqZwC97DRLhPqLMPT42qLD_vxuKc8A8dhK0g1yn-RRrZzH_E8blpEQQbnjuR6RiJ0QFkPhQ5WmW9LoW37u_Pms"
        
    
    def getJsonStr(self) -> str:
        try:
            headers = {
                "accept": "application/json",
                "Authorization": f"{self.token}"
                }
            response = requests.get(self.url, headers=headers)
            json_str_input:str = str(response.text)
            return json_str_input
        except Exception as e:
            print(f'SNAP! Doing this throws an error:\n\t"{e}"')
    
    def putJsonStr(self, id:int, name:str, categ_name:str, order:str, qty:int) -> None:
        #TODO: Just get all data for the asset so it can be repopulated, this will make the script a little more future-proof
        try:
            url = self.url + f"/{id}"
            category = {
                "name" : f"{categ_name}"
            }
            payload = {
                "name": f"{name}",
                "category": category,
                "order_number": f"{order}",
                "qty": qty
                }
            headers = {
                "accept": "application/json",
                "Authorization": f"{self.token}",
                "content-type": "application/json"
                }
            response = requests.put(url, json=payload, headers=headers)
            print(response.text)
        except Exception as e:
            print(f'SHUCKS! Doing this throws an error:\n\t"{e}"')