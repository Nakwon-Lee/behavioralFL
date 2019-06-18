from BaseHandler import BaseHandler
from BehaveLog import Behavlog
from apiclient.errors import HttpError
from apiclient.discovery import build
from apiclient.http import MediaFileUpload

import google.oauth2.credentials

import Keys

class R_ChannelBanner(BaseHandler):
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

                if command == 'channelbanner':
                    response = youtube.channelBanners().insert(media_body=MediaFileUpload('banner.jpg')).execute()

                    strurl = response.get('url')

                    self.session['bannerurl'] = strurl

                    thislog.vector[32] = 1

                elif command == 'guideCategory':

                    channelid = self.session['channel']

                    response = youtube.guideCategories().list(part='id,snippet',id=channelid).execute()

                    items = []

                    for item in response.get('items',[]):
                        items.append(item)

                    print(response)

                    thislog.vector[33] = 1

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