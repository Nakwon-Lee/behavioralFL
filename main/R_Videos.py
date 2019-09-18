from BehaveLog import Behavlog
from BehaviorError import BehaviorError
from apiclient.errors import HttpError
from apiclient.discovery import build
from apiclient.http import MediaFileUpload

import google.oauth2.credentials

import Keys

class R_Videos():

    session = None
    request = None
    def __init__(self, pSession, pRequest):
        self.session = pSession
        self.request = pRequest

    def get(self):

        try:

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

            if command == 'videosin':

                try:
            
                    body = {
                        'snippet' : {
                            'title' : 'rainbow',
                            'description' : 'Rainbow!',
                            'categoryId' : '22'
                        },
                        'status' : {
                            'privacyStatus' : 'public'
                        }
                    }

                    videoin_req = youtube.videos().insert(part=','.join(body.keys()),body=body,media_body=MediaFileUpload('nwlee-video.mp4',chunksize=-1,resumable=True))

                    response = None

                    while response is None:
                        status, response = videoin_req.next_chunk()
                        #if 'id' in response:
                        #    self.session['videoid'] = response['id']

                except HttpError, e:
                    thislog.sflabel = True
                    print(e)
                    print("http error")
                    raise BehaviorError()
                finally:
                    count = self.session['count']
                    thislog.vector[count] = 10

            elif command == 'videosrm':

                try:

                    videoid = self.session['videoid']
                    youtube.videos().delete(id=videoid).execute()
                    self.session['videoid'] = 'none'
                    self.session['videomine'] = False
                    self.session['cstate'] = 14

                except HttpError, e:
                    thislog.sflabel = True
                    print(e)
                    print("http error")
                    raise BehaviorError()
                finally:
                    count = self.session['count']
                    thislog.vector[count] = 4

            elif command == 'videos':

                try:

                    videoid = self.session['videoid']
                    videostat = youtube.videos().list(id=videoid,part='snippet').execute()

                    items = []

                    for item in videostat.get('items',[]):
                        items.append(item)

                    if len(items) > 0:
                        videotitle = items[0].get('snippet').get('title')

                    self.session['videotitle'] = videotitle

                except HttpError, e:
                    thislog.sflabel = True
                    print(e)
                    print("http error")
                    raise BehaviorError()
                finally:
                    count = self.session['count']
                    thislog.vector[count] = 13

            elif command == 'videosup':

                try:

                    videoid = self.session['videoid']

                    body = {
                        'id' : videoid,
                        'snippet' : {
                            'title' : 'rainbow-modi'
                        }
                    }

                    youtube.videos().update(part='snippet',body=body).execute()

                except HttpError, e:
                    thislog.sflabel = True
                    print(e)
                    print("http error")
                    raise BehaviorError()
                finally:
                    count = self.session['count']
                    thislog.vector[count] = 9

            # elif command == 'playlistsnew':

            #     body = {
            #         'snippet' : {
            #             'title' : 'added new 1',
            #             'description' : 'Experiment!'
            #         },
            #         'status' : {
            #             'privacyStatus' : 'private'
            #         }
            #     }

            #     youtube.playlists().insert(part='snippet,status', body=body).execute()

            #     thislog.vector[5] = 1

            # elif command == 'playlistsupdate':

            #     pPlaylistid = self.session['playlistId']

            #     body = {
            #         'id' : pPlaylistid,
            #         'snippet' : {
            #             'title' : 'list1 modi!',
            #             'description' : 'none'
            #         }
            #     }

            #     youtube.playlists().update(part='snippet',body=body).execute()

            #     thislog.vector[6] = 1

            # elif command == 'playlistsrm':

            #     pPlaylistid = self.session['playlistId']
            #     youtube.playlists().delete(id=pPlaylistid).execute()

            #     thislog.vector[7] = 1

        except KeyError:
            print("KeyError on videos")
        finally:
            thislog.put()