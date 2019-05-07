import os
import json
import httplib2

import google.oauth2.credentials
import google_auth_oauthlib.flow
import flask
import ssl
import requests

from requests_toolbelt.adapters import appengine
from apiclient.discovery import build
from apiclient.errors import HttpError
from google.appengine.ext import ndb
from webapp2_extras import sessions

import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    autoescape=True,
    extensions=['jinja2.ext.autoescape'])

DEVELOPER_KEY = 'AIzaSyAzUQuEdXv7iz062Ep9YjgFzDp1dZF8jJY'
LIST_LENGTH = 3
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

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

class Behavlog(ndb.Model):
    remoaddr = ndb.StringProperty(indexed=True)
    startdate = ndb.DateTimeProperty(auto_now_add=True)
    vector = ndb.JsonProperty()
    sflabel = ndb.BooleanProperty(default=False)


class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
        self.session_store = sessions.get_store(request=self.request)

        try:
            webapp2.RequestHandler.dispatch(self)
        finally:
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        return self.session_store.get_session()


class MainPage(BaseHandler):
    def get(self):

        #os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

        appengine.monkeypatch()

        self.session[str(self.request.remote_addr)] = str(self.request.remote_addr)

        log_query = Behavlog.query(Behavlog.remoaddr == str(self.request.remote_addr)).order(-Behavlog.startdate).fetch(5)

        loglist = []

        for alog in log_query:
            loglist.append(alog)

        alog = Behavlog()

        alog.remoaddr = self.session[str(self.request.remote_addr)]

        templist=[]

        for i in range(LIST_LENGTH):
            templist.append(0)

        alog.vector = templist

        alog.put()

        variables = {
        'text': 'Welcome at ' + str(self.request.remote_addr),
        'loglist': loglist
        }

        template = JINJA_ENVIRONMENT.get_template('templates/welcome.html')
        self.response.write(template.render(variables))


class YouTubeShow(BaseHandler):
    def get(self):

        try:
            whoswho = self.session[str(self.request.remote_addr)]

            log_query = Behavlog.query(Behavlog.remoaddr == str(self.request.remote_addr)).order(-Behavlog.startdate).fetch(1)

            thislog = None

            onlyone = True
            for alog in log_query:
                if onlyone:
                    thislog = alog
                    onlyone = False

            thislog.vector[1] = 1

            try:

                youtube = build(YOUTUBE_API_SERVICE_NAME,YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)
                searchlist = youtube.search().list(q='Google Official',part='id,snippet',maxResults=5).execute()

                videos = []
                playlists = []

                for item in searchlist.get('items',[]):
                    if item['id']['kind'] == 'youtube#video':
                        videos.append('%s' % (item['id']['videoId']))
                    elif item['id']['kind'] == 'youtube#playlist':
                        playlists.append('%s' % (item['id']['playlistId']))

                self.session['videoid'] = videos[0]

                self.redirect('/main/player')

                #template_vars = {
                #    'name' : whoswho,
                #    'videos' : videos
                #}

                #template = JINJA_ENVIRONMENT.get_template('templates/youtube.html')
                #self.response.write(template.render(template_vars))

            except HttpError, e:
                thislog.sflabel = True
                self.response.write('<html><body><p>http error</p></body></html>')
            finally:
                thislog.put()

        except KeyError:
            self.response.status_int = 401
            self.response.write('<html><body><p>401 unauthorized access</p></body></html>')


