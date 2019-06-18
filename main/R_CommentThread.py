import io

from BaseHandler import BaseHandler
from BehaveLog import Behavlog
from apiclient.errors import HttpError
from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from apiclient.http import MediaIoBaseDownload

import google.oauth2.credentials

import Keys

class R_CommentThread(BaseHandler):
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

                if command == 'cmtthds':
                    videoid = self.session['videoid']
                    commentthd = youtube.commentThreads().list(videoId=videoid,part='id,snippet').execute()

                    items = []

                    for item in commentthd.get('items',[]):
                        items.append(item)

                    self.session['cmtthdid'] = items[0].get('id')

                    thislog.vector[23] = 1

                elif command == 'cmtthdsin':
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

                    print(response)

                    thislog.vector[24] = 1

                elif command == 'cmtthdsup':

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

                    thislog.vector[25] = 1

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