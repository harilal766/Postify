import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from postify.database import * 
import pytest
from postify.environment_variables import *


class Test_Database:
    def test_db_variables(self):
        assert type(db_access) == dict
        assert db_connection
        assert "orders" in order_table.lower()
        
    def test_db_connection(self):
        pass
    
    
    
    
    