import json, os
from dotenv import load_dotenv

def get_credentials(json_filename,env_filename):
    credentials = None
    try:
        if json_filename in os.listdir():
            with open(json_filename,"r") as json_file:
                credentials = json.load(json_file)
        else:
            load_dotenv()
            credentials = json.loads(os.getenv(env_filename))
    except json.JSONDecodeError as je:
        print(f"Json Error : {je}")
    except Exception as e:
        print(e)
    else:
        return credentials
    
    
def html_reader(html_file):
    html_text = None
    try:
        available_files = os.listdir("postify/")
        if html_file in available_files:
            with open(f"postify/{html_file}","r", encoding="utf-8") as html:
                html_text = html.read()
    except Exception as e:
        print(e)
    else:
        return html_text
