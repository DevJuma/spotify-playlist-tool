from dotenv import load_dotenv
#from requests import post, get
from flask import Flask, request, url_for, session, redirect, render_template
from spotipy.oauth2 import SpotifyOAuth as SOA
import os, spotipy, time

load_dotenv()

cID = os.getenv("CLIENT_ID")
cSEC = os.getenv("CLIENT_SECRET")
host_env =  os.getenv("base_url")
port_env =  os.getenv("port")
disc_weekly = os.getenv("disc_weekly")
host_app = host_env[:-1].replace("http://",'')

rDIRuri = host_env + port_env

app = Flask(__name__)

app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'
app.secret_key = os.getenv("appSecret_key")
TOKEN_INFO = 'info'


@app.route('/')
def login():
    auth_url = create_spotify_oauth().get_authorize_url()
    return redirect(auth_url)


@app.route('/redirect')
def redirect_page():
    session.clear()
    code = request.args.get('code')
    token_info = create_spotify_oauth().get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('select_action', external = True))


@app.route('/select')
def select_action():
    if 'methode' in request.args:
        methode = request.args.get('methode')
        if(methode == "Merge_Playlists"): 
            return redirect(url_for('merge_playlists'))
        elif(methode == "Backup_Week_Discovery"):
            return redirect(url_for('save_discover_weekly'))
        else:
            return("error selecting methode!")
    else:
        return redirect(url_for("get_methode", extern = True))
    

@app.route('/getMethode')
def get_methode():
    return render_template('methode.html')


@app.route('/mergepl')
def merge_playlists():
    try:
        token_info = get_token()
    except:
        print("LOGIN ERROR")
        return redirect('/')    


@app.route('/saveDiscoverWeekly')
def save_discover_weekly():
    try:
        token_info = get_token()
    except:
        print("LOGIN ERROR")
        return redirect('/')

    bckup_wekly_pl_ID = ""
    disc_wekly_pl_ID = ""
    sp = spotipy.Spotify(auth=token_info['access_token'])
    current_playlists = sp.current_user_playlists()['items']
    userID = sp.current_user()['id']
    for playlist in current_playlists:
        if(playlist['name'] == "Discover Weekly"):
            disc_wekly_pl_ID = playlist['id']
        if(playlist['name'] == "Weekly Discovery BackUp"):
            bckup_wekly_pl_ID = playlist['id']
    
    if not disc_wekly_pl_ID:
        return 'No such Playlist'
    if not bckup_wekly_pl_ID:
        new_playlist = sp.user_playlist_create(userID,'Weekly Discovery BackUp',True)
        bckup_wekly_pl_ID = new_playlist['id']

    disc_wekly_pl = sp.playlist_items(disc_wekly_pl_ID) 
    song_uris = []
    for song in disc_wekly_pl['items']:
        song_uri = song['track']['uri']
        song_uris.append(song_uri)
    sp.user_playlist_add_tracks(userID,bckup_wekly_pl_ID,song_uris)
    return("success")

def get_token():
    token_info = session.get(TOKEN_INFO)
    if not token_info:
        redirect(url_for('login', external=False))
    now = int(time.time())
    is_expired = token_info['expires_at']- now < 60
    if(is_expired):
        spotify_oauth = create_spotify_oauth()
        token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info


def create_spotify_oauth():
    return SOA(
        client_id=cID,
        client_secret=cSEC,
        redirect_uri=url_for('redirect_page', _external=True),
        scope='user-library-read playlist-modify-public playlist-modify-private'
        )


app.run(debug=True, host=host_app, port=port_env)