class PlayList(BaseHandler):
    def get(self):
        try:
            whoswho = self.session[str(self.request.remote_addr)]

            log_query = Behavlog.query(Behavlog.remoaddr == str(self.request.remote_addr)).order(-Behavlog.startdate).fetch(1)

            thislog = None

            onlyone = True
            for alog in log_query:
                if onlyone:
                    thislog = alog
                    onlyone = False

            thislog.vector[2] = 1

            try:

                pPlaylistid = self.session['playlistId']

                youtube = build(YOUTUBE_API_SERVICE_NAME,YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)
                plistitems = youtube.playlistItems().list(playlistId=pPlaylistid,part='id,snippet',maxResults=5).execute()

                videos = []

                for item in plistitems.get('items',[]):
                    if item.get('snippet').get('resourceId').get('kind') == 'youtube#video':
                        print item.get('snippet').get('resourceId').get('videoId')
                        videos.append('%s' % (item.get('snippet').get('resourceId').get('videoId')))
                        
                self.session['videoid'] = videos[0]

                self.redirect('/main/YouTubePlayer')

            except HttpError, e:
                thislog.sflabel = True
                self.response.write('<html><body><p>http error</p></body></html>')
            finally:
                thislog.put()

        except KeyError:
            self.response.status_int = 401
            self.response.write('<html><body><p>401 unauthorized access</p></body></html>')


class YouTubePlayer(BaseHandler):
    def get(self):
        videoid = self.session['videoid']
        template_vars = {
                    'name' : 'my',
                    'youtubesrc' : ('http://www.youtube.com/embed/'+videoid)
                }
        template = JINJA_ENVIRONMENT.get_template('templates/player2.html')
        self.response.write(template.render(template_vars))


class GetChannelActivities(BaseHandler):
    def get(self):
        try:
            whoswho = self.session[str(self.request.remote_addr)]

            log_query = Behavlog.query(Behavlog.remoaddr == str(self.request.remote_addr)).order(-Behavlog.startdate).fetch(1)

            thislog = None

            onlyone = True
            for alog in log_query:
                if onlyone:
                    thislog = alog
                    onlyone = False

            thislog.vector[0] = 1

            try:

                youtube = build(YOUTUBE_API_SERVICE_NAME,YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)
                activitylist = youtube.channels().list(part='snippet,contentDetails',mySubscribers=True,id='UCK8sQmJBp8GCxrOtXWBpyEA').execute()
                
                print json.dumps(activitylist)

            except HttpError, e:
                thislog.sflabel = True
                self.response.write('<html><body><p>http error</p></body></html>')
            finally:
                thislog.put()

        except KeyError:
            self.response.status_int = 401
            self.response.write('<html><body><p>401 unauthorized access</p></body></html>')


class Authorized(BaseHandler):
    def get(self):
        #print(self.request.url)
        state = self.request.get('state')
        print(state)
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secret.json', scopes=['https://www.googleapis.com/auth/youtube'],state=state)
        flow.redirect_uri = 'https://localhost:1338/main/red'
        authorization_response = self.request.url
        flow.fetch_token(authorization_response=authorization_response)
        credentials = flow.credentials
        self.session['credentials'] = credentials_to_dict(credentials)

        self.redirect('/main/comein')


class OauthPage(BaseHandler):
    def get(self):
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secret.json', scopes=['https://www.googleapis.com/auth/youtube'])

        flow.redirect_uri = 'https://localhost:1338/main/red'

        auth_url, state = flow.authorization_url(access_type='offline')
        #,prompt='consent'

        print(auth_url)

        self.redirect(str(auth_url))


class OauthReq(BaseHandler):
    def get(self):
        if 'credentials' not in self.session:
            return self.redirect('/main/oauth')
        self.redirect('/main/')


class History(BaseHandler):
    def get(self):
        credentials = google.oauth2.credentials.Credentials(**self.session['credentials'])

        youtube = build(YOUTUBE_API_SERVICE_NAME,YOUTUBE_API_VERSION,credentials=credentials)

        historylist = youtube.channels().list(part='snippet',mine='true').execute()

        print json.dumps(historylist)


app = webapp2.WSGIApplication([
    ('/main/', MainPage),
    ('/main/comein',OauthReq),
    ('/main/youtube', YouTubeShow),
    ('/main/player', YouTubePlayer),
    ('/main/activities', GetChannelActivities),
    ('/main/oauth', OauthPage),
    ('/main/red', Authorized),
    ('/main/playlist', PlayList),
    ('/main/history', History)
], config=sconfig, debug=True)