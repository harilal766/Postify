from postify.shopify.shopify_order import Shopify
from postify.environment_variables import *
import os

class Test_Shopify():
    sh = Shopify(order_id="M18184")
    with open(os.path.join(os.getcwd(),"credentials.json") ) as cred_file:
        creds = json.load(cred_file)
        
        test_shopify_store = tuple(creds["shopify_stores"].keys())[0]
        test_storename = creds["shopify_stores"][test_shopify_store]["storename"]
        test_access_token = creds["shopify_stores"][test_shopify_store]["access_token"]
        
    
    
    def test_order_detail(self):
        order = self.sh.order_detail(storename=self.test_storename, access_token=self.test_access_token)
        print(order)
        

    def test_search_in_all_stores(self):
        pass