from BaseHandler import BaseHandler
from BehaveLog import Behavlog
from BehaviorError import BehaviorError
from apiclient.errors import HttpError
from apiclient.discovery import build
from apiclient.http import MediaFileUpload

from R_Playlist import R_Playlist
from R_PlaylistItems import R_PlayListItems
from R_Channels import R_Channels
from R_Videos import R_Videos
from R_CommentThread import R_CommentThread
from R_Comment import R_Comment
from R_Search import R_Search
from R_Activity import R_Activity
from R_Caption import R_Caption
from R_ChannelBanner import R_ChannelBanner
from R_ChannelSections import R_ChannelSections

import random
import google.oauth2.credentials

import Keys

class R_ForceFail(BaseHandler):
    c_channels = None
    c_cmts = None
    c_cmtthds = None
    c_videos = None
    c_plistitem = None
    c_plist = None
    c_search = None
    c_activity = None
    c_caption = None
    c_channelbanner = None
    c_channelsec = None

    def get(self):

        self.c_channels = R_Channels(self.session,self.request)
        self.c_cmts = R_Comment(self.session,self.request)
        self.c_cmtthds = R_CommentThread(self.session,self.request)
        self.c_videos = R_Videos(self.session,self.request)
        self.c_plistitem = R_PlayListItems(self.session,self.request)
        self.c_plist = R_Playlist(self.session,self.request)
        self.c_search = R_Search(self.session,self.request)
        self.c_activity = R_Activity(self.session,self.request)
        self.c_caption = R_Caption(self.session,self.request)
        self.c_channelbanner = R_ChannelBanner(self.session,self.request)
        self.c_channelsec = R_ChannelSections(self.session,self.request)

        try:

            credentials = google.oauth2.credentials.Credentials(**self.session['credentials'])

            count = 0

            self.session['count'] = count

            self.session['sel'] = 0
            self.session['command'] = 'channels'
            self.c_channels.get()

            count = count + 1

            self.session['count'] = count

            self.session['sel'] = 0
            self.session['command'] = 'playlistitem'
            self.c_plistitem.get()

            count = count + 1

            self.session['count'] = count

            self.session['sel'] = 1 # no meaning
            self.session['command'] = 'cmtthdsin'
            self.c_cmtthds.get()

            count = count + 1

            self.session['count'] = count

            self.session['sel'] = 0 # no meaning
            self.session['command'] = 'commentsin'
            self.c_cmts.get()

            count = count + 1

            self.session['count'] = count

            self.session['sel'] = 0 # no meaning
            self.session['command'] = 'commentsrm'
            self.c_cmts.get()

            count = count + 1

            self.session['count'] = count

            self.session['sel'] = 0 # no meaning
            self.session['command'] = 'commentsup'
            self.c_cmts.get()

            count = count + 1

            self.session['count'] = count

            self.session['sel'] = 0
            self.session['command'] = 'channels'
            self.c_channels.get()
                    
            self.redirect('/main/welcome')

        except BehaviorError:
            print('behavior error')
            self.redirect('/main/welcome')
