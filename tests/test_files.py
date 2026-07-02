import json


credentials = {
    "shopify_stores" : [
        {"subdomain" : "","access_token":""}    
    ],
    "database" : {
        "connection_string" : "", "tablename" : ""
    },
    "testing_values" : {},
    "postify" : {}
}

credential_filename = "postify_credentials.json"

with open (credential_filename,"w+") as cred_file:
    json.dump(credentials,cred_file,indent=4)


