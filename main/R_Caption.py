from BaseHandler import BaseHandler
from BehaveLog import Behavlog
from apiclient.errors import HttpError
from apiclient.discovery import build

import google.oauth2.credentials

import Keys

class R_Caption(BaseHandler):
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

            credentials = google.oauth2.credentials.Credentials(**self.session['credentials'])

            try:
                youtube = build(Keys.YOUTUBE_API_SERVICE_NAME,Keys.YOUTUBE_API_VERSION,credentials=credentials)
                
                command = self.session['command']

                if command == 'captions':
                    videoid = self.session['videoid']
                    captions = youtube.captions().list(videoId=videoid,part='snippet').execute()

                    items = []

                    for item in captions.get('items',[]):
                        items.append(item)

                    print items[0]

                self.redirect('/main/welcome')

            except HttpError, e:
                thislog.sflabel = True
                self.response.write('<html><body><p>http error</p></body></html>')
            finally:
                thislog.put()

        except KeyError:
            self.response.status_int = 401
            self.response.write('<html><body><p>401 unauthorized access</p></body></html>')