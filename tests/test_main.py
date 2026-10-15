import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from postify.environment_variables import *
from postify.main import *


class Test_Order():
    order_instance = Order()
    
    def test_get_order(self):
        order_detail = self.order_instance.get_order(identification="S151576")    
        print(order_detail)
        assert order_detail


def test_origins():
    http_count = 0
    for origin in ALLOWED_ORIGINS:
        if "http" in origin:
            http_count += 1
    assert len(ALLOWED_ORIGINS) == http_count
    
    
    

