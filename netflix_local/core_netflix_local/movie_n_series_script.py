import requests
from .models import Movie, Country, Language, Genre, Rated, FilmPersons, MovieRole, Season, Episode
from dateutil import parser

# import logging
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s %(levelname)s: %(message)s',
#                     filemode='w')

#TODO
# creating data with the response without doing API calls (remainder)
# create episodes based on the series and seasons and check for diplicates



base_url = "http://www.omdbapi.com"
apikey = "4f912514"


def main():
    with open(r'''D:\django_projects\netflix_local\core_netflix_local\movie_n_series_list.txt''', 'r', encoding="utf-8") as file:
        try:
            for line in file:
                master_data = {}
                row = line.strip().split(",")
                movie = row[0]
                year = row[1]
                query_params = build_query_params("movie", movie, year)
                data = process_request(query_params)
                master_data["movie"] = data
                movie_id = data.get("imdbID")
                print(movie_id)
                movie = verify_movie_sync(movie_id)
                print(movie)
                if data and not movie:
                    print("enter to create a new movie")
                    if data.get("Type").lower() == "series":
                        if "totalSeasons" in data:
                            seasons = int(data.get("totalSeasons"))
                            for season in range(1, seasons + 1):
                                query_params = build_query_params("series", movie_id, season)
                                season_data = process_request(query_params)
                                master_data["season"] = season_data
                                episodes = season_data.get("Episodes")
                                episode_data = {}
                                for episode in episodes:
                                    query_params = build_query_params("episode", data.get("Title") ,int(episode.get("Episode")), season)
                                    episode_data[f"e{episode.get("Episode")}"] = process_request(query_params)
                                master_data[f"s{season}"] = episode_data
                    m_or_s = create_movies_or_series(master_data['movie'])
                    if master_data.get("movie").get("Type") == "series":
                        create_season_and_episodes(m_or_s, master_data, int(master_data.get("movie").get("totalSeasons")))
        except Exception as e:
            print(f"Exception : {e}")

def create_season_and_episodes(movie:object, season:dict, season_count:int):
    start = 1
    season_prefix = "s"
    for i in range(start, season_count+start):
        s_data = _create_get_data(model=Season, data={"name":f"Season {i}", "movie":movie, "season": str(i)})
        season_name = f"{season_prefix}{str(i)}"
        for ep in list(season.get(season_name).keys()):
            title = season.get(season_name).get(ep).get("Title")
            episode = season.get(season_name).get(ep).get("Episode")
            runtime = season.get(season_name).get(ep).get("Runtime")
            description = season.get(season_name).get(ep).get("Plot")
            episode_id = season.get(season_name).get(ep).get("imdbID")
            released = date_parser(season.get(season_name).get(ep).get("Released")) if date_parser(season.get(season_name).get(ep).get("Released")) != "N/A" else None
            _create_get_data(model=Episode, data={
                "title": title,
                "episode": episode,
                "runtime": runtime,
                "description": description,
                "episode_id": episode_id,
                "season": s_data,
                "poster": str(season.get(season_name).get(ep).get("Poster")),
                "released": released
            })

def build_query_params(type, *args):
    query_params = {'apikey': apikey}
    if type == "movie":
        query_params['t'] = args[0]
        query_params['y'] = args[1]
    elif type == "series":
        query_params['i'] = args[0]
        query_params['season'] = args[1]
    elif type == "episode":
        query_params['t'] = args[0]
        query_params['Episode'] = args[1]
        query_params['Season'] = args[2]
    return query_params

def parse_movie_data(data):
    parse_movie_data = {}
    if data:
        parse_movie_data["directors"] = data.get("Director").split(", ") if data.get("Director") and "," in data.get("Director") else [
            data.get("Director")]
        parse_movie_data["actors"] = data.get("Actors").split(", ") if data.get("Actors") and "," in data.get("Actors") else [
            data.get("Actors")]
        parse_movie_data["writers"] = data.get("Writer").split(", ") if data.get("Writer") and "," in data.get("Writer") else [
            data.get("Writer")]
        parse_movie_data["countries"] = data.get("Country").split(", ") if data.get("Country") and "," in data.get("Country") else [
            data.get("Country")]
        parse_movie_data["languages"] = data.get("Language").split(", ") if data.get("Language") and "," in data.get("Language") else [
            data.get("Language")]
        parse_movie_data["genres"] = data.get("Genre").split(", ") if data.get("Genre") and "," in data.get("Genre") else [data.get("Genre")]
    return parse_movie_data


