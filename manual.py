from postify.shopify.shopify_order import Shopify
import re

sh = Shopify(identification="6304")

print(sh.handle_stores())