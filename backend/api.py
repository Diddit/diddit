from flask import Flask
import models

app = Flask(__name__)
app.config['DEBUG'] = True

#use error payloads
#http://blog.mwaysolutions.com/2014/06/05/10-best-practices-for-better-restful-api/

@app.route('/v1/tasks',methods=['POST','GET','PUT'])
def tasks():
	pass	#returns all tasks for the current permissions or creates a new task

@app.route('/v1/tasks/<id>',methods=['GET','DELETE','PUT','POST'])
def tasks(id):
	pass

@app.route('/v1/tasks/<id>/customers',methods=['GET','DELETE','PUT','POST'])
def tasks_customers():
	pass

@app.route('/v1/tasks/<task_id>/customers/<cutomer_id>',methods=['GET','DELETE','PUT','POST'])
def tasks_customers(id)
	pass


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404

