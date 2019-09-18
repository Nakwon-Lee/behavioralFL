from BehaveLog import Behavlog
from BehaviorError import BehaviorError
from apiclient.errors import HttpError
from apiclient.discovery import build

import google.oauth2.credentials
import random

import Keys

class R_Channels():
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

            if command == 'channels':

                try:

                    sel = self.session['sel']

                    if sel == 0: # mine

                        channelsitems = youtube.channels().list(part='snippet,contentDetails,brandingSettings',mine=True).execute()

                        channelslist = []

                        items = []

                        for item in channelsitems.get('items',[]):
                            channelslist.append('%s' % (item.get('id')))
                            items.append(item)

                        if len(items) > 0:
                            idx = random.randrange(0,len(items))
                            self.session['channel'] = channelslist[idx]
                            self.session['uploads'] = items[idx].get('contentDetails').get('relatedPlaylists').get('uploads')
                            self.session['channelmine'] = True
                            self.session['cstate'] = 1

                    elif sel == 1: # user name

                        channelsitems = youtube.channels().list(part='snippet,contentDetails,brandingSettings',forUsername='Google').execute()

                        channelslist = []

                        for item in channelsitems.get('items',[]):
                            channelslist.append('%s' % (item.get('id')))

                        if len(channelslist) > 0:
                            idx = random.randrange(0,len(channelslist))
                            self.session['channel'] = channelslist[idx]
                            self.session['channelmine'] = False
                            self.session['cstate'] = 2

                except HttpError, e:
                    thislog.sflabel = True
                    print(e)
                    print("http error")
                    raise BehaviorError()
                finally:
                    count = self.session['count']
                    thislog.vector[count] = 0

            elif command == 'channelsup':

                try:

                    channelid = self.session['channel']
                    bannerurl = self.session['bannerurl']

                    body = {
                        'id' : channelid,
                        'brandingSetting' : {
                            'image' : {
                                'bannerExternalUrl' : bannerurl
                            }
                        }
                    }

                    youtube.channels().update(part='id',body=body).execute()

                except HttpError, e:
                    thislog.sflabel = True
                    print(e)
                    print("http error")
                    raise BehaviorError()
                finally:
                    count = self.session['count']
                    thislog.vector[count] = 32

        except KeyError:
            print("KeyError on channel")
        finally:
            thislog.put()