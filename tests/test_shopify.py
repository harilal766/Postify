from postify.shopify.shopify_order import Shopify
from postify.environment_variables import *


class Test_Shopify():
    sh = Shopify(order_id="S58065")
    
    def test_order_detail(self):
        order = self.sh.order_detail()
        

    def test_search_in_all_stores(self):
        pass