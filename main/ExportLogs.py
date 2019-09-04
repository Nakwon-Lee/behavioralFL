import csv
import os

from BaseHandler import BaseHandler
from BehaveLog import Behavlog

import jinja2

LOG_LENGTH = 38

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    autoescape=True,
    extensions=['jinja2.ext.autoescape'])

class ExportLogs(BaseHandler):
    def get(self):
        log_query = Behavlog.query()
        logs = log_query.fetch()

        dictlist = []

        for low in logs:
            newdic = {}
            for i in range(LOG_LENGTH):
                newdic[str(i)] = low.vector[i]
            newdic['sflabel'] = low.sflabel
            dictlist.append(newdic)
        
        variables = {
            'diclist': dictlist
        }

        template = JINJA_ENVIRONMENT.get_template('templates/logsview.html')
        self.response.write(template.render(variables))