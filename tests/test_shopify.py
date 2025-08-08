from postify.shopify.shopify_order import Shopify
from postify.environment_variables import *


class Test_Shopify():
    def test_search_in_all_stores(self):
        sh = Shopify(identification="40000")
        print(sh.search_in_all_stores())
        assert sh.identification == sh.search_in_all_stores()
        