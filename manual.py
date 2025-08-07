from postify.shopify.shopify_order import Shopify
import re


from postify.database_managing.models import Scheduled_Order


so = Scheduled_Order()

order = so.find_scheduled_order(id="#40700")


print(order.Order_ID)