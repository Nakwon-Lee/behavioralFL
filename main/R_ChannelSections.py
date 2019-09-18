from BehaveLog import Behavlog
from BehaviorError import BehaviorError
from apiclient.errors import HttpError
from apiclient.discovery import build

import google.oauth2.credentials

import random
import Keys

class R_ChannelSections():

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

            if command == 'channelsec':

                try:

                    channelsitems = youtube.channelSections().list(part='snippet,contentDetails',mine=True).execute()

                    channelseclist = []

                    for item in channelsitems.get('items',[]):
                        channelseclist.append('%s' % (item.get('id')))

                    if len(channelseclist) > 0:
                        idx = random.randrange(0,len(channelseclist))
                        self.session['channelsec'] = channelseclist[idx]

                except HttpError, e:
                    thislog.sflabel = True
                    print(e)
                    print("http error")
                    raise BehaviorError()
                finally:
                    count = self.session['count']
                    thislog.vector[count] = 28

            elif command == 'channelsecin':

                try:

                    channelid = self.session['channel']

                    body = {
                        'snippet' : {
                            'type' : 'allPlaylists',
                            'style' : 'verticalList',
                            'channelId' : channelid
                        }
                    }

                    youtube.channelSections().insert(part='snippet',body=body).execute()

                except HttpError, e:
                    thislog.sflabel = True
                    print(e)
                    print("http error")
                    raise BehaviorError()
                finally:
                    count = self.session['count']
                    thislog.vector[count] = 29

            elif command == 'channelsecdel':

                try:

                    channelsecid = self.session['channelsec']
                    youtube.channelSections().delete(id=channelsecid).execute()

                except HttpError, e:
                    thislog.sflabel = True
                    print(e)
                    print("http error")
                    raise BehaviorError()
                finally:
                    count = self.session['count']
                    thislog.vector[count] = 31

            elif command == 'channelsecup':

                try:

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

                except HttpError, e:
                    thislog.sflabel = True
                    print(e)
                    print("http error")
                    raise BehaviorError()
                finally:
                    count = self.session['count']
                    thislog.vector[count] = 30

        except KeyError:
            print("KeyError on channelsec")
        finally:
            thislog.put()