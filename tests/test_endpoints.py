from postify.main import Order, Pickup, Tracking
from postify.environment_variables import TEST_ORDER_IDS

order = Order()
class Test_Order():
    def test_get_order():
        for id in TEST_ORDER_IDS:
            assert order.get_order(identification=id)