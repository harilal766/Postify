import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 
from postify.database_managing.models import Scheduled_Order
from postify.environment_variables import TEST_ORDER_IDS

inst = Scheduled_Order()
date = "2025-08-16"
class Test_Scheduled_Order:
    def __init__(self):
        self.scheduled_order = Scheduled_Order()
    
    def test_find_all_entry_timestamps(self):
        timestamps = self.scheduled_order.find_all_entry_timestamps()
        assert timestamps
        assert type(timestamps) == list
    
    def test_is_despatched_and_bagged(self):
        assert self.scheduled_order
        
    def test_find_scheduled_order(self):
        for id in TEST_ORDER_IDS:
            assert self.scheduled_order.find_scheduled_order(
                id=id
            )
    
    