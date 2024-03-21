from http_handler import HTTPHandler
from asset_creator import AssetCreator
from asset import Asset
from emailer import Emailer
from logger import Logger

if __name__ == '__main__':
    logger:Logger = Logger()
    handler:HTTPHandler = HTTPHandler()
    assetCreator:AssetCreator = AssetCreator(handler.getAsset())
    assets:list[Asset] = assetCreator.createAssets()
    asset: Asset
    logger.log("\n")
    logger.log("Begin script", True)
    for asset in assets:
        if asset.get_current_qty() <= asset.get_reorder_at_qty():
            if asset.get_order() == "":
                if (asset.set_order("ORDERED")):
                    logger.log("Asset was ordered")
                    emailer:Emailer = Emailer(asset.email_msg())
                    emailer.run()
            elif asset.get_order() != "ORDERED":
                if (asset.set_order("")):
                    logger.log(f"Asset order tag was cleared of the following unnecessary text: \"{asset.get_order()}\"")
        elif asset.get_order() != "":
            if (asset.set_order("")):
                logger.log("Quantity now acceptable, ORDERED tag was removed")
    logger.log("Script finished running")