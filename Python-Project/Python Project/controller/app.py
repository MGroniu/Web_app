from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
import sqlite3
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from model.cinema_model import CinemaModel
from functools import wraps


app=Flask(__name__)

app.config['sqlite3_CURSORCLASS']='DictCursor'
database_path = app.root_path+"\..\database\cinema_booking.db"


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

################################################ LOGIN MODULE################################################################################

class RegisterForm(Form):
    name=StringField('Name',[validators.Length(min=1,max=50)])
    username=StringField('Username',[validators.Length(min=4,max=25)])
    email=StringField('Email',[validators.Length(min=6,max=50)])
    password=PasswordField('Password',[
        validators.DataRequired(),
        validators.EqualTo('confirm',message='Passwords do not match')
    ])
    confirm=PasswordField('Confirm Password')

#Register
@app.route('/register',methods=['GET','POST'])
def register():
    form=RegisterForm(request.form)
    if request.method=='POST' and form.validate():
        name=form.name.data
        email=form.email.data
        username=form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        #Create cursor
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(?, ?, ?, ?)",
                    (name, email, username, password))

        #Commit to DB
        conn.commit()

        #Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)

#User login
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        # Get for fields
        username=request.form['username']
        password_candidate=request.form['password']

        print(username)
        #Create cursor
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()

        #Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = ?", [username])

        if result!="":
            #Get stored hash
            data=cur.fetchone()
            print(data)
            if data!=None:
                password=data[4]
                print(password)

                #Compare passwords
                if sha256_crypt.verify(password_candidate,password):
                    #Passed
                    session['logged_in']=True
                    session['username']=username
                    session['id']=data[0]
                    print(session['id'])
                    flash('You are now logged in', 'success')
                    return redirect(url_for('dashboard'))
                else:
                    error = 'Invalid login'
                    flash(error,'danger')
                return render_template('login.html', error=error)
                #Close connection
                conn.close()
            else:
                error = 'Username not found'
                flash(error,'danger')
                return render_template('login.html', error=error)

    return render_template('login.html')

#Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash('Unauthorized, Please login','danger')
            return redirect(url_for('login'))
    return wrap

#Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out','success')
    return redirect(url_for('login'))

#Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    return render_template('dashboard.html')

#Editprofile
@app.route('/editprofile',methods=['GET','POST'])
@is_logged_in
def editprofile():
    conn = sqlite3.connect(database_path)
    cur = conn.cursor()

    result=cur.execute("SELECT * FROM users WHERE id = ?",[session['id']])
    data = result.fetchone()
    email=data[2]
    print(email)
    username=data[3]
    print(username)
    # Commit to DB
    conn.commit()
    conn.close()
    return render_template('editprofile.html',data=data)

#Changeusername
@app.route('/changeusername/<string:id>',methods=['GET','POST'])
@is_logged_in
def changeusername(id):
    if request.method=='POST':
        # Get for field
        username=request.form['username']
        email = request.form['email']

        #connecting to database to correct data
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()
        cur.execute("UPDATE users SET username = ?, email = ? WHERE id = ?",(username,email,id))

        # Commit to DB
        conn.commit()
        conn.close()
        flash('Username / Email changed', 'success')

        return redirect(url_for('dashboard'))


##############################################FOR USER TO BOOK TICKETS#####################################################################################

@app.route('/cinema')
def cinema():

    cinemaModel = CinemaModel(database_path=database_path)
    data = cinemaModel.get_cinema_details()

    return render_template('cinema_list.html', data = data)

@app.route('/movies/<string:id>/')
def movies(id):

    cinemaModel = CinemaModel(cinema_id=id, database_path=database_path)
    data = cinemaModel.get_movies()
    if len(data)!=0:
        print(len(data))
        return render_template('movies_list.html',data = data)

    else:
        return render_template('empty_list.html')

@app.route('/movie/<string:id>/<string:c_id>')
def movie(id,c_id):

    cinemaModel = CinemaModel(movie_id=id, cinema_id=c_id, database_path=database_path)
    data1 = cinemaModel.get_movie()
    data2 = cinemaModel.get_seat_status()
    data = []
    data.append(data1)
    data.append(data2)
    return render_template('movie_details.html',data = data)

@app.route('/book_ticket/<string:c_id>/<string:m_id>/<string:seats>', methods =['GET','POST'])
def book_ticket(c_id,m_id,seats):
    cinemaModel = CinemaModel(movie_id=m_id, cinema_id=c_id, database_path=database_path)
    cinemaModel.update_seat_status(seats=seats)
    data1 = cinemaModel.get_movie()
    data2 = cinemaModel.get_seat_status()
    data = []
    data.append(data1)
    data.append(data2)
    flash("YOU HAVE BOOK TICKET SUCCESSFULLY!!!!!",'success')
    flash("Do you want to book more seats",'success')
    return render_template('movie_details.html',data=data)

####################################################################################################################################

########################## Movie details Module#################
@app.route('/form_movie_details', methods=['GET', 'POST'])
def form_movie_details():
    cinemaModel = CinemaModel(database_path=database_path)
    data = cinemaModel.get_movie_details()
    return render_template('form_movie_details.html', data = data)


@app.route('/add_movie_details', methods=['GET', 'POST'])
def add_movie_details():
    if request.method == 'POST':
        movie_name = request.form.get('movie_name')
        movie_desc = request.form.get('movie_desc')
        data = []
        data.append(movie_name)
        data.append(movie_desc)
        cinemaModel = CinemaModel(database_path=database_path)
        message = cinemaModel.insert_movie_details(data=data)
        if message == 1:
            flash("Movie Details Successfully Added",'success')
            data = cinemaModel.get_movie_details()
            return render_template('/form_movie_details.html', data= data)
        else:
            flash("Problem with server, please try again later",'danger')
            return render_template('/form_movie_details.html')

