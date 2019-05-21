import os
import jinja2
from BaseHandler import BaseHandler

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    autoescape=True,
    extensions=['jinja2.ext.autoescape'])

class YouTubePlayer(BaseHandler):
    def get(self):
        videoid = self.session['videoid']
        template_vars = {
                    'name' : 'my',
                    'youtubesrc' : ('http://www.youtube.com/embed/'+videoid)
                }
        template = JINJA_ENVIRONMENT.get_template('templates/player2.html')
        self.response.write(template.render(template_vars))