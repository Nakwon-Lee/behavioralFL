from BaseHandler import BaseHandler
from BehaveLog import Behavlog
from apiclient.errors import HttpError
from apiclient.discovery import build
from apiclient.http import MediaFileUpload

import google.oauth2.credentials

import Keys

class R_Videos(BaseHandler):
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

                if command == 'videosin':
                
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
                        if 'id' in response:
                            self.session['videoid'] = response['id']

                    thislog.vector[14] = 1

                elif command == 'videosrm':

                    videoid = self.session['videoid']
                    youtube.videos().delete(id=videoid).execute()
                    self.session['videoid'] = 'none'

                    thislog.vector[15] = 1

                elif command == 'videos':

                    videoid = self.session['videoid']
                    videostat = youtube.videos().list(id=videoid,part='snippet').execute()

                    items = []

                    for item in videostat.get('items',[]):
                        items.append(item)

                    videotitle = items[0].get('snippet').get('title')

                    self.session['videotitle'] = videotitle

                    thislog.vector[16] = 1

                elif command == 'videosup':

                    videoid = self.session['videoid']

                    body = {
                        'id' : videoid,
                        'snippet' : {
                            'title' : 'rainbow-modi'
                        }
                    }

                    youtube.videos().update(part='snippet').execute()

                    thislog.vector[17] = 1

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