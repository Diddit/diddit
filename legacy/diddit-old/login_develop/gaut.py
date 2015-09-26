import webapp2
import urllib
import base64
from webapp2_extras import auth
from webapp2_extras import sessions
from webapp2_extras.auth import InvalidAuthIdError
from webapp2_extras.auth import InvalidPasswordError

#Decorator to easily append routes to an app
class route(object):
	def __init__(self,app,*args,**kwargs):
		self.route_args=args
		self.route_kwargs=kwargs
		self.app=app
	def __call__(self,handler):
		self.route_kwargs['handler']=handler
		r=webapp2.Route(*self.route_args,**self.route_kwargs)
		self.app.router.add(r)
		return handler
class User(object):
	def __init__(self,user_id,nickname=None):
		self.muser_id=user_id
		if(nickname):
			self.mnickname=nickname
		else:
			self.mnickname="User_"+str(user_id)
	def user_id(self):
		return self.muser_id
	def nickname(self):
		return self.mnickname
		
def get_user(a=None):
	if(not a):
		a=auth.get_auth()
	udict=a.get_user_by_session()
	if(udict):
		return User(udict['user_id'])
	return None
#Decorator to require a login by inheriting from a wrapper
class authentication_required(object):
	def __init__(self,authlevel=100):
		self.authlevel=authlevel
	def __call__(self,cls):
		class AuthVersion(cls):
			requiredlevel=self.authlevel
			def dispatch(self):
					try:
						if(self.attempt_login()):
							response = super(AuthVersion, self).dispatch()
							self.response.write(response)
					finally:
						self.session_store.save_sessions(self.response)

			def attempt_login(self):
				self.user=get_user(self.auth)
				if not self.user:
					#check to see if requiredlevel is valid
					# If handler has no login_url specified invoke a 403 error
					try:
						self.redirect_to('get_login',referrer_uri=base64.urlsafe_b64encode(self.request.uri))
					except (AttributeError, KeyError), e:
						webapp2.abort(403)
					return False
				else:
					return True

			@webapp2.cached_property
			def auth(self):
				return auth.get_auth()

			@webapp2.cached_property
			def session_store(self):
				return sessions.get_store(request=self.request)
		return AuthVersion


#decorator to create a login response handler
class authroute(object):
	def __init__(self,app,login=r'/login',logout=r'/logout',newuser=r'/newuser',default='/',enable_google_logins=False):
		self.app=app
		self.login_uri=login
		self.logout_uri=logout
		self.newuser_uri=newuser
		self.default_uri=default
		self.enable_google_logins=enable_google_logins
	def __call__(self,cls):
		cls.login_uri=self.login_uri
		cls.logout_uri=self.logout_uri
		cls.newuser_uri=self.newuser_uri
		cls.default_uri=self.default_uri
		cls.enable_google_logins=self.enable_google_logins
		
		self.app.router.add(webapp2.Route(self.login_uri,name='post_login',handler=cls,methods=['POST'],handler_method='post_login'))
		self.app.router.add(webapp2.Route(self.logout_uri,name='post_logout',handler=cls,methods=['POST'],handler_method='post_logout'))
		self.app.router.add(webapp2.Route(self.newuser_uri,name='post_newuser',handler=cls,methods=['POST'],handler_method='post_newuser'))
		self.app.router.add(webapp2.Route(self.login_uri,name='get_login',handler=cls,methods=['GET'],handler_method='get_login'))
		self.app.router.add(webapp2.Route(self.logout_uri,name='get_logout',handler=cls,methods=['GET'],handler_method='get_logout'))
		self.app.router.add(webapp2.Route(self.newuser_uri,name='get_newuser',handler=cls,methods=['GET'],handler_method='get_newuser'))
		
		return cls
	
	
	
DEFAULT_LOGIN_PAGE="""
<html>
  <body>
    <form action="{login_uri}" method="post">
      <div><input type="text" name="username" value="Username" cols="60"></input></div>
      <div><input type="password" name="password" cols="60"></input></div>
      <div><input type="hidden" name="referrer_uri" value="{referrer_uri}"></input></div>
      <div><input type="submit" value="Login"></div>
    </form>
  </body>
</html>
"""
DEFAULT_NEWUSER_PAGE="""
<html>
  <body>
    <form action="{newuser_uri}" method="post">
      <div><input type="text" name="username" value="Username" cols="60"></input></div>
      <div><input type="password" name="password" cols="60"></input></div>
      <div><input type="hidden" name="referrer_uri" value="{referrer_uri}"></input></div>
      <div><input type="submit" value="New User"></div>
    </form>
  </body>
</html>
"""
		
class AuthHandler(webapp2.RequestHandler):
	#def __init__(self,enable_google_logins=False):
	#	self.enable_google_logins=False
	@webapp2.cached_property
	def auth(self):
		return auth.get_auth()
	def get_login(self,referrer_uri=None):
		referrer_uri=base64.urlsafe_b64encode(self.default_uri) if not referrer_uri else referrer_uri
		
		rbody=DEFAULT_LOGIN_PAGE.format(login_uri=self.login_uri,referrer_uri=referrer_uri)
		self.response.out.write(rbody)
		
	def get_logout(self,referrer_uri=None):
		#self.redirect_to('post_logout')
		self.post_logout()
	def get_newuser(self,referrer_uri=None):
		referrer_uri=base64.urlsafe_b64encode(self.default_uri) if not referrer_uri else referrer_uri
		
		rbody=DEFAULT_NEWUSER_PAGE.format(newuser_uri=self.newuser_uri,referrer_uri=referrer_uri)
		self.response.out.write(rbody)
		
	def try_login(self):
		username = self.request.POST.get('username')
		password = self.request.POST.get('password')
		self.auth.get_user_by_password(username, password)
	def post_login(self):
		referrer_uri=self.request.POST.get('referrer_uri',default=None)
		rud=base64.urlsafe_b64decode(str(referrer_uri)) if referrer_uri else self.default_uri
		
		# Try to login user with password
		# Raises InvalidAuthIdError if user is not found
		# Raises InvalidPasswordError if provided password doesn't match with specified user
		try:
			self.try_login()
			self.redirect(rud)
		except (InvalidAuthIdError, InvalidPasswordError), e:
			# Returns error message to self.response.write in the BaseHandler.dispatcher
			# Currently no message is attached to the exceptions
			return e
		finally:
			sessions.get_store(request=self.request).save_sessions(self.response)
			
			
	def post_logout(self):
		self.auth.unset_session()

		# User is logged out, let's try redirecting to login page
		#try:
		#	self.redirect(self.default_uri)
		#except (AttributeError, KeyError), e:
		#	return "User is logged out"
		#finally:
		self.redirect(self.default_uri)
		sessions.get_store(request=self.request).save_sessions(self.response)
	def post_newuser(self):
		try:
			self.try_login()
		except (InvalidAuthIdError, InvalidPasswordError), e:
			username = self.request.POST.get('username')
			password = self.request.POST.get('password')
			# Passing password_raw=password so password will be hashed
			# Returns a tuple, where first value is BOOL. If True ok, If False no new user is created
			user = self.auth.store.user_model.create_user(username, password_raw=password)
			if not user[0]: #user is a tuple
				return user[1] # Error message
			else:
				# User is created, let's try redirecting to login page
				try:
					self.redirect_to('get_login')
				except (AttributeError, KeyError), e:
					self.abort(403)
	