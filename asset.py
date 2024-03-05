from fsas.fsa import FSA
from fsas.fsa_null import Null
from fsas.fsa_id import ID
from fsas.fsa_model import Model
from fsas.fsa_model_number import ModelNumber
from fsas.fsa_curr_qty import CurrQuantity
from fsas.fsa_reorder_at_qty import ReorderAtQuantity
from fsas.fsa_category import Category
from fsas.fsa_order import Order
from fsas.fsa_item_type import ItemType
from fsas.fsa_total_qty import TotalQuantity
from http_handler import HTTPHandler

class Asset:
    def __init__(self, json_input:str) -> None:
        self.input: str = json_input
        self.id:int = -1
        self.current_qty:int = Null
        self.total_qty:int = Null
        self.reorder_at_qty:int = Null
        self.qty_to_order:int = 1000
        self.model:str = ""
        self.item_name:str = ""
        self.product_number:str = ""
        self.order:str = ""
        self.__populate_attributes__()

    # Regex for categories
    #       Model: after the first "name" in the asset
    #        Item type: after the "name" in "category" in the asset
    #       Product Number: after "model_number"
    #       Current Quantity: after "remaining" in the asset
    #       Reorder At Quantity: after "min_amt" in the asset
    
    def __populate_attributes__(self) -> None:
        currInput:str = self.input
        inputExhausted:bool = False
        nameScanned:bool = False
        idScanned:bool = False
        inCategory:bool = False
        id:ID = ID()
        model:Model = Model()
        model_number:ModelNumber = ModelNumber()
        tot_qty:TotalQuantity = TotalQuantity()
        curr_qty:CurrQuantity = CurrQuantity()
        re_at_qty:ReorderAtQuantity = ReorderAtQuantity()
        category:Category = Category()
        order:Order = Order()
        item_type:ItemType = ItemType()
        # Rather than pass this in char by char, pass in the whole string and delete it as
        while not inputExhausted:
            if id.passesTest(currInput) and not idScanned:
                idScanned = True
                currInput = self.__updateCurrInput__(currInput, id)
                self.id = self.__getAttributeNumVal__(currInput)
            elif model.passesTest(currInput) and not nameScanned:
                nameScanned = True
                currInput = self.__updateCurrInput__(currInput, model)
                self.model = self.__getAttributeVal__(currInput)
            elif item_type.passesTest(currInput) and inCategory:
                inCategory = False
                currInput = self.__updateCurrInput__(currInput, item_type)
                self.item_name = self.__getAttributeVal__(currInput)
            elif category.passesTest(currInput):
                inCategory = True
                currInput = currInput[1:]
            elif tot_qty.passesTest(currInput):
                currInput = self.__updateCurrInput__(currInput, tot_qty)
                self.total_qty = self.__getAttributeNumVal__(currInput)
            elif model_number.passesTest(currInput):
                currInput = self.__updateCurrInput__(currInput, model_number)
                self.product_number = self.__getAttributeVal__(currInput)
            elif curr_qty.passesTest(currInput):
                currInput = self.__updateCurrInput__(currInput, curr_qty)
                self.current_qty = self.__getAttributeNumVal__(currInput)
            elif re_at_qty.passesTest(currInput):
                currInput = self.__updateCurrInput__(currInput, re_at_qty)
                self.reorder_at_qty = self.__getAttributeNumVal__(currInput)
            elif order.passesTest(currInput):
                currInput = self.__updateCurrInput__(currInput, order)
                self.order = self.__getAttributeVal__(currInput)
            else:
                currInput = currInput[1:]
            if len(currInput) == 0:
                inputExhausted = True

    def __updateCurrInput__(self, currInput:str, fsa:FSA) -> str:
        return currInput[fsa.numDel():]

    def __getAttributeVal__(self, currInput:str) -> str:
        numApostrophes:int = 0
        retStr:str = ""
        nullTester:Null = Null()
        fullyParsed:bool = False

        while not fullyParsed:
            if not currInput: return "Parse Error, ran out of chars"
            if nullTester.passesTest(currInput): return "null"
            if currInput[0] == '"':
                numApostrophes += 1
            else:
                retStr += currInput[0]
            currInput = currInput[1:]
            if numApostrophes >= 2:
                fullyParsed = True
        return retStr
    
    def __getAttributeNumVal__(self, currInput:str) -> int:
        fullyParsed:bool = False
        retInt:int = 0
        while not fullyParsed:
            if not currInput: return "Parse Error, ran out of chars"
            if currInput[0].isdecimal():
                retInt *= 10
                retInt += int(currInput[0])
            elif currInput[0] == ',':
                fullyParsed = True
            currInput = currInput[1:]
        return retInt

    def get_current_qty(self) -> int:
        return self.current_qty
    
    def get_reorder_at_qty(self) -> int:
        return self.reorder_at_qty
    
    def get_order(self) -> str:
        return self.order
    
    def set_order(self, input:str) -> None:
        handler:HTTPHandler = HTTPHandler()
        handler.putJsonStr(self.id, self.model, self.item_name, input, self.total_qty)
    
    def to_string(self) -> str:
        model:str = "Model: " + self.model
        item_name:str = "Item Name: " + self.item_name
        product_number:str = "Product Number: " + self.product_number
        current_qty:str = "Current Quantity: " + str(self.current_qty)
        reorder_at_qty:str = "Reorder At Quantity: " + str(self.reorder_at_qty)
        qty_to_order:str = "Quantity to Order: " + str(self.qty_to_order)
        order:str = "Ordered: " + self.order
        input:str =  "JSON input: " + self.input

        return model + "\n" + item_name + "\n" + product_number + "\n" + current_qty + "\n" + reorder_at_qty + "\n" + qty_to_order + "\n" + order + "\n" + input + "\n\n"
    
    def email_msg(self) -> str:
        return f"Our printer supply for the following model(s) is low:\n\t* Model: {self.model}, Item Type: {self.item_name}, Product Number: {self.product_number}, Quantity to order: {self.qty_to_order}, The current quantity is: {self.current_qty}"