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

from GlobalVar import LIST_LENGTH

class R_Random(BaseHandler):
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

            while True:

                swtch = []

                for i in range(15):
                    swtch.append(False)

                if self.session['videoid'] != 'none':
                    swtch[0] = True
                if self.session['videomine']:
                    swtch[1] = True
                if self.session['playlistId'] != 'none':
                    swtch[2] = True
                if self.session['playlistIdmine']:
                    swtch[3] = True
                if self.session['cmtthdid'] != 'none':
                    swtch[4] = True
                if self.session['cmtthdmine']:
                    swtch[5] = True
                if self.session['channel'] != 'none':
                    swtch[6] = True
                if self.session['channelmine']:
                    swtch[7] = True
                if self.session['uploads'] != 'none':
                    swtch[8] = True
                if self.session['playlistitemid'] != 'none':
                    swtch[9] = True
                if self.session['playlistitemmine']:
                    swtch[10] = True
                if self.session['commentid'] != 'none':
                    swtch[11] = True
                if self.session['activityid'] != 'none':
                    swtch[12] = True
                if self.session['captionid'] != 'none':
                    swtch[13] = True
                if self.session['channelsec'] != 'none':
                    swtch[14] = True

                avail = set()

                avail.add(0)
                avail.add(1)
                avail.add(2)
                avail.add(12)
                avail.add(19)
                avail.add(22)
                avail.add(23)
                avail.add(29)
                avail.add(30)

                if swtch[2]:
                    avail.add(3)
                if swtch[8]:
                    avail.add(4)
                if swtch[2] and swtch[3] and swtch[0]:
                    avail.add(5)
                if swtch[2] and swtch[3]:
                    avail.add(20)
                    avail.add(21)
                if swtch[0] and swtch[1]:
                    avail.add(6)
                    avail.add(7)
                    avail.add(8)
                    avail.add(11)
                if swtch[4] and swtch[5]:
                    avail.add(9)
                    avail.add(10)
                if swtch[9] and swtch[2] and swtch[0]:
                    avail.add(13)
                if swtch[9] and swtch[10]:
                    avail.add(14)
                if swtch[6] and swtch[7]:
                    avail.add(31)
                if swtch[0]:
                    avail.add(15)
                    avail.add(24)
                    avail.add(25)
                    avail.add(26)
                if swtch[4]:
                    avail.add(16)
                    avail.add(17)
                if swtch[11]:
                    avail.add(18)
                if swtch[0] and swtch[13]:
                    avail.add(27)
                if swtch[13]:
                    avail.add(28)
                    avail.add(35)
                if swtch[14]:
                    avail.add(32)
                    avail.add(33)
                if swtch[6]:
                    avail.add(34)

                print(count)
                print(avail)

                self.session['count'] = count

                selectedkey = random.choice(list(avail))

                if count >= LIST_LENGTH:
                    selectedkey = 100
                else:
                    count = count + 1

                print(selectedkey)

                if selectedkey == 0: # channel mine 0
                    self.session['sel'] = 0
                    self.session['command'] = 'channels'
                    self.c_channels.get()
                elif selectedkey == 1: # channel not mine 0
                    self.session['sel'] = 1
                    self.session['command'] = 'channels'
                    self.c_channels.get()
                elif selectedkey == 2: # playlist mine 1
                    self.session['sel'] = 2
                    self.session['command'] = 'playlists'
                    self.c_plist.get()
                elif selectedkey == 3: # playlistitem not my video 2
                    self.session['sel'] = 1
                    self.session['command'] = 'playlistitem'
                    self.c_plistitem.get()
                elif selectedkey == 4: # playlistitem uploads 2
                    self.session['sel'] = 0
                    self.session['command'] = 'playlistitem'
                    self.c_plistitem.get()
                elif selectedkey == 5: # playlistitemin 3
                    self.session['sel'] = 1 # no meaning
                    self.session['command'] = 'playlistitemin'
                    self.c_plistitem.get()
                elif selectedkey == 6: # videorm 4
                    self.session['sel'] = 0 # no meaning
                    self.session['command'] = 'videosrm'
                    self.c_videos.get()
                elif selectedkey == 7: # cmtthdsin 5
                    self.session['sel'] = 1 # no meaning
                    self.session['command'] = 'cmtthdsin'
                    self.c_cmtthds.get()
                elif selectedkey == 8: # cmtthds 6
                    self.session['sel'] = 0 # no meaning
                    self.session['command'] = 'cmtthds'
                    self.c_cmtthds.get()
                elif selectedkey == 9: # cmtthdsrm 7
                    self.session['sel'] = 0 # no meaning
                    self.session['command'] = 'commentsrm'
                    self.c_cmts.get()
                elif selectedkey == 10: # cmtthdsup 8
                    self.session['sel'] = 1 # no meaning
                    self.session['command'] = 'cmtthdsup'
                    self.c_cmtthds.get()
                elif selectedkey == 11: # videoup 9
                    self.session['sel'] = 3 # no meaning
                    self.session['command'] = 'videosup'
                    self.c_videos.get()
                elif selectedkey == 12: # videoin 10
                    self.session['sel'] = 3 # no meaning
                    self.session['command'] = 'videosin'
                    self.c_videos.get()
                elif selectedkey == 13: # playlistitemup 11
                    self.session['sel'] = 0 # no meaning
                    self.session['command'] = 'playlistitemupdate'
                    self.c_plistitem.get()
                elif selectedkey == 14: # playlistitemdel 12
                    self.session['sel'] = 0 # no meaning
                    self.session['command'] = 'playlistitemdel'
                    self.c_plistitem.get()
                elif selectedkey == 15: # videos 13
                    self.session['sel'] = 0 # no meaning
                    self.session['command'] = 'videos'
                    self.c_videos.get()
                elif selectedkey == 16: # cmts 14
                    self.session['sel'] = 0 # no meaning
                    self.session['command'] = 'comments'
                    self.c_cmts.get()
                elif selectedkey == 17: # cmtsin 15
                    self.session['sel'] = 0 # no meaning
                    self.session['command'] = 'commentsin'
                    self.c_cmts.get()
                elif selectedkey == 18: # cmtsup 16
                    self.session['sel'] = 0 # no meaning
                    self.session['command'] = 'commentsup'
                    self.c_cmts.get()
                elif selectedkey == 19: # playlistsin 17
                    self.session['sel'] = 0 # no meaning
                    self.session['command'] = 'playlistsnew'
                    self.c_plist.get()
                elif selectedkey == 20: # playlistsup 18
                    self.session['sel'] = 0 # no meaning
                    self.session['command'] = 'playlistsupdate'
                    self.c_plist.get()
                elif selectedkey == 21: # playlistsrm 19
                    self.session['sel'] = 0 # no meaning
                    self.session['command'] = 'playlistsrm'
                    self.c_plist.get()
                elif selectedkey == 22: # playlistsrm 20
                    self.session['sel'] = 0 # no meaning
                    self.session['command'] = 'search'
                    self.c_search.get()
                elif selectedkey == 23: # activity 21
                    self.session['sel'] = 0 # no meaning
                    self.session['command'] = 'activities'
                    self.c_activity.get()
                elif selectedkey == 24: # activityin 22
                    self.session['sel'] = 0 # no meaning
                    self.session['command'] = 'activitiesin'
                    self.c_activity.get()
                elif selectedkey == 25: # captions 23
                    self.session['sel'] = 0 # no meaning
                    self.session['command'] = 'captions'
                    self.c_caption.get()
                elif selectedkey == 26: # captionsin 24
                    self.session['sel'] = 0 # no meaning
                    self.session['command'] = 'captionsin'
                    self.c_caption.get()
                elif selectedkey == 27: # captionsup 25
                    self.session['sel'] = 0 # no meaning
                    self.session['command'] = 'captionsup'
                    self.c_caption.get()
                elif selectedkey == 28: # captionsrm 26
                    self.session['sel'] = 0 # no meaning
                    self.session['command'] = 'captionsrm'
                    self.c_caption.get()
                elif selectedkey == 29: # channelbanner 27
                    self.session['sel'] = 0 # no meaning
                    self.session['command'] = 'channelbanner'
                    self.c_channelbanner.get()
                elif selectedkey == 30: # channelsec 28
                    self.session['sel'] = 0 # no meaning
                    self.session['command'] = 'channelsec'
                    self.c_channelsec.get()
                elif selectedkey == 31: # channelsecin 29
                    self.session['sel'] = 0 # no meaning
                    self.session['command'] = 'channelsecin'
                    self.c_channelsec.get()
                elif selectedkey == 32: # channelsecup 30
                    self.session['sel'] = 0 # no meaning
                    self.session['command'] = 'channelsecup'
                    self.c_channelsec.get()
                elif selectedkey == 33: # channelsecdel 31
                    self.session['sel'] = 0 # no meaning
                    self.session['command'] = 'channelsecdel'
                    self.c_channelsec.get()
                elif selectedkey == 34: # guideCategory 32
                    self.session['sel'] = 0 # no meaning
                    self.session['command'] = 'guideCategory'
                    self.c_channelbanner.get()
                elif selectedkey == 35: # captions 33
                    self.session['sel'] = 0 # no meaning
                    self.session['command'] = 'captionsdw'
                    self.c_caption.get()
                else:
                    print(100)
                    break
                    
            self.redirect('/main/welcome')

        except BehaviorError:
            print('behavior error')
            self.redirect('/main/welcome')
