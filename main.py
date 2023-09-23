from dotenv import load_dotenv
from requests import post, get
#from flask import Flask
#from spotipy import oauth
import os, base64, json, sys, platform

load_dotenv()

cID = os.getenv("CLIENT_ID")
cSEC = os.getenv("CLIENT_SECRET")

#in work reworked to flask 