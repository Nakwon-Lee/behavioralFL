from BaseHandler import BaseHandler
from BehaveLog import Behavlog
from apiclient.errors import HttpError
from apiclient.discovery import build

import google.oauth2.credentials

import Keys

class R_Activity(BaseHandler):
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

                if command == 'activities':
                    comments = youtube.activities().list(part='id,snippet,contentDetails',mine=True).execute()

                    items = []

                    for item in comments.get('items',[]):
                        items.append(item)

                    self.session['activityid'] = items[0].get('id')

                    thislog.vector[30] = 1

                elif command == 'activitiesin':

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

                    thislog.vector[31] = 1

                self.redirect('/main/welcome')

            except HttpError, e:
                thislog.sflabel = True
                print(e)
                self.response.write('<html><body><p>http error</p></body></html>')
            finally:
                thislog.put()

        except KeyError:
            self.response.status_int = 401
            self.response.write('<html><body><p>401 unauthorized access</p></body></html>')