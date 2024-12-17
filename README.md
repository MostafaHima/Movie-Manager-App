# Movie Manager App

A Flask-based web application that allows users to search for movies, add them to a database, update their ratings and reviews, and delete entries. The app integrates with The Movie Database (TMDB) API to fetch movie details.

## Features
1. **Home Page**: Displays a list of movies sorted by their rating in descending order.
2. **Add a Movie**: Search for a movie title using TMDB API and add it to the database.
3. **Edit Movie**: Update a movie's rating and review.
4. **Delete Movie**: Remove a movie entry from the database.
5. **Ranking System**: Automatically ranks movies based on their ratings.

## Technologies Used
- **Python**: Core language for backend development.
- **Flask**: Web framework for building the application.
- **Flask-Bootstrap**: For integrating Bootstrap to improve UI design.
- **Flask-SQLAlchemy**: For database management.
- **WTForms**: To manage forms for adding and editing movie details.
- **TMDB API**: To fetch movie details such as titles, posters, and descriptions.
- **SQLite**: Database to store movie information.
- **HTML/CSS**: Frontend structure and styling.

## Installation
### 1. Clone the Repository
```bash
https://github.com/MostafaHima/Movie-Manager-App.git
cd Movie-Manager-App
```

### 2. Install Dependencies
Make sure you have Python installed, then run:
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the project root directory to store your secret key and API configurations:
```env
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///Movies_database.db
```

### 4. Run the Application
```bash
python main.py
```
The app will be accessible at `http://127.0.0.1:5000/`.

## Usage
1. Visit the **home page** to view your movie list.
2. Click **Add Movie** to search for a new movie title.
3. Edit a movie's rating or review by clicking **Edit**.
4. Delete a movie by clicking **Delete**.

## API Integration
The app uses [The Movie Database (TMDB)](https://www.themoviedb.org/) API to fetch movie details. You must provide an API token for authentication.

### API Example:
- **Search Movie**: `https://api.themoviedb.org/3/search/movie?query=<movie_title>`
- **Movie Details**: `https://api.themoviedb.org/3/movie/<movie_id>`

## Database
- The app uses SQLite as the database backend.
- A table `Movie` is created to store movie details with the following schema:
  - `id`: Primary key
  - `title`: Movie title
  - `year`: Release year
  - `description`: Movie overview
  - `rating`: User-defined rating
  - `ranking`: Rank based on rating
  - `review`: User review
  - `img_url`: Poster image URL

## Dependencies
- Flask
- Flask-Bootstrap
- Flask-SQLAlchemy
- Flask-WTF
- Requests



