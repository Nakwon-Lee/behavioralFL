import io

from BaseHandler import BaseHandler
from BehaveLog import Behavlog
from apiclient.errors import HttpError
from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from apiclient.http import MediaIoBaseDownload

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

                    print(items[0].get('id'))

                    self.session['captionid'] = items[0].get('id')

                    thislog.vector[18] = 1

                elif command == 'captionsin':
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

                    thislog.vector[19] = 1

                elif command == 'captionsdw':
                    captionid = self.session['captionid']

                    request = youtube.captions().download(id=captionid)

                    fh = io.FileIO('down-cap.srt','wb')

                    download = MediaIoBaseDownload(fh,request)

                    complete = False

                    while not complete:
                        status, complete = download.next_chunk()

                    thislog.vector[20] = 1

                elif command == 'captionsdw':
                    captionid = self.session['captionid']

                    request = youtube.captions().download(id=captionid)

                    fh = io.FileIO('down-cap.srt','wb')

                    download = MediaIoBaseDownload(fh,request)

                    complete = False

                    while not complete:
                        status, complete = download.next_chunk()

                    thislog.vector[20] = 1
                
                elif command == 'captionsrm':
                    captionid = self.session['captionid']

                    request = youtube.captions().delete(id=captionid).execute()

                    thislog.vector[21] = 1

                elif command == 'captionsup':
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

                    thislog.vector[22] = 1

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