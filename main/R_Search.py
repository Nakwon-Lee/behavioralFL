from BehaveLog import Behavlog
from apiclient.errors import HttpError
from apiclient.discovery import build

import random
import Keys

class R_Search():

    session = None
    request = None
    def __init__(self, pSession, pRequest):
        self.session = pSession
        self.request = pRequest

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

                idx = random.randrange(0,len(videos))

                self.session['videoid'] = videos[idx]

                thislog.vector[20] = 1

            except HttpError, e:
                thislog.sflabel = True
                print(e)
                print("http error")
                raise HttpError
                #self.response.write('<html><body><p>http error</p></body></html>')
            finally:
                thislog.put()

        except KeyError:
            print("KeyError on search")
            #self.response.status_int = 401
            #self.response.write('<html><body><p>401 unauthorized access</p></body></html>')