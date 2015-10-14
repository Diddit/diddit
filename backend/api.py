from flask import Flask
app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/tasks',methods=['POST','GET','PUT'])
def tasks():
	pass	#returns all tasks for the current permissions or creates a new task

@app.route('/task/<id>',methods=['GET','PUT','POST','DELETE'])
def task(id):
	pass

@app.route('/task/<id>/customers',methods=['GET','DELETE','PUT','POST'])
def task_customers(id):
	pass

@app.route('/task/<id>/customer/<id>'):
	pass

#@app.route('/task/<id>/customers/<customer>',methods=['GET','PUT','POST'])
#def task_customers(id=None,customer=None):
	



@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404

