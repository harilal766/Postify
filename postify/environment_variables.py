from postify.utils import *



db_access = get_credentials(json_filename="db_access.json", env_filename="DB_ACCESS")
db_connection = db_access["connection"]
order_table = db_access["tablename"]



SHOPIFY_API_DICT = 0