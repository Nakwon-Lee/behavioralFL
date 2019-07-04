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
from R_Search import R_Search
from R_Playlist import R_Playlist
from R_PlaylistItems import R_PlayListItems
from R_Channels import R_Channels
from R_ChannelSections import R_ChannelSections
from R_Videos import R_Videos
from R_Caption import R_Caption
from R_CommentThread import R_CommentThread
from R_Comment import R_Comment
from R_Activity import R_Activity
from R_ChannelBanner import R_ChannelBanner

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    autoescape=True,
    extensions=['jinja2.ext.autoescape'])

LIST_LENGTH = 37

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

        self.session['cstate'] = 0

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

        channelid = 'none'

        if 'channel' in self.session:
            channelid = self.session['channel']

        uploadsid = 'none'

        if 'uploads' in self.session:
            uploadsid = self.session['uploads']

        playlistitemid = 'none'

        if 'playlistitemid' in self.session:
            playlistitemid = self.session['playlistitemid']

        videotitle = 'none'

        if 'videotitle' in self.session:
            videotitle = self.session['videotitle']

        captionid = 'none'

        if 'captionid' in self.session:
            captionid = self.session['captionid']

        cmtthdid = 'none'

        if 'cmtthdid' in self.session:
            cmtthdid = self.session['cmtthdid']

        commentid = 'none'

        if 'commentid' in self.session:
            commentid = self.session['commentid']

        activityid = 'none'

        if 'activityid' in self.session:
            activityid = self.session['activityid']

        bannerurl = 'none'

        if 'bannerurl' in self.session:
            bannerurl = self.session['bannerurl']

        currstate = 0

        if 'cstate' in self.session:
            currstate = self.session['cstate']

        variables = {
        'text': 'Welcome at ' + str(self.request.remote_addr),
        'state': currstate,
        'videoid': videoid,
        'videotitle': videotitle,
        'cmtthdid': cmtthdid,
        'activityid': activityid,
        'bannerurl': bannerurl,
        'commentid': commentid,
        'playlistid': playlistid,
        'playlistitemid': playlistitemid,
        'uploadsid': uploadsid,
        'captionid': captionid,
        'loglist': loglist,
        'channelid' : channelid
        }

        template = JINJA_ENVIRONMENT.get_template('templates/welcome.html')
        self.response.write(template.render(variables))

        if self.session['cstate'] == 14:
            self.redirect('/main/comein')

class CentralPut(BaseHandler):
    def post(self):
        self.session['command'] = self.request.get('command')
        self.redirect('/main/maineventhandler')


class MainEventHandler(BaseHandler):
    def get(self):
        if self.session['command'] == 'search':
            self.redirect('/main/search')
        elif self.session['command'] == 'playlists':
            self.redirect('/main/playlist')
        elif self.session['command'] == 'playlistsnew':
            self.redirect('/main/playlist')
        elif self.session['command'] == 'playlistsupdate':
            self.redirect('/main/playlist')
        elif self.session['command'] == 'playlistsrm':
            self.redirect('/main/playlist')
        elif self.session['command'] == 'playlistitem':
            self.redirect('/main/playlistitem')
        elif self.session['command'] == 'playlistitemin':
            self.redirect('/main/playlistitem')
        elif self.session['command'] == 'playlistitemdel':
            self.redirect('/main/playlistitem')
        elif self.session['command'] == 'playlistitemupdate':
            self.redirect('/main/playlistitem')
        elif self.session['command'] == 'channels':
            self.redirect('/main/channels')
        elif self.session['command'] == 'channelsec':
            self.redirect('/main/channelsections')
        elif self.session['command'] == 'channelsecin':
            self.redirect('/main/channelsections')
        elif self.session['command'] == 'channelsecdel':
            self.redirect('/main/channelsections')
        elif self.session['command'] == 'channelsecup':
            self.redirect('/main/channelsections')
        elif self.session['command'] == 'videos':
            self.redirect('/main/videos')
        elif self.session['command'] == 'videosin':
            self.redirect('/main/videos')
        elif self.session['command'] == 'videosrm':
            self.redirect('/main/videos')
        elif self.session['command'] == 'videosup':
            self.redirect('/main/videos')
        elif self.session['command'] == 'captions':
            self.redirect('/main/captions')
        elif self.session['command'] == 'captionsin':
            self.redirect('/main/captions')
        elif self.session['command'] == 'captionsdw':
            self.redirect('/main/captions')
        elif self.session['command'] == 'captionsrm':
            self.redirect('/main/captions')
        elif self.session['command'] == 'captionsup':
            self.redirect('/main/captions')
        elif self.session['command'] == 'cmtthds':
            self.redirect('/main/cmtthds')
        elif self.session['command'] == 'cmtthdsin':
            self.redirect('/main/cmtthds')
        elif self.session['command'] == 'cmtthdsup':
            self.redirect('/main/cmtthds')
        elif self.session['command'] == 'comments':
            self.redirect('/main/comments')
        elif self.session['command'] == 'commentsin':
            self.redirect('/main/comments')
        elif self.session['command'] == 'commentsup':
            self.redirect('/main/comments')
        elif self.session['command'] == 'commentsrm':
            self.redirect('/main/comments')
        elif self.session['command'] == 'activities':
            self.redirect('/main/activity')
        elif self.session['command'] == 'activitiesin':
            self.redirect('/main/activity')
        elif self.session['command'] == 'channelbanner':
            self.redirect('/main/channelbanner')
        elif self.session['command'] == 'channelsup':
            self.redirect('/main/channels')
        elif self.session['command'] == 'guideCategory':
            self.redirect('/main/channelbanner')
        else:
            self.response.status_int = 401
            self.response.write('<html><body><p>401 unauthorized access</p></body></html>')


class Authorized(BaseHandler):
    def get(self):
        #print(self.request.url)
        state = self.request.get('state')
        print(state)
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secret.json', scopes=['https://www.googleapis.com/auth/youtube.force-ssl'],state=state)
        #flow.redirect_uri = 'https://localhost:1338/main/red'
        flow.redirect_uri = 'http://localhost:8080/main/red'
        authorization_response = self.request.url
        flow.fetch_token(authorization_response=authorization_response)
        credentials = flow.credentials
        self.session['credentials'] = credentials_to_dict(credentials)

        self.redirect('/main/comein')


class OauthPage(BaseHandler):
    def get(self):
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secret.json', scopes=['https://www.googleapis.com/auth/youtube.force-ssl'])

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
        self.session['cstate'] = 14
        self.redirect('/main/welcome')


app = webapp2.WSGIApplication([
    ('/main/main', MainPage),
    ('/main/welcome', Welcome),
    ('/main/comein',OauthReq),
    ('/main/oauth', OauthPage),
    ('/main/red', Authorized),
    ('/main/centralput', CentralPut),
    ('/main/maineventhandler', MainEventHandler),
    ('/main/player', YouTubePlayer),
    ('/main/search', R_Search),
    ('/main/playlist', R_Playlist),
    ('/main/playlistitem', R_PlayListItems),
    ('/main/channels', R_Channels),
    ('/main/channelsections', R_ChannelSections),
    ('/main/videos', R_Videos),
    ('/main/captions', R_Caption),
    ('/main/cmtthds', R_CommentThread),
    ('/main/comments', R_Comment),
    ('/main/activity', R_Activity),
    ('/main/channelbanner', R_ChannelBanner)
], config=sconfig, debug=True)