@app.route('/delete_movie_details/<string:m_id>')
def delete_movie_details(m_id):
    cinemaModel = CinemaModel(database_path=database_path, movie_id=m_id)
    cinemaModel.delete_movie_details()
    data = cinemaModel.get_movie_details()
    return render_template('form_movie_details.html', data=data)

#########################  cinema details module##############################----------------------------------------------
@app.route('/add_cinema_details', methods=['GET', 'POST'])
def add_cinema_details():
    if request.method == 'POST':
        cinema_name = request.form.get('cinema_name')
        cinema_address = request.form.get('cinema_address')
        data = []
        data.append(cinema_name)
        data.append(cinema_address)
        print(data)
        cinemaModel = CinemaModel(database_path=database_path)
        message = cinemaModel.insert_cinema_details(data=data)
        if message == 1:
            flash("Cinema Details Successfully Added")
            data = cinemaModel.get_cinema_details()
            return render_template('/form_cinema_details.html', data= data)
        else:
            flash("Problem with server, please try again later")
            return render_template('/form_cinema_details.html')


@app.route('/form_cinema_details', methods=['GET', 'POST'])
def form_cinema_details():
    cinemaModel = CinemaModel(database_path=database_path)
    data = cinemaModel.get_cinema_details()
    return render_template('form_cinema_details.html', data = data)

@app.route('/delete_cinema/<string:c_id>')
def delete_cinema(c_id):
    print(c_id)
    cinemaModel = CinemaModel(database_path=database_path,cinema_id=c_id)
    cinemaModel.deleteCinema()
    data = cinemaModel.get_cinema_details()
    return render_template('form_cinema_details.html', data=data)

@app.route('/update_cinema_details/<string:c_id>')
def update_cinema_details(c_id):
    print(c_id)
    cinemaModel = CinemaModel(database_path=database_path,cinema_id=c_id)
    data = cinemaModel.get_cinema_details_by_id()
    return render_template('form_update_cinema_details.html', data=data)

@app.route('/update_cinema/<string:c_id>',methods =['GET','POST'])
def update_cinema(c_id):
    print(c_id)
    if request.method == 'POST':
        cinema_name = request.form.get('cinema_name')
        cinema_address = request.form.get('cinema_address')
        data = []
        data.append(cinema_name)
        data.append(cinema_address)
        print(data)
        cinemaModel = CinemaModel(database_path=database_path, cinema_id=c_id)
        message = cinemaModel.updateCinema(data=data)
        if message == 1:
            flash("Cinema Details Successfully Updated")
            data = cinemaModel.get_cinema_details()
            return render_template('/form_cinema_details.html', data= data)
        else:
            flash("Problem with server, please try again later")
            return render_template('/form_cinema_details.html')


#################################################################################
############################################# movie to cinema module ##################

@app.route('/form_movie_to_cinema', methods=['GET', 'POST'])
def form_movie_to_cinema():
    cinemaModel = CinemaModel(database_path=database_path)
    data = []
    data1 = cinemaModel.get_cinema_details()
    data2 = cinemaModel.get_all_movies()
    data3 = cinemaModel.get_all_movies_added()
    data.append(data1)
    data.append(data2)
    data.append(data3)
    print(data)
    return render_template('form_movie_to_cinema.html', data = data)


@app.route('/add_movie_to_cinema', methods=['GET', 'POST'])
def add_movie_to_cinema():
    if request.method == 'POST':
        cinema_id = request.form.get('cinemaList')
        movie_id = request.form.get('movieList')
        ticket_price = request.form.get('ticket_price')
        movie_time = request.form.get('movie_time')
        data = []
        data.append(cinema_id)
        data.append(movie_id)
        data.append(ticket_price)
        data.append(movie_time)
        print(data)
        cinemaModel = CinemaModel(database_path=database_path)
        message = cinemaModel.insert_movie_cinema_price_time(data=data)
        cinemaModel.insert_movie_cinema_seats(cinema_id,movie_id)
        if message == 1:
            flash("Movie added to Cinema")
            data = []
            data1 = cinemaModel.get_cinema_details()
            data2 = cinemaModel.get_all_movies()
            data3 = cinemaModel.get_all_movies_added()
            data.append(data1)
            data.append(data2)
            data.append(data3)
            return render_template('form_movie_to_cinema.html', data=data)
        else:
            flash("Problem with server, please try again later")
            data = []
            data1 = cinemaModel.get_cinema_details()
            data2 = cinemaModel.get_all_movies()
            data3 = cinemaModel.get_all_movies_added()
            data.append(data1)
            data.append(data2)
            data.append(data3)
            return render_template('form_movie_to_cinema.html', data=data)

@app.route('/delete_movie_to_cinema/<string:id>')
def delete_movie_to_cinema(id):
    print(id)
    cinemaModel = CinemaModel(database_path=database_path)
    cinemaModel.deleteMovieToCinema(id=id)
    data = []
    data1 = cinemaModel.get_cinema_details()
    data2 = cinemaModel.get_all_movies()
    data3 = cinemaModel.get_all_movies_added()
    data.append(data1)
    data.append(data2)
    data.append(data3)
    return render_template('form_movie_to_cinema.html', data=data)



#####################################################################
if __name__=='__main__':
    app.secret_key='secret123'
    app.run(debug=True)
