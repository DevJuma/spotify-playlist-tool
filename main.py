from dotenv import load_dotenv as l_de
from requests import post, get
import os, base64

l_de()

cID = os.getenv("CLIENT_ID")
cSEC = os.getenv("CLIENT_SECRET")

def get_token():
    auth_str = cID+ ":" + cSEC
    auth_base64 = str(base64.b64encode(auth_str.encode("utf-8")),"utf-8")
    