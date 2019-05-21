from google.appengine.ext import ndb

class Behavlog(ndb.Model):
    remoaddr = ndb.StringProperty(indexed=True)
    startdate = ndb.DateTimeProperty(auto_now_add=True)
    vector = ndb.JsonProperty()
    sflabel = ndb.BooleanProperty(default=False)