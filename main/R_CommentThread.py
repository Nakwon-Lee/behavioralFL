import io

from BehaveLog import Behavlog
from BehaviorError import BehaviorError
from apiclient.errors import HttpError
from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from apiclient.http import MediaIoBaseDownload

import random
import google.oauth2.credentials

import Keys

class R_CommentThread():

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

            if command == 'cmtthds':

                try:

                    videoid = self.session['videoid']
                    commentthd = youtube.commentThreads().list(videoId=videoid,part='id,snippet').execute()

                    items = []

                    for item in commentthd.get('items',[]):
                        items.append(item)

                    if len(items) > 0:
                        idx = random.randrange(0,len(items))
                        self.session['cmtthdid'] = items[idx].get('id')
                        if items[idx].get('snippet').get('authorChannelId').get('value') == self.session['channel']:
                            self.session['cstate'] = 5
                            self.session['cmtthdmine'] = True
                        else:
                            self.session['cstate'] = 6
                            self.session['cmtthdmine'] = False

                except HttpError, e:
                    thislog.sflabel = True
                    print(e)
                    print("http error")
                    raise BehaviorError()
                finally:
                    count = self.session['count']
                    thislog.vector[count] = 6

            elif command == 'cmtthdsin':

                try:

                    videoid = self.session['videoid']

                    body = {
                        'snippet' : {
                            'videoId' : videoid,
                            'topLevelComment' : {
                                'snippet' : {
                                    'textOriginal' : 'This is a test top-level comment.'
                                }
                            }
                        }
                    }

                    response = youtube.commentThreads().insert(part='snippet',body=body).execute()

                    print(response.get('id'))

                    self.session['cmtthdid'] = response.get('id')

                    self.session['cstate'] = 4

                except HttpError, e:
                    thislog.sflabel = True
                    print(e)
                    print("http error")
                    raise BehaviorError()
                finally:
                    count = self.session['count']
                    thislog.vector[count] = 5

            elif command == 'cmtthdsup':

                try:

                    cmtthdid = self.session['cmtthdid']

                    body = {
                        'id': cmtthdid,
                        'snippet' : {
                            'topLevelComment' : {
                                'snippet' : {
                                    'textOriginal' : 'This is an updated comment.'
                                }
                            }
                        }
                    }

                    response = youtube.commentThreads().update(part='snippet',body=body).execute()

                    self.session['cstate'] = 5

                except HttpError, e:
                    thislog.sflabel = True
                    print(e)
                    print("http error")
                    raise BehaviorError()
                finally:
                    count = self.session['count']
                    thislog.vector[count] = 8

        except KeyError:
            print("KeyError on cmtthd")
        finally:
            thislog.put()