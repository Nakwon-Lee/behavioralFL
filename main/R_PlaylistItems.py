from BaseHandler import BaseHandler
from BehaveLog import Behavlog
from apiclient.errors import HttpError
from apiclient.discovery import build

import google.oauth2.credentials

import Keys

class R_PlayListItems(BaseHandler):
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

            try:

                pPlaylistid = self.session['playlistId']
                command = self.session['command']

                credentials = google.oauth2.credentials.Credentials(**self.session['credentials'])

                youtube = build(Keys.YOUTUBE_API_SERVICE_NAME,Keys.YOUTUBE_API_VERSION,credentials=credentials)

                if command == 'playlistitem':
                    plistitems = youtube.playlistItems().list(playlistId=pPlaylistid,part='id,snippet',maxResults=5).execute()
                    videos = []
                    itemids = []
                    for item in plistitems.get('items',[]):
                        if item.get('snippet').get('resourceId').get('kind') == 'youtube#video':
                            # print item.get('snippet').get('resourceId').get('videoId')
                            videos.append('%s' % (item.get('snippet').get('resourceId').get('videoId')))
                            itemids.append('%s' % (item.get('id')))
                    self.session['videoid'] = videos[0]
                    self.session['playlistitemid'] = itemids[0]

                    thislog.vector[0] = 1

                elif command == 'playlistitemin':

                    videoid = self.session['videoid']

                    body = {
                        'snippet' : {
                            'playlistId' : pPlaylistid, 
                            'resourceId' : {
                                'kind':'youtube#video',
                                'videoId':videoid
                            } 
                        }
                    }

                    youtube.playlistItems().insert(part='snippet',body=body).execute()

                    thislog.vector[1] = 1

                elif command == 'playlistitemdel':
                    playlistitemid = self.session['playlistitemid']
                    youtube.playlistItems().delete(id=playlistitemid).execute()

                    thislog.vector[2] = 1

                elif command == 'playlistitemupdate':
                    playlistitemid = self.session['playlistitemid']
                    videoid = self.session['videoid']

                    body = {
                        'id' : playlistitemid,
                        'snippet' : {
                            'playlistId' : pPlaylistid,
                            'resourceId' : {
                                'kind':'youtube#video',
                                'videoId': videoid 
                            },
                            'position' : 0
                        }
                    }

                    youtube.playlistItems().update(part='snippet',body=body).execute()

                    thislog.vector[3] = 1

                self.redirect('/main/welcome')

            except HttpError, e:
                thislog.sflabel = True
                self.response.write('<html><body><p>http error</p></body></html>')
            finally:
                thislog.put()

        except KeyError:
            self.response.status_int = 401
            self.response.write('<html><body><p>401 unauthorized access</p></body></html>')