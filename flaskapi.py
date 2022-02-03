"""Code for a flask API to Create, Read, Update, Delete users"""
import os
from flask import Flask,render_template, redirect, url_for
from flask import request,jsonify 
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()

# MySQL configurations
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = os.getenv("db_root_password")
app.config["MYSQL_DATABASE_DB"] = os.getenv("db_name")
app.config["MYSQL_DATABASE_HOST"] = os.getenv("MYSQL_SERVICE_HOST")
#app.config["MYSQL_DATABASE_PORT"] = 3306
app.config["MYSQL_DATABASE_PORT"] = int(os.getenv("MYSQL_SERVICE_PORT"))
mysql.init_app(app)

print("#########################################")
print(os.getenv("db_root_password"))
print(os.getenv("db_name"))
print(os.getenv("MYSQL_SERVICE_HOST"))
print("#########################################")


# To render home page
@app.route("/")
def home():
    return render_template('index.html')
# To render index page
@app.route("/index")
def index():
    return render_template('index.html')

# To render the create movie page
@app.route("/create_movie")
def create_movie_page():
    return render_template('create_movie.html')


# To create movie and redirect to a url 
@app.route("/new_movie",methods = ['POST','GET'])
def new_movie():
    
    # First create the database connection
    conn = mysql.connect()
    cursor = conn.cursor()
    
    if request.method =='POST':
        new_movie = request.form["movie_name"]
        new_director = request.form['director_name']
        ratings = request.form['ratings']
        create_new_movie = """
        INSERT INTO movie ( movie_name, director_name ,ratings)
        VALUES(%s, %s, %s)
        """
        data = (new_movie,new_director,ratings)
        cur = cursor.execute(create_new_movie, data)
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for("index"))

# To display all movies
@app.route("/movieslist",methods = ['GET'])
def movieslist():
    # Let's first create a database connection to get all movies data
    conn = mysql.connect()
    cursor = conn.cursor()
    get_all_movie = """
        select * from movie
    """
    if request.method == 'GET':
        results = cursor.execute(get_all_movie)
        all_movies = [
            {'id':data[0],
            "movie_name":data[1],
            "director_name":data[2],
            "ratings":data[3] }
            for data in cursor.fetchall()
        ]
        cursor.close()
        conn.close()
        return render_template('all_movies.html',result1 = all_movies), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
