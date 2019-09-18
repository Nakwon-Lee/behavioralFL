from BehaveLog import Behavlog
from BehaviorError import BehaviorError
from apiclient.errors import HttpError
from apiclient.discovery import build

import google.oauth2.credentials

import random
import Keys

class R_Activity():

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

            credentials = google.oauth2.credentials.Credentials(**self.session['credentials'])

            youtube = build(Keys.YOUTUBE_API_SERVICE_NAME,Keys.YOUTUBE_API_VERSION,credentials=credentials)
            
            command = self.session['command']

            if command == 'activities':

                try:

                    comments = youtube.activities().list(part='id,snippet,contentDetails',mine=True).execute()

                    items = []

                    for item in comments.get('items',[]):
                        items.append(item)

                    if len(items) > 0:
                        idx = random.randrange(0,len(items))
                        self.session['activityid'] = items[idx].get('id')
                
                except HttpError, e:
                    thislog.sflabel = True
                    print(e)
                    print("http error")
                    raise BehaviorError()
                finally:
                    count = self.session['count']
                    thislog.vector[count] = 21

            elif command == 'activitiesin':

                try:

                    videoid = self.session['videoid']

                    body = {
                        'snippet' : {
                            'description' : 'test bulletin'
                        },
                        'contentDetails' : {
                            'bulletin' : {
                                'resourceId' : {
                                    'kind' : 'youtube#video',
                                    'videoId' : videoid
                                }
                            }
                        }
                    }

                    response = youtube.activities().insert(part='snippet,contentDetails',body=body).execute()

                    print(response)

                except HttpError, e:
                    thislog.sflabel = True
                    print(e)
                    print("http error")
                    raise BehaviorError()
                finally:
                    count = self.session['count']
                    thislog.vector[count] = 22

        except KeyError:
            print("KeyError on activities")
        finally:
            thislog.put()