import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from postify.environment_variables import *
from postify.main import *
from postify.environment_variables import TEST_ORDER_IDS

def test_origins():
    http_count = 0
    for origin in ALLOWED_ORIGINS:
        if "http" in origin:
            http_count += 1
    assert len(ALLOWED_ORIGINS) == http_count
    
def test_get_order():
    for id in TEST_ORDER_IDS:
        order = get_order(identification=id)
        assert order
        
    

