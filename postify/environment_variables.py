from postify.utils import *

credentials = get_credentials(json_filename="credentials.json", env_filename="CREDENTIALS")

db_access = credentials["database"]
db_connection = db_access["connection"]
order_table = db_access["tablename"]

shopify_stores = credentials["shopify_stores"]

API_KEY = credentials["security"]["api_key"]
ALLOWED_ORIGINS = credentials["security"]["origins"]


"""
TEST_VALUES = credentials["test_values"]
TEST_ORDER_IDS = TEST_VALUES["order_ids"]
"""