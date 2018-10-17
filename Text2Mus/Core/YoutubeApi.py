import json
import sys
import google.oauth2.credentials

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow


commenturl = 'https://www.googleapis.com/youtube/v3/commentThreads'
searchurl = 'https://www.googleapis.com/youtube/v3/search'

class YoutubeVideo():
    def __init__(self, id, jsondata):
        return



class YoutubeApi():
    def __init__(self):
        return
    def YoutubeSearch(self, name):
        return
    def getComments(self,video):
        return