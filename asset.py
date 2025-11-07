import json
from http_handler import HTTPHandler

class Asset:
    def __init__(self, input: str) -> None:
        self.input = json.loads(input)
        self.id: int = self.input["id"]
        self.currQty: int = self.input["remaining"]
        self.totalQty: int = self.input["qty"]
        self.reorderAtQty: int = self.input["min_amt"]
        self.model: str = self.input["name"]
        self.itemName: str = self.input["category"]["name"]
        self.productNum: str = self.input["model_number"]
        self.order: str = self.input["order_number"]
        self.qtyToOrder: int = max(self.reorderAtQty + 1 - self.currQty, 0)
    
    def set_order(self, ordered: str) -> bool:
        handler: HTTPHandler = HTTPHandler()
        return handler.patchAsset(self.id, self.currQty, ordered, self.productNum, self.model)
    
    def to_string(self) -> str:
        id: int = "ID: " + str(self.id)
        model: str = "Model: " + self.model
        item_name: str = "Item Name: " + self.itemName
        product_number: str = "Product Number: " + self.productNum
        current_qty: str = "Current Quantity: " + str(self.currQty)
        reorder_at_qty: str = "Reorder At Quantity: " + str(self.reorderAtQty)
        qty_to_order: str = "Quantity to Order: " + str(self.qtyToOrder)
        order: str = "Ordered: " + self.order
        input: str =  "JSON input: " + self.input

        return id + "\n" + model + "\n" + item_name + "\n" + product_number + "\n" + current_qty + "\n" + reorder_at_qty + "\n" + qty_to_order + "\n" + order + "\n" + input + "\n\n"
    
    def email_msg(self) -> str:
        return f"Our printer supply for the following model(s) is low:\n\t* Model: {self.model}, Item Type: {self.itemName}, Product Number: {self.productNum}, Quantity to order: {self.qtyToOrder}, The current quantity is: {self.currQty}"