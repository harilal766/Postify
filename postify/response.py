import re

class Tracking_Response:
    def __init__(self,name, id, mobile,status):
        self.customer_name = name
        self.order_id = id
        self.mobile = mobile
        self.status = status
        self.tracking_link = self.tracking_link()
        
    def tracking_link(self):
        link = "Will be available after despatching."
        try:
            barcode_pattern = r'EL\d{9}IN'
            barcode_match = re.search(barcode_pattern,self.status)
            if barcode_match:
                link = f"https://app.indiapost.gov.in/enterpriseportal/track-result/article-number/{barcode_match.group()}"
        except Exception as e:
            print(e)
        else:
            return link
    