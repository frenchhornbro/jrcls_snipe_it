from asset import Asset
import json

class AssetCreator:
    def __init__(self, json_input: str) -> None:
        self.input: str = json_input
    
    def createAssets(self) -> list[Asset]:
        return [Asset(json.dumps(asset)) for asset in json.loads(self.input)["rows"]]