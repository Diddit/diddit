import webapp2
import base64
from webapp2_extras import auth
from webapp2_extras import sessions
from webapp2_extras.auth import InvalidAuthIdError
from webapp2_extras.auth import InvalidPasswordError

#Decorator to easily append routes to an app
class route(object):
	def __init__(self,app=webapp2.get_app(),*args,**kwargs):
		self.route_args=args
		self.route_kwargs=kwargs
		self.app=app
	def __call__(self,handler):
		self.route_kwargs['handler']=handler
		r=webapp2.Router(*self.route_args,**self.route_kwargs)
		self.app.router.add(r)
		return handler

#needs a named route named login.
#needs a named route named logout.
#needs a named put route named user

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
				lauth = self.auth
				if not lauth.get_user_by_session():
					#check to see if requiredlevel is valid
					# If handler has no login_url specified invoke a 403 error
					try:
						webapp2.redirect_to('login', abort=True,request=request,response=response,referrer_uri=base64.urlsafe_b64encode(self.request.uri))
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


@decorator to create a login response handler
class authhandler(object):
	def __init__(self,login=r'/login',logout=r'/logout',newuser=r'/newuser'):
		self.login_uri=login
		self.logout_uri=logout
		self.newuser_uri=newuser
	def __call__(self,cls):
		class AuthHandler(cls):
			def post_login(self):
				username = self.request.POST.get('username')
				password = self.request.POST.get('password')
				referrer_uri=self.request.POST.get('referrer_uri',default=None)
				rud=urllib.urlencode_b64decode(referrer_uri) if referrer_uri else AuthHandler.login_result_uri
				# Try to login user with password
				# Raises InvalidAuthIdError if user is not found
				# Raises InvalidPasswordError if provided password doesn't match with specified user
				try:
					self.auth.get_user_by_password(username, password)
					self.redirect_to(rud)
				except (InvalidAuthIdError, InvalidPasswordError), e:
					# Returns error message to self.response.write in the BaseHandler.dispatcher
					# Currently no message is attached to the exceptions
					return e
				finally:
					sessions.get_store(request=self.request).save_sessions(self.response)
					
					
			def post_logout(self):
				auth.get_auth().unset_session()

				# User is logged out, let's try redirecting to login page
				try:
					self.redirect(self.logout_result)
				except (AttributeError, KeyError), e:
					return "User is logged out"
				finally:
					sessions.get_store(request=self.request).save_sessions(self.response)
			def post_newuser(self):
				try:
					post_login(self):
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
							self.redirect_to('login', abort=True)
						except (AttributeError, KeyError), e:
							self.abort(403)
		
		webapp2.get_app().router.add(webapp2.Route(self.login_uri,name='login',handler=AuthHandler,methods=['POST'],handler_method='post_login'))
		#todo: all 6 routes here
		
		
		
		
@gaut.authhandler()
class LoginHandler(webapp2.BaseHandler):
	def get_login(self,referrer_uri):
		pass
	def get_logout(self,referrer_uri):
		pass
	def get_newuser(self,referrer_uri):
		pass
	


	