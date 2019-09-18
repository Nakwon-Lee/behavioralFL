import io

from BehaveLog import Behavlog
from BehaviorError import BehaviorError
from apiclient.errors import HttpError
from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from apiclient.http import MediaIoBaseDownload

import google.oauth2.credentials

import random
import Keys

class R_Caption():

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

            if command == 'captions':

                try:

                    videoid = self.session['videoid']
                    captions = youtube.captions().list(videoId=videoid,part='snippet').execute()

                    items = []

                    for item in captions.get('items',[]):
                        items.append(item)

                    if len(items) > 0:
                        idx = random.randrange(0,len(items))
                        self.session['captionid'] = items[idx].get('id')

                except HttpError, e:
                    thislog.sflabel = True
                    print(e)
                    print("http error")
                    raise BehaviorError()
                finally:
                    count = self.session['count']
                    thislog.vector[23] = 23

            elif command == 'captionsin':

                try:
                    videoid = self.session['videoid']

                    body = {
                        'snippet' : {
                            'videoId' : videoid,
                            'language' : 'ko-KR',
                            'name' : 'kor caption'
                        }
                    }

                    medf = MediaFileUpload('kor-cap-rainbow.srt')

                    captionres = youtube.captions().insert(part='snippet',body=body,media_body=medf)

                    response = captionres.execute()

                    print(response)

                except HttpError, e:
                    thislog.sflabel = True
                    print(e)
                    print("http error")
                    raise BehaviorError()
                finally:
                    count = self.session['count']
                    thislog.vector[count] = 24

            elif command == 'captionsdw':

                try:

                    captionid = self.session['captionid']

                    request = youtube.captions().download(id=captionid)

                    fh = io.FileIO('down-cap.srt','wb')

                    download = MediaIoBaseDownload(fh,request)

                    complete = False

                    while not complete:
                        status, complete = download.next_chunk()

                except HttpError, e:
                    thislog.sflabel = True
                    print(e)
                    print("http error")
                    raise BehaviorError()
                finally:
                    count = self.session['count']
                    thislog.vector[count] = 33
            
            elif command == 'captionsrm':

                try:

                    captionid = self.session['captionid']

                    request = youtube.captions().delete(id=captionid).execute()

                except HttpError, e:
                    thislog.sflabel = True
                    print(e)
                    print("http error")
                    raise BehaviorError()
                finally:
                    count = self.session['count']
                    thislog.vector[count] = 26

            elif command == 'captionsup':

                try:
                    videoid = self.session['videoid']
                    captionid = self.session['captionid']

                    body = {
                        'id' : captionid,
                        'snippet' : {
                            'videoId' : videoid,
                            'language' : 'ko-KR',
                            'name' : 'kor caption v2'
                        }
                    }

                    medf = MediaFileUpload('kor-cap-rainbow2.srt')

                    request = youtube.captions().update(part='snippet',body=body,media_body=medf).execute()

                except HttpError, e:
                    thislog.sflabel = True
                    print(e)
                    print("http error")
                    raise BehaviorError()
                finally:
                    count = self.session['count']
                    thislog.vector[count] = 25

        except KeyError:
            print("KeyError on caption")
        finally:
            thislog.put()