from dotenv import load_dotenv
from requests import post, get
import os, base64, json, sys, platform

load_dotenv()

cID = os.getenv("CLIENT_ID")
cSEC = os.getenv("CLIENT_SECRET")

def clear_cml():
    if(str(platform.system())=="Windows"):
        os.system('cls')
    else:
        os.system('clear')

def get_token():
    auth_str = cID+ ":" + cSEC
    auth_base64 = str(base64.b64encode(auth_str.encode("utf-8")),"utf-8")
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization" : "Basic " + auth_base64,
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    j_result = json.loads(result.content)
    return j_result["access_token"]

def bearer_header():
    token = get_token()
    return {"Authorization": "Bearer " + token}

def req_userdata_get(url, headers):
    j_data = get(url,headers=headers)
    if j_data.status_code == 200:
       result = json.loads(j_data.content)
       return result
    else:
        #prints error message 
        print("Error:", result.status_code, result.text)
        sys.exit() #if request was invalide exits script 


def select_playlist():
    current_user_ID = select_user()
    url = f"https://api.spotify.com/v1/users/{current_user_ID}/playlists"
    headers = bearer_header()
    playlist_ids = []
    clear_cml()
    print(current_user_name+"s Playlists:")
    #counter for total playlists
    playlist_count = 0
    while url:
        results = req_userdata_get(url, headers)
        for playlist in results['items']:
            playlist_id = playlist["id"]
            playlist_ids.append(playlist_id)
            playlist_name = playlist["name"]
            print(f"{str(playlist_count+1)}. Playlist Name: {playlist_name}, ID: {playlist_id}")
            playlist_count += 1
        #checks for next page to get all playlists
        url = results.get('next')
    select = int(input())-1
    if (select<len(playlist_ids) and select > 0):
        return playlist_ids[select]
    else:
        print("selection out of range")
        sys.exit()


def select_user():
    print("You can find a Users ID in the Profile URL example: https://open.spotify.com/user/xxx\n")
    userID= input("Enter a Spotify userID to search for: ")
    #checking if user id is valide
    url = f"https://api.spotify.com/v1/users/{userID}"
    headers = bearer_header()
    result = req_userdata_get(url, headers)
    global current_user_name 
    current_user_name = result["display_name"]
    return userID #returning user id for later use
    
def gen_playlist(id_one, id_two):
    url = "https://api.spotify.com/v1/users/{id_one}/playlists"
    new_playlist_name = input("Name of new playlist: ")
    token = get_token()
    bearer = f'Bearer {token}'  # Remove 'Authorization:' prefix
    new_playlist_dscpt = input("New playlist description:\n")
    headers = {
        "Authorization": bearer,  
        "Content-Type": "application/json"
    }
    data = {
        "name": new_playlist_name,
        "description": new_playlist_dscpt,
        "public": True
    }
    result = post(url, headers=headers, json=data)
    if(result.status_code==200):
        print("nice")
    else:
        print("not nice\n" + result.text)


def merg_playlist():
    print("User one: ")
    playlist_id_one = select_playlist()
    clear_cml()
    print("User two: ")
    playlist_id_two = select_playlist()
    clear_cml()
    gen_playlist(playlist_id_one, playlist_id_two)


merg_playlist()