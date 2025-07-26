import sys, requests
from postify.environment_variables import shopify_stores

class Shopify:
    def __init__(self,identification : str):
        self.order_id_pattern = r'#\d{4,5}'
        self.identification = identification
        self.shopify_dict = shopify_stores
        
    def handle_stores(self):
        order = None
        try:
            for store in self.shopify_dict.items():
                order = self.order_detail(
                    storename=store["storename"],
                    access_token=store["access_token"]
                ).json()
                
        except Exception as e:
            print(e)
        else:
            return order
    
    def order_detail(self, storename : str, access_token : str):
        if not access_token:
            sys.exit("No access token")
        headers = {
            "Content-Type" : 'application/json',
            "X-Shopify-Access-Token" : access_token
        }; version = "2025-04"
        base_url = f"https://{storename}.myshopify.com/admin/api/{version}/graphql.json"
        try:
            shopify_basic_query = """
                    query {
                        orders(first:1, query: "%s", sortKey: CREATED_AT, reverse: true) {
                            edges {
                                node {
                                    name
                                    phone
                                    billingAddress {
                                        firstName
                                        phone
                                    }
                                    displayFulfillmentStatus
                                    statusPageUrl
                                }
                            }
                        }
                    }
                    """ % self.identification
                    
            response = requests.post(
                base_url,headers=headers, json = {"query" : shopify_basic_query}
            )
        except requests.RequestException as re:
            print(re)
        except Exception as e:
            print(e)
        else:
            return response