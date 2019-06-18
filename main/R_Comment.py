import io

from BaseHandler import BaseHandler
from BehaveLog import Behavlog
from apiclient.errors import HttpError
from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from apiclient.http import MediaIoBaseDownload

import google.oauth2.credentials

import Keys

class R_Comment(BaseHandler):
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

                if command == 'comments':
                    cmtthdid = self.session['cmtthdid']
                    comments = youtube.comments().list(part='snippet',parentId=cmtthdid).execute()

                    items = []

                    for item in comments.get('items',[]):
                        items.append(item)

                    self.session['commentid'] = items[0].get('id')

                    thislog.vector[26] = 1

                elif command == 'commentsin':
                    cmtthdid = self.session['cmtthdid']

                    body = {
                        'snippet' : {
                            'parentId' : cmtthdid,
                            'textOriginal' : 'This is a replying comment.'
                        }
                    }

                    response = youtube.comments().insert(part='snippet',body=body).execute()

                    print(response)

                    thislog.vector[27] = 1

                elif command == 'commentsup':
                    commentid = self.session['commentid']

                    body = {
                        'id' : commentid,
                        'snippet' : {
                            'textOriginal' : 'This is an updated replying comment.'
                        }
                    }

                    request = youtube.comments().update(part='snippet',body=body).execute()

                    thislog.vector[28] = 1
                
                elif command == 'commentsrm':
                    commentid = self.session['commentid']

                    request = youtube.comments().delete(id=commentid).execute()

                    thislog.vector[29] = 1

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