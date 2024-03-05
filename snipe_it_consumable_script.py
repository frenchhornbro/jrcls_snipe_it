from http_handler import HTTPHandler
from asset_creator import AssetCreator
from asset import Asset
from emailer import Emailer
if __name__ == '__main__':
    handler:HTTPHandler = HTTPHandler()
    assetCreator:AssetCreator = AssetCreator(handler.getJsonStr())
    assets:list[Asset] = assetCreator.createAssets()
    asset: Asset
    for asset in assets:
        # TODO: Test that each message prints when intended
        if asset.get_current_qty() <= asset.get_reorder_at_qty():
            if asset.get_order() == "":
                emailer:Emailer = Emailer(asset.email_msg())
                emailer.run()
                asset.set_order("ORDERED")
                print("Asset Ordered")
            elif asset.get_order() != "ORDERED":
                asset.set_order("")
                print(f"Asset order tag cleared of the following unnecessary text: \"{asset.get_order()}\"")
        elif asset.get_order() != "":
            asset.set_order("")
            print("Quantity now acceptable, ORDERED tag removed")
                