from asset import Asset

class AssetCreator:
    def __init__(self, json_input:str) -> None:
        self.input:str = json_input
        self.assets:list[Asset] = []
    
    def createAssets(self) -> list[Asset]:
        # Produce the list of assets and populate all the quantities and strings
        char:str
        asset_json_str:str = ""
        leftCurlyBraceScanned:bool = False
        dataStarted:bool = False
        numLeftCurlyBraces:int = 0
        numRightCurlyBraces:int = 0
        assetJustRecorded:bool = False

        for char in self.input:
            if dataStarted or (leftCurlyBraceScanned and char == '{'):
                if char == '{':
                    numLeftCurlyBraces += 1
                    dataStarted = True
                elif char == '}':
                    numRightCurlyBraces += 1
                if numLeftCurlyBraces == numRightCurlyBraces and numRightCurlyBraces != 0:
                    #We want to not record a comma once this code has been run
                    asset_json_str += char
                    self.assets.append(Asset(asset_json_str))
                    numLeftCurlyBraces = 0
                    numRightCurlyBraces = 0
                    asset_json_str = ""
                    assetJustRecorded = True
                    # Create all the assets, and then within each asset use the whole string to parse out the data we want.
                elif not assetJustRecorded or not char == ',':
                    asset_json_str += char
                else:
                    assetJustRecorded = False
            elif char == '{':
                leftCurlyBraceScanned = True

        return self.assets
    
    # Model             Consumable Name
    # Current qty       Quantity
    # Reorder at qty    Min. QTY
    # Qty to order      1
    # Item name         Catgeory?
    # Product number    Model No.?