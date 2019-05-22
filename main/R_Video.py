from BaseHandler import BaseHandler
from BehaveLog import Behavlog
from apiclient.errors import HttpError
from apiclient.discovery import build

import Keys

class R_Video(BaseHandler):
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
                youtube = build(Keys.YOUTUBE_API_SERVICE_NAME,Keys.YOUTUBE_API_VERSION,developerKey=Keys.DEVELOPER_KEY)
                searchlist = youtube.search().list(q='Google Official',part='snippet',type='video',maxResults=5).execute()

                videos = []

                for item in searchlist.get('items',[]):
                    if item['id']['kind'] == 'youtube#video':
                        videos.append('%s' % (item['id']['videoId']))

                self.session['videoid'] = videos[0]

                thislog.vector[8] = 1

                self.redirect('/main/welcome')

            except HttpError, e:
                thislog.sflabel = True
                self.response.write('<html><body><p>http error</p></body></html>')
            finally:
                thislog.put()

        except KeyError:
            self.response.status_int = 401
            self.response.write('<html><body><p>401 unauthorized access</p></body></html>')