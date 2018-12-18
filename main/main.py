
import os

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

#DEFAULT_LOGSET_NAME = 'behavelogset'


#def logset_key(logset_name=DEFAULT_LOGSET_NAME):
#
#    return ndb.Key('Logset', logset_name)

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
                searchlist = youtube.search().list(q='BTS',part='id,snippet',maxResults=5).execute()

                videos = []

                for item in searchlist.get('items',[]):
                    if item['id']['kind'] == 'youtube#video':
                        videos.append('%s' % (item['snippet']['title']))

                template_vars = {
                    'name' : whoswho,
                    'videos' : videos
                }

                template = JINJA_ENVIRONMENT.get_template('templates/youtube.html')
                self.response.write(template.render(template_vars))

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
        template_vars = {
                    'name' : 'my'
                }
        template = JINJA_ENVIRONMENT.get_template('templates/player.html')
        self.response.write(template.render(template_vars))


app = webapp2.WSGIApplication([
    ('/main/', MainPage),
    ('/main/youtube', YouTubeShow),
    ('/main/player', YouTubePlayer)
], config=sconfig, debug=True)