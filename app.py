from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from flask import render_template
app = Flask(__name__)


# change to name of your database; add path if necessary
#db_name = 'database.db'

app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'

app.config['SECRET_KEY'] = "random string"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy(app)

class database(db.Model):
    id = db.Column('form_id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    mobilenumber = db.Column(db.String(20))
    email = db.Column(db.String(200))
    gender= db.Column(db.String(10))
    subject= db.Column(db.String(10))

    def __init__(self, name, mobilenumber, email, gender,subject):
        self.name = name
        #self.id=id
        self.mobilenumber = mobilenumber
        self.email = email
        self.gender = gender
        self.subject=subject


   
# NOTHING BELOW THIS LINE NEEDS TO CHANGE
# this route will test the database connection and nothing more
"""@app.route('/')
def testdb():
    try:
        db.session.query(text('1')).from_statement(text('SELECT 1')).all()
        return '<h1>Database success</h1>'
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text"""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/formpage1')
def formpage1():
    return render_template('form.html')

@app.route('/enquiries')
def enquiries():
    view = database.query.all()
    return render_template('view.html', msg=view)

@app.route('/enquiryid/<id>')
def enquiryid(id):
    myid=id
    query = database.query.get(myid)
    return render_template('enquiryid.html', msg=query)

@app.route('/form/<id>')
def form(id):
    myid=id
    user = database.query.filter_by(id=2).first()
    user.email = 'my_new_email@example.com'
    db.session.commit()
    return render_template('index.html', msg="Successfully updated")

   
@app.route('/forms', methods = ['GET', 'POST','DELETE'])
def forms():
    if request.method == 'POST':
        formdata = database(name=request.form['name'], mobilenumber=request.form['mobilenumber'],
                          email=request.form['email'],gender= request.form['gender'],subject=request.form['subject'])

        db.session.add(formdata)
        db.session.commit()
        #flash('Record was successfully added')
        return render_template('index.html')

    if request.method=='GET':
        view = database.query.all()
        return render_template('view.html', msg=view)

    if request.method=='DELETE':
        database.query.filter(database.id == 3).delete()
        return render_template('index.html', msg="Successfully deleted")

    #return render_template('index.html')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

