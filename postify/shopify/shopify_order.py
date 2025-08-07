import sys, requests
import re
from postify.environment_variables import shopify_stores

class Shopify:
    def __init__(self,identification : str):
        self.order_id_pattern = r'#?\d{4,5}'
        self.identification = identification
        self.shopify_dict = shopify_stores
        
    def search_in_all_stores(self):
        unscheduled_order = None
        try:
            for store, store_dict in self.shopify_dict.items():
                order = self.order_detail(
                    storename=store_dict["storename"],
                    access_token=store_dict["access_token"]
                )
                if order != []:
                    unscheduled_order = order[0]
                    break

        except Exception as e:
            print(e)
        else:
            return unscheduled_order
    
    def order_detail(self, storename : str, access_token : str):
        if not access_token:
            sys.exit("No access token")
        headers = {
            "Content-Type" : 'application/json',
            "X-Shopify-Access-Token" : access_token
        }; version = "2025-04"
        base_url = f"https://{storename}.myshopify.com/admin/api/{version}/graphql.json"
        response = None
        try:
            shopify_basic_query = """
                    query {
                        orders(first:1, query: "%s", sortKey: CREATED_AT, reverse: true) {
                            edges {
                                node {
                                    name
                                    createdAt
                                    displayFulfillmentStatus
                                    billingAddress{
                                        name
                                        phone
                                    }
                                }
                            }
                        }
                    }
                    """ % self.identification
            
            if re.match(self.order_id_pattern, self.identification):
                response = requests.post(
                    base_url, headers=headers,json = {"query" : shopify_basic_query}
                )
                order = response.json()["data"]["orders"]["edges"]
        except requests.RequestException as e:
            print(e)
        except Exception as e:
            print(e)
        else:
            if response.status_code == 200:
                return order       
            