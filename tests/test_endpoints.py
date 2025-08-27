from postify.main import Order, Pickup, Tracking
from postify.environment_variables import TEST_ORDER_IDS


class Test_Order():
    order = Order()
    
    def test_get_order(self):
        for id in TEST_ORDER_IDS:
            assert id