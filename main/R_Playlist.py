from BaseHandler import BaseHandler
from BehaveLog import Behavlog
from apiclient.errors import HttpError
from apiclient.discovery import build

import google.oauth2.credentials

import Keys

class R_Playlist(BaseHandler):
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

                if command == 'playlists':
                
                    playlistlist = youtube.playlists().list(part='snippet',mine=True).execute()

                    playlists = []

                    for item in playlistlist.get('items',[]):
                        print item.get('id')
                        playlists.append('%s' % (item.get('id')))
                        
                    self.session['playlistId'] = playlists[0]

                    thislog.vector[4] = 1

                elif command == 'playlistsnew':

                    body = {
                        'snippet' : {
                            'title' : 'added new 1',
                            'description' : 'Experiment!'
                        },
                        'status' : {
                            'privacyStatus' : 'private'
                        }
                    }

                    youtube.playlists().insert(part='snippet,status', body=body).execute()

                    thislog.vector[5] = 1

                elif command == 'playlistsupdate':

                    pPlaylistid = self.session['playlistId']

                    body = {
                        'id' : pPlaylistid,
                        'snippet' : {
                            'title' : 'list1 modi!',
                            'description' : 'none'
                        }
                    }

                    youtube.playlists().update(part='snippet',body=body).execute()

                    thislog.vector[6] = 1

                elif command == 'playlistsrm':

                    pPlaylistid = self.session['playlistId']
                    youtube.playlists().delete(id=pPlaylistid).execute()

                    thislog.vector[7] = 1

                self.redirect('/main/welcome')

            except HttpError, e:
                thislog.sflabel = True
                self.response.write('<html><body><p>http error</p></body></html>')
            finally:
                thislog.put()

        except KeyError:
            self.response.status_int = 401
            self.response.write('<html><body><p>401 unauthorized access</p></body></html>')