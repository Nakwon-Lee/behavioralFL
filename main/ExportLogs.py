import csv
import os

from BaseHandler import BaseHandler
from BehaveLog import Behavlog

from GlobalVar import LIST_LENGTH
from GlobalVar import VEC_LENGTH

class ExportLogs(BaseHandler):
    def get(self):
        log_query = Behavlog.query()
        logs = log_query.fetch()

        labellist = []
        vectorlist = []

        for low in logs:

            templist = []

            for i in range(VEC_LENGTH):
                for j in range(VEC_LENGTH):
                    templist.append(0)

            for i in range(0,LIST_LENGTH-1):
                for j in range(i+1,LIST_LENGTH):
                    if low.vector[i] >= 0 and low.vector[j] >= 0:
                        templist[(VEC_LENGTH*low.vector[i])+low.vector[j]] = 1

            vectorlist.append(templist)
            labellist.append(low.sflabel)

        for i in range(len(labellist)):
            print(labellist[i])
            print(vectorlist[i])

        