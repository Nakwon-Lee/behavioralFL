from BaseHandler import BaseHandler
from BehaveLog import Behavlog
from apiclient.errors import HttpError
from apiclient.discovery import build

import random
import google.oauth2.credentials

import Keys

class R_Playlist():

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

            try:
                youtube = build(Keys.YOUTUBE_API_SERVICE_NAME,Keys.YOUTUBE_API_VERSION,credentials=credentials)
                
                command = self.session['command']

                if command == 'playlists':
                
                    playlistlist = youtube.playlists().list(part='snippet',mine=True).execute()

                    playlists = []

                    for item in playlistlist.get('items',[]):
                        print item.get('id')
                        playlists.append('%s' % (item.get('id')))

                    if len(playlists) > 0:
                        idx = random.randrange(0,len(playlists))
                        self.session['playlistId'] = playlists[idx]
                        self.session['playlistIdmine'] = True
                        self.session['cstate'] = 3
                    else:
                        pass
                    thislog.vector[1] = 1

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

                    thislog.vector[17] = 1

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

                    thislog.vector[18] = 1

                elif command == 'playlistsrm':

                    pPlaylistid = self.session['playlistId']
                    youtube.playlists().delete(id=pPlaylistid).execute()

                    thislog.vector[19] = 1

            except HttpError, e:
                thislog.sflabel = True
                print(e)
                print("http error")
                raise HttpError
                #self.response.write('<html><body><p>http error</p></body></html>')
            finally:
                thislog.put()

        except KeyError:
            print("KeyError on plist")
            #self.response.status_int = 401
            #self.response.write('<html><body><p>401 unauthorized access</p></body></html>')