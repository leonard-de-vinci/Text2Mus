import json
import sys
import google.oauth2.credentials

import YoutubeSearch

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

DEVELOPER_KEY = "REPLACE_ME"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

commenturl = 'https://www.googleapis.com/youtube/v3/commentThreads'
searchurl = 'https://www.googleapis.com/youtube/v3/search'

class YoutubeVideo():
    def __init__(self, id):

        return


class SearchQuery():
    def __init__(self, query, max_res):
        self.q = query
        self.max_results = max_res
    def search(self):
        YoutubeSearch.youtube_search(self)


dodo = SearchQuery("bonobo",15)
dodo.search()