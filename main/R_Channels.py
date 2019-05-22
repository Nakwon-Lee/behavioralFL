from BaseHandler import BaseHandler
from BehaveLog import Behavlog
from apiclient.errors import HttpError
from apiclient.discovery import build

import google.oauth2.credentials

import Keys

class R_Channels(BaseHandler):
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

            try:

                credentials = google.oauth2.credentials.Credentials(**self.session['credentials'])

                youtube = build(Keys.YOUTUBE_API_SERVICE_NAME,Keys.YOUTUBE_API_VERSION,credentials=credentials)

                command = self.session['command']

                if command == 'channels':
                    channelsitems = youtube.channels().list(part='snippet,contentDetails,brandingSettings',mine=True).execute()

                    channelslist = []

                    for item in channelsitems.get('items',[]):
                        channelslist.append('%s' % (item.get('id')))

                    self.session['channel'] = item.get('id')

                    thislog.vector[9] = 1

                self.redirect('/main/welcome')

            except HttpError, e:
                    thislog.sflabel = True
                    self.response.write('<html><body><p>http error</p></body></html>')
            finally:
                thislog.put()

        except KeyError:
            self.response.status_int = 401
            self.response.write('<html><body><p>401 unauthorized access</p></body></html>')