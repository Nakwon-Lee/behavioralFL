from BaseHandler import BaseHandler
from BehaveLog import Behavlog
from apiclient.errors import HttpError
from apiclient.discovery import build

import google.oauth2.credentials

import Keys

class R_ChannelSections(BaseHandler):
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

                credentials = google.oauth2.credentials.Credentials(**self.session['credentials'])

                youtube = build(Keys.YOUTUBE_API_SERVICE_NAME,Keys.YOUTUBE_API_VERSION,credentials=credentials)

                command = self.session['command']

                if command == 'channelsec':
                    channelsitems = youtube.channelSections().list(part='snippet,contentDetails',mine=True).execute()

                    channelseclist = []

                    for item in channelsitems.get('items',[]):
                        channelseclist.append('%s' % (item.get('id')))

                    self.session['channelsec'] = item.get('id')

                    thislog.vector[10] = 1

                elif command == 'channelsecin':
                    channelid = self.session['channel']

                    body = {
                        'snippet' : {
                            'type' : 'allPlaylists',
                            'style' : 'verticalList',
                            'channelId' : channelid
                        }
                    }

                    youtube.channelSections().insert(part='snippet',body=body).execute()

                    thislog.vector[11] = 1

                elif command == 'channelsecdel':
                    channelsecid = self.session['channelsec']
                    youtube.channelSections().delete(id=channelsecid).execute()

                    thislog.vector[12] = 1

                elif command == 'channelsecup':
                    channelsecid = self.session['channelsec']

                    body = {
                        'id' : channelsecid,
                        'snippet' : {
                            'type' : 'allPlaylists',
                            'style' : 'verticalList',
                            'position' : 0
                        }
                    }

                    youtube.channelSections().update(part='id,snippet',body=body).execute()

                    thislog.vector[13] = 1

                self.redirect('/main/welcome')

            except HttpError, e:
                    thislog.sflabel = True
                    print e
                    self.response.write('<html><body><p>http error</p></body></html>')
            finally:
                thislog.put()

        except KeyError:
            self.response.status_int = 401
            self.response.write('<html><body><p>401 unauthorized access</p></body></html>')