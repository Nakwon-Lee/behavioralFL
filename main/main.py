import os
import json
import httplib2

import google.oauth2.credentials
import google_auth_oauthlib.flow
import flask
import ssl
import requests

import Keys

from BaseHandler import BaseHandler
from BehaveLog import Behavlog

from requests_toolbelt.adapters import appengine
from apiclient.discovery import build
from apiclient.errors import HttpError
from google.appengine.ext import ndb
from webapp2_extras import sessions

import webapp2
import jinja2

from R_Player import YouTubePlayer
from R_Video import R_Video
from R_Playlist import R_Playlist
from R_PlaylistItems import R_PlayListItems

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    autoescape=True,
    extensions=['jinja2.ext.autoescape'])

LIST_LENGTH = 3

sconfig = {}
sconfig['webapp2_extras.sessions'] = {'secret_key':'472405203058'}

#export OAUTHLIB_INSECURE_TRANSPORT=1

#DEFAULT_LOGSET_NAME = 'behavelogset'


#def logset_key(logset_name=DEFAULT_LOGSET_NAME):
#
#    return ndb.Key('Logset', logset_name)

def credentials_to_dict(credentials):
    return {'token':credentials.token,
            'refresh_token':credentials.refresh_token,
            'token_uri':credentials.token_uri,
            'client_id':credentials.client_id,
            'client_secret':credentials.client_secret,
            'scopes':credentials.scopes}


class MainPage(BaseHandler):
    def get(self):

        #os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

        appengine.monkeypatch()

        self.session[str(self.request.remote_addr)] = str(self.request.remote_addr)

        alog = Behavlog()

        alog.remoaddr = self.session[str(self.request.remote_addr)]

        templist=[]

        for i in range(LIST_LENGTH):
            templist.append(0)

        alog.vector = templist

        alog.put()

        self.redirect('/main/welcome')


class Welcome(BaseHandler):
    def get(self):
        log_query = Behavlog.query(Behavlog.remoaddr == str(self.request.remote_addr)).order(-Behavlog.startdate).fetch(5)

        loglist = []

        for alog in log_query:
            loglist.append(alog)
        
        videoid = 'none'

        if 'videoid' in self.session:
            videoid = self.session['videoid']

        playlistid = 'none'

        if 'playlistId' in self.session:
            playlistid = self.session['playlistId']

        variables = {
        'text': 'Welcome at ' + str(self.request.remote_addr),
        'videoid': videoid,
        'playlistid': playlistid,
        'loglist': loglist
        }

        template = JINJA_ENVIRONMENT.get_template('templates/welcome.html')
        self.response.write(template.render(variables))


class CentralPut(BaseHandler):
    def post(self):
        self.session['command'] = self.request.get('command')
        self.redirect('/main/maineventhandler')


class MainEventHandler(BaseHandler):
    def get(self):
        if self.session['command'] == 'video':
            self.redirect('/main/video')
        elif self.session['command'] == 'playlists':
            self.redirect('/main/playlist')
        elif self.session['command'] == 'playlistitem':
            self.redirect('/main/playlistitem')
        elif self.session['command'] == 'playlistitemin':
            self.redirect('/main/playlistitem')
        elif self.session['command'] == 'playlistitemdel':
            self.redirect('/main/playlistitem')


class Authorized(BaseHandler):
    def get(self):
        #print(self.request.url)
        state = self.request.get('state')
        print(state)
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secret.json', scopes=['https://www.googleapis.com/auth/youtube'],state=state)
        #flow.redirect_uri = 'https://localhost:1338/main/red'
        flow.redirect_uri = 'http://localhost:8080/main/red'
        authorization_response = self.request.url
        flow.fetch_token(authorization_response=authorization_response)
        credentials = flow.credentials
        self.session['credentials'] = credentials_to_dict(credentials)

        self.redirect('/main/comein')


class OauthPage(BaseHandler):
    def get(self):
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secret.json', scopes=['https://www.googleapis.com/auth/youtube'])

        #flow.redirect_uri = 'https://localhost:1338/main/red'
        flow.redirect_uri = 'http://localhost:8080/main/red'

        auth_url, state = flow.authorization_url(access_type='offline')
        #,prompt='consent'

        print(auth_url)

        self.redirect(str(auth_url))


class OauthReq(BaseHandler):
    def get(self):
        if 'credentials' not in self.session:
            return self.redirect('/main/oauth')
        self.redirect('/main/main')


app = webapp2.WSGIApplication([
    ('/main/main', MainPage),
    ('/main/welcome', Welcome),
    ('/main/comein',OauthReq),
    ('/main/oauth', OauthPage),
    ('/main/red', Authorized),
    ('/main/centralput', CentralPut),
    ('/main/maineventhandler', MainEventHandler),
    ('/main/player', YouTubePlayer),
    ('/main/video', R_Video),
    ('/main/playlist', R_Playlist),
    ('/main/playlistitem', R_PlayListItems)
], config=sconfig, debug=True)