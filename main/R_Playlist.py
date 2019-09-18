from BehaveLog import Behavlog
from BehaviorError import BehaviorError
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

            youtube = build(Keys.YOUTUBE_API_SERVICE_NAME,Keys.YOUTUBE_API_VERSION,credentials=credentials)
            
            command = self.session['command']

            if command == 'playlists':

                try:
            
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

                except HttpError, e:
                    thislog.sflabel = True
                    print(e)
                    print("http error")
                    raise BehaviorError()
                finally:
                    count = self.session['count']
                    thislog.vector[count] = 1

            elif command == 'playlistsnew':

                try:

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

                except HttpError, e:
                    thislog.sflabel = True
                    print(e)
                    print("http error")
                    raise BehaviorError()
                finally:
                    count = self.session['count']
                    thislog.vector[count] = 17

            elif command == 'playlistsupdate':

                try:

                    pPlaylistid = self.session['playlistId']

                    body = {
                        'id' : pPlaylistid,
                        'snippet' : {
                            'title' : 'list1 modi!',
                            'description' : 'none'
                        }
                    }

                    youtube.playlists().update(part='snippet',body=body).execute()

                except HttpError, e:
                    thislog.sflabel = True
                    print(e)
                    print("http error")
                    raise BehaviorError()
                finally:
                    count = self.session['count']
                    thislog.vector[count] = 18

            elif command == 'playlistsrm':

                try:

                    pPlaylistid = self.session['playlistId']
                    youtube.playlists().delete(id=pPlaylistid).execute()

                except HttpError, e:
                    thislog.sflabel = True
                    print(e)
                    print("http error")
                    raise BehaviorError()
                finally:
                    count = self.session['count']
                    thislog.vector[count] = 19

        except KeyError:
            print("KeyError on plist")
        finally:
            thislog.put()