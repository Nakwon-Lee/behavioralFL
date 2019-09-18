from BehaveLog import Behavlog
from BehaviorError import BehaviorError
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

            youtube = build(Keys.YOUTUBE_API_SERVICE_NAME,Keys.YOUTUBE_API_VERSION,developerKey=Keys.DEVELOPER_KEY)
            
            try:

                searchlist = youtube.search().list(q='Google Official',part='snippet',type='video',maxResults=5).execute()

                videos = []

                for item in searchlist.get('items',[]):
                    if item['id']['kind'] == 'youtube#video':
                        videos.append('%s' % (item['id']['videoId']))

                if len(videos) > 0:
                    idx = random.randrange(0,len(videos))
                    self.session['videoid'] = videos[idx]

            except HttpError, e:
                thislog.sflabel = True
                print(e)
                print("http error")
                raise BehaviorError()
            finally:
                count = self.session['count']
                thislog.vector[count] = 20

        except KeyError:
            print("KeyError on search")
        finally:
            thislog.put()