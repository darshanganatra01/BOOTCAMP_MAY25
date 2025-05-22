from flask import Flask,render_template,request,redirect,session,flash
from flask_sqlalchemy import SQLAlchemy

#installing
#importing 
#configuration
#initialization
#integrating
#usage

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bootcamp.db' #config
app.config['SECRET_KEY']='saltnpepper'

db = SQLAlchemy()  #initialization

db.init_app(app)  #integrating

app.app_context().push()

# ORM Object relational mapping 
# mapping relational database to the python classes (objects)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True ,autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Album(db.Model):
    __tablename__ = 'albums'
    a_id = db.Column(db.Integer, primary_key=True ,autoincrement=True)
    album_name = db.Column(db.String(80), unique=True, nullable=False)

class Song(db.Model):
    __tablename__ = 'songs'
    s_id = db.Column(db.Integer, primary_key=True ,autoincrement=True)
    song_name = db.Column(db.String(80), unique=True, nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey(Album.a_id), nullable=False)
    album = db.relationship(Album,backref='songs',lazy=True)



db.create_all()  #creating the database


@app.route('/')
def landing():
    return render_template('landing.html')



#route methods by default allows only GET requests!
#methods is the list that states the only allowed methods in the routes

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        print(username,password)

        user_exist=User.query.filter_by(username=username).first()

        if user_exist:
            if user_exist.password == password:
                print("Password is correct")
                session['username']=username
                return redirect('/dashboard')
            else:
                print("Password is incorrect")
                flash("Password is incorrect","error")
                return render_template('login.html',error="Password is incorrect")
        else:
            print("User doesn't exist")
            return redirect('/signup')


@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='GET':
        return render_template('signup.html')
    else:
        formusername = request.form.get('username')
        formpassword = request.form.get('password')

        user_exists=User.query.filter_by(username=formusername).first()
        if user_exists:
            print("User already exists please use a different username")
            return redirect('/signup')
        else:
            new_user=User(username=formusername,password=formpassword)
            db.session.add(new_user)
            db.session.commit()
            print("User created successfully")
            return redirect('/login')
        

@app.route('/dashboard')  #user:string
def dashboard():
    user=session['username']
    albums = Album.query.all()
    return render_template('Dashboard.html',Dashusername=user,jinjaalbums=albums)

@app.route('/add_album',methods=['GET','POST'])
def add_album():
    if request.method=="GET":
        return render_template('add_album.html')
    else:
        formalbum_name = request.form.get('album_name')
        print(formalbum_name)
        album_exists = Album.query.filter_by(album_name=formalbum_name).first()
        if album_exists:
            print("Album Already exists")
            flash("Album Already exists","error")
            return redirect('/add_album')
        else:
            new_album = Album(album_name=formalbum_name)
            db.session.add(new_album)
            db.session.commit()
            print("Album created successfully")
            return redirect('/dashboard')
        
        
@app.route('/edit_album/<albumid>',methods=['GET','POST'])
def edit_album(albumid):
    if request.method=="GET":
        album=Album.query.filter_by(a_id=albumid).first()
        album_name = album.album_name
        album_id = album.a_id
        return render_template('edit_album.html',jinjaalbumname=album_name,jinjaalbumid=album_id)
    else:
        edited_album_name = request.form.get('album_name')
        check_album = Album.query.filter_by(album_name=edited_album_name).first()
        if check_album:
            print("Album already exists")
            flash("Album already exists try different name","error")
            return redirect('/edit_album/'+albumid)
        else:
            album=Album.query.filter_by(a_id=albumid).first()
            album.album_name = edited_album_name
            db.session.commit()
            print("Album edited successfully")
            return redirect('/dashboard')


        
def create_auto_admin():
    if_exists = User.query.filter_by(is_admin=True).first()
    if not if_exists:
        admin = User(username='admin', password='passadmin',is_admin=True)
        db.session.add(admin)
        db.session.commit()
        print("Admin got created")
    else:
        print("Admin already exists")

   
if __name__ == "__main__":
    create_auto_admin()
    app.run(debug=True)

