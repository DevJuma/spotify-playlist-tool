from dotenv import load_dotenv
from requests import post, get
import os, base64, json

load_dotenv()

cID = os.getenv("CLIENT_ID")
cSEC = os.getenv("CLIENT_SECRET")

def get_token():
    auth_str = cID+ ":" + cSEC
    auth_base64 = str(base64.b64encode(auth_str.encode("utf-8")),"utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization" : "Basic " + auth_base64,
        "Content-Type" : "application/x-    www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    j_result = json.loads(result.content)
    return j_result["access_token"]

token = get_token()
print(token)