def verify_movie_sync(movie_id):
    movie = Movie.objects.filter(imdb_id=movie_id)
    if movie:
        return True
    return False

def date_parser(date):
    date_object = parser.parse(date)
    return date_object.date()

def create_movies_or_series(data):
    parsed_movie_data = parse_movie_data(data)
    directors = parsed_movie_data.get("directors")
    actors = parsed_movie_data.get("actors")
    writers = parsed_movie_data.get("writers")
    countries = parsed_movie_data.get("countries")
    languages = parsed_movie_data.get("languages")
    genres = parsed_movie_data.get("genres")

    movies_data = {}
    director_data = []
    actor_data = []
    writer_data = []
    country_data = []
    language_data = []
    genre_data = []

    role_director = MovieRole.objects.get(name="Director")
    for director in directors:
        rec_data = _create_get_data(model=FilmPersons, data={"name" : director})
        if rec_data.roles.exists():
            roles = [role.id for role in rec_data.roles.all()]
            if role_director not in roles:
                rec_data.roles.add(role_director)
        else:
            rec_data.roles.add(role_director)
        director_data.append(rec_data)

    role_writer = MovieRole.objects.get(name="Writer")
    for writer in writers:
        rec_data = _create_get_data(model=FilmPersons, data={"name": writer})
        if rec_data.roles.exists():
            roles = [role.id for role in rec_data.roles.all()]
            if role_writer not in roles:
                rec_data.roles.add(role_writer)
        else:
            rec_data.roles.add(role_writer)
        writer_data.append(rec_data)

    role_actor = MovieRole.objects.get(name="Actor")
    for actor in actors:
        rec_data = _create_get_data(model=FilmPersons, data={"name": actor})
        if rec_data.roles.exists():
            roles = [role.id for role in rec_data.roles.all()]
            if role_writer not in roles:
                rec_data.roles.add(role_actor)
        else:
            rec_data.roles.add(role_actor)
        actor_data.append(rec_data)

    # create or update country
    for country in countries:
        country_data.append(_create_get_data(model=Country, data={'name': country}))
    # movies_data["countries"] = country_data

    # create or update language
    for language in languages:
        language_data.append(_create_get_data(model=Language, data={'name': language}))
    # movies_data["languages"] = country_data

    # create or update genre
    for genre in genres:
        genre_data.append(_create_get_data(model=Genre, data={'name': genre}))
    # movies_data["genre"] = genre_data

    # create or update rated

    rated = _create_get_data(model=Rated, data={'name': data.get("Rated")})
    # movies_data["rated"] = rated_data

    movies_data["title"] = data.get("Title")
    movies_data["description"] = data.get("Plot")
    movies_data["movie_type"] = data.get("Type").title()
    movies_data["runtime"] = data.get("Runtime")
    movies_data["awards"] = data.get("Awards")
    movies_data["rating"] = float(data.get("imdbRating")) if isinstance(data.get("imdbRating"), float) else 0.00
    movies_data["imdb_id"] = data.get("imdbID")
    movies_data["rated"] = rated
    movies_data["released"] = date_parser(data.get("Released")) if date_parser(data.get("Released")) != "N/A" else None
    movies_data["poster"] = str(data.get("Poster"))

    movie = _create_get_data(model=Movie, data=movies_data)
    movie.genre.add(*genre_data)
    movie.languages.add(*language_data)
    movie.countries.add(*country_data)
    movie.writer.add(*writer_data)
    movie.actors.add(*actor_data)
    movie.directors.add(*director_data)
    return movie

a = "https://m.media-amazon.com/images/M/MV5BZjU4OWNiYzQtMzc1NS00NjZlLTgyYTctZWY4ZmEzMTkxYjA4XkEyXkFqcGc@._V1_QL75_UX380_CR0,4,380,562_.jpg"

def _create_get_data(model, data):
    # the ** (double asterisk) operator is known as the dictionary unpacking operator.
    # data = {"name": "Alice", "age": 30} **data converts to (name='Alice', age=30)
    obj, created = model.objects.get_or_create(**data)
    return obj

def process_request(query_params):
    response = requests.get(base_url, params=query_params)
    datas = response.json()
    if datas["Response"] == "True":
        return datas
    return None