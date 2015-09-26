import cgi
from google.appengine.api import users
import webapp2
import gaut

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'e9c3848d099ab861f85ab1e6b6dac123',
}
app = webapp2.WSGIApplication([], debug=True,config=config)

MAIN_PAGE_HTML = """\
<html>
  <body>
     You are logged in as user_id {username}
  </body>
</html>
"""

@gaut.route(app,'/')
class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write(MAIN_PAGE_HTML.format(username='Mainpage'))


@gaut.route(app,'/profile')
@gaut.authentication_required()
class Profile(webapp2.RequestHandler):
    def get(self):
	u=gaut.get_user()
	if(u):
		uselect=u.nickname()
	else:
		uselect='Anonymous'
        self.response.write(MAIN_PAGE_HTML.format(username=uselect))
	
@gaut.route(app,'/sign')
class Guestbook(webapp2.RequestHandler):
    def post(self):
        self.response.write('<html><body>You wrote:<pre>')
        self.response.write(cgi.escape(self.request.get('content')))
        self.response.write('</pre></body></html>')

@gaut.authroute(app)
class LoginHandler(gaut.AuthHandler):
	pass
