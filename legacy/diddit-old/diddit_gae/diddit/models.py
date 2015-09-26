from google.appengine.ext import ndb

class Item(ndb.Model):
	read_permissions=ndb.UserProperty(repeated=True)
	write_permissions=ndb.UserProperty(repeated=True)
	child_permissions=ndb.UserProperty(repeated=True)
	assigned_to=ndb.UserProperty(repeated=True)
	
	category=ndb.StringProperty(default='Item')
	description=ndb.StringProperty()
	inherited_data=PickleProperty(default={})
	
	satisfied=ndb.BooleanProperty(default=False)
	number_unsatisfied_children=ndb.IntegerProperty(default=0)
	parents=ndb.KeyProperty(repeated=True)
	
	
	creation_date=ndb.DateTimeProperty(auto_now_add=True)
	last_modified_date=ndb.DateTimeProperty(auto_now=True)

	

