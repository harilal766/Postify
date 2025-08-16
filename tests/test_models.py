import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 
from postify.database_managing.models import Scheduled_Order

inst = Scheduled_Order()
date = "2025-08-16"
class Test:
    def test_filter_with_entry(self):
        shipment = inst.filtered_shipment(entry_date=date)
        assert shipment