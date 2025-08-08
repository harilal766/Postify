from postify.shopify.shopify_order import Shopify
from postify.environment_variables import *


class Test_Shopify():
    
    def test_order_detail(self):
        sh = Shopify(identification="40000")
        wrong_count = 0; right_count = 0
        for key, value in shopify_stores.items():
            order = sh.order_detail(
                storename=shopify_stores[key]["storename"],
                access_token=shopify_stores[key]["access_token"]
            )
            
            if order[0]["node"]["name"] == "#"+sh.identification:
                right_count += 1
            else:
                wrong_count +=1
                
        assert right_count == wrong_count