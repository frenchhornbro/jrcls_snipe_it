import time
import datetime
import json
from pathlib import Path
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
    asset:Asset
    logger.log("\n", True, True)
    logger.log("Begin script", True)


    compFolderPath:Path = Path("comparison")
    compLogPath:Path = Path("comparison/comparison.txt")
    if (not compLogPath.exists()):
        compFolderPath.mkdir(parents=True)
        with open(compLogPath, 'w') as compareFile:
            print("Comparison file created")

    weeklyLogPath:Path = Path("log/weekly-asset-log.txt")
    if (not weeklyLogPath.exists()):
        with open(weeklyLogPath, 'a') as file:
            file.write('{:%Y-%b-%d}'.format(datetime.datetime.now()))

    currIDs:dict = {}

    for asset in assets:
        logger.compareAsset(weeklyLogPath, compLogPath, asset.id, asset.model, asset.itemName, asset.productNum, asset.currQty, asset.reorderAtQty, asset.qtyToOrder, asset.order)
        currIDs[asset.id] = asset.id
        if asset.currQty <= asset.reorderAtQty:
            if asset.order == "":
                if (asset.set_order("ORDERED")):
                    logger.log(f"Asset {asset.productNum} was ordered")
                    emailer:Emailer = Emailer(asset.email_msg())
                    emailer.run()
                    time.sleep(5) #Without this Jira freaks out and can take up to 30 minutes to actually receive the email and run its end of the script
            elif asset.order != "ORDERED":
                if (asset.set_order("")):
                    logger.log(f"Order field for the asset {asset.productNum} was cleared of the following unnecessary text: \"{asset.order}\"")
        elif asset.order != "":
            if (asset.set_order("")):
                logger.log(f"Quantity now acceptable for asset {asset.productNum}, ORDERED tag was removed")


    compStr:str = ""
    with open(compLogPath, 'r') as compareFile:
        compStr = compareFile.read()
    compJSON:dict = json.loads(compStr)

    # Log deleted assets
    for oldID in compJSON:
        if not currIDs[oldID]:
            logger.logDeletion(weeklyLogPath, oldID, oldID['model'], oldID['currQty'])

    if False:
        #TODO: If it has been a week (tell by reading line), send the email (containing the weeklyLogFile) and remove the file ./log/weekly-asset-log.txt
        weeklyLogPath.unlink() #This deletes the file
    logger.log("Script finished running")