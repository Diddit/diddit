from google.appengine.ext import ndb
class PermissionsModel(ndb.Model):
	read=ndb.KeyProperty(indexed=True,repeated=True,required=True)
	edit=ndb.KeyProperty(indexed=True,repeated=True,required=True)
	mark=ndb.KeyProperty(indexed=True,repeated=True,required=True)
	assign=ndb.KeyProperty(indexed=True,repeated=True,required=True)

class Task(ndb.Model):
	permissions=ndb.StructuredProperty(PermissionsModel,indexed=True)
	id_hash=ndb.ComputedProperty()
	title=ndb.StringProperty()
	type=ndb.StringProperty(indexed=True)
	client_data=ndb.JsonProperty(indexed=False)
	customers=ndb.KeyProperty(Task,indexed=True)
	last_updated=ndb.DateTimeProperty(indexed=True,auto_now=True)
	