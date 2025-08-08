from postify.shopify.shopify_order import Shopify
from postify.environment_variables import *


class Test_Shopify():
    def test_search_in_all_stores(self):
        sh = Shopify(order_id="40858")
        print(sh.search_in_all_stores())
        assert sh.order_id == sh.search_in_all_stores()
        