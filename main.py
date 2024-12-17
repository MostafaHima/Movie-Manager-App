# ------------------------------------- IMPORT LIBRARIES ---------------------------------------------------------------
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import secrets


# -------------------------------- CREATING FORM TO SEARCH ABOUT MOVIE -------------------------------------------------
class AddMovieForm(FlaskForm):
    title = StringField(label="Movie Title", validators=[DataRequired()], render_kw={"placeholder": "Phone Both"})
    submit = SubmitField(label="Search")


# ----------------------------- CREATE FORM TO UPDATE RATING AND REVIEW ------------------------------------------------
class RateMovieForm(FlaskForm):
    rating = StringField(label="New Rating", render_kw={"placeholder": "6.8"})
    review = StringField(label="New_Review")
    submit = SubmitField(label="Submit")


# SETTING APP FLASK
app = Flask(__name__)
app.secret_key = secrets.token_hex(31)
Bootstrap5(app)


# -------------------------------------------- CREATE DB ---------------------------------------------------------------
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Movies_database.db"
db.init_app(app=app)


# --------------------------------------------- CREATE TABLE -----------------------------------------------------------
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(250), nullable=True)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)


# ---------------------------------------- CREATING DATABASE MOVIES ----------------------------------------------------
with app.app_context():
    db.create_all()


# ------------------------------------------- HOME PAGE ----------------------------------------------------------------
@app.route("/")
def home():
    display_info = db.session.query(Movie).all()
    sorted_movies = sorted(display_info, key=lambda x: x.rating, reverse=True)

    for index, movie in enumerate(sorted_movies, start=1):
        movie.ranking = index
    db.session.commit()
    return render_template("index.html", movies=sorted_movies)


# -------------------------------------------- UPDATE PAGE -------------------------------------------------------------
@app.route("/edit", methods=["POST", "GET"])
def edit():
    form = RateMovieForm()
    id_ = request.args.get("id")

    update_some_info = db.session.execute(db.select(Movie).where(Movie.id == id_)).scalar()

    if form.validate_on_submit():

        new_rating = form.rating.data
        if new_rating == "":
            new_rating = update_some_info.rating
        else:
            update_some_info.rating = float(new_rating)

        new_review = form.review.data
        if new_review == "":
            update_some_info.review = update_some_info.review
        else:
            update_some_info.review = new_review

        db.session.commit()
        return redirect("/")

    return render_template("edit.html", form=form)


# --------------------------------------- DELETE PAGE ------------------------------------------------------------------
@app.route("/delete")
def delete():
    id_ = request.args.get('id')
    delete_movie = db.session.execute(db.select(Movie).where(Movie.id == id_)).scalar()
    if delete_movie is not None:
        db.session.delete(delete_movie)
        db.session.commit()
        return redirect(url_for("home"))


# ----------------------------------------------- ADD NEW MOVIE --------------------------------------------------------
@app.route("/add", methods=["POST", "GET"])
def add():
    form = AddMovieForm()
    if form.validate_on_submit():
        movie_title = form.title.data
        url = f"https://api.themoviedb.org/3/search/movie?query={movie_title}&include_adult=true&language=en-US"

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3M2RkNGQwNDAzNzhmNzdmZDAzN2NhZTY1Y2M4NWZjZSIsIm5"
                             "iZiI6MTczMTYyNDg2NC4wNzc1NDUyLCJzdWIiOiI2NzM2N2RmOWZmZTM4NzhlOWU5ZmE1NjgiLCJzY29wZXMiOls"
                             "iYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.RrtLsiJQnKXD672uib4NIYeCs3dFJOXFrQohzgg6ks0"
        }

        response = requests.get(url, headers=headers)
        movies = response.json()["results"]
        return render_template("select.html", movies=movies, movie_title=movie_title)

    return render_template("add.html", form=form)


# ----------------------------------------- FIND MOVIE FORM DATABASE API -----------------------------------------------
@app.route("/find")
def find_movie():

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3M2RkNGQwNDAzNzhmNzdmZDAzN2NhZTY1Y2M4NWZjZSIsIm5"
                         "iZiI6MTczMTYyNDg2NC4wNzc1NDUyLCJzdWIiOiI2NzM2N2RmOWZmZTM4NzhlOWU5ZmE1NjgiLCJzY29wZXMiOls"
                         "iYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.RrtLsiJQnKXD672uib4NIYeCs3dFJOXFrQohzgg6ks0"}

    id_ = request.args.get("id")
    url = f"https://api.themoviedb.org/3/movie/{id_}?language=en-US"
    data = requests.get(url=url, headers=headers).json()

    title = data["title"]
    poster_img = data["poster_path"]
    overview = data["overview"]
    year = int(data["release_date"].split('-')[0])

    with app.app_context():

        try:
            new_movie = Movie(
                title=title,
                year=year,
                description=overview,
                rating=0,
                ranking=0,
                review="",
                img_url=f"https://image.tmdb.org/t/p/w500/{poster_img}"
            )

            db.session.add(new_movie)
            db.session.commit()

        except IntegrityError:
            db.session.rollback()
            print("The Movie already here")
            
    return redirect("/")


# ---------------------------------------- RUN CODE --------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)

