"""
gptproject.py - Module for handling movie data operations, including\
 reading data from CSV files and writing to text files.

This module provides functionality to:
- Read movie data from a CSV file, optionally filtering based on the year.
- Write lists of movie titles and ratings to a text file.

Functions:
-----------
read_file(pathname: str, year: int = 0) -> list
    Reads a CSV file containing movie data and returns the data as a list of lists.
    If a year is specified, it filters movies released after the given year.

write_file(top: list, file_name: str)
    Writes a list of movie titles and ratings to a specified file, each entry on a new line.
    Each line follows the format: "Title, rating".

Usage Example:
--------------
# Reading movies from a file, filtering by year 2000
movies = read_file("movies.csv", 2000)

# Writing selected movies and ratings to a text file
write_file([('Inception', 8.8), ('The Matrix', 8.7)], "top_movies.txt")
"""

def read_file(pathname: str, year: int = 0) -> list:
    """
    Reads a CSV file containing movie data and returns the data as a list of lists.

    Each movie entry is represented as a list of fields:
    ['ank', 'Title', 'Genre', 'Description', 'Director', 'Actors', 'Year',
     'Runtime (Minutes)', 'Rating', 'Votes', 'Revenue (Millions)', 'Metascore'].

    :param pathname: The file path to the CSV file.
    :param year: An optional starting year to filter movies by release date.
                 Only movies from this year onward will be included.
                 Default is 0, meaning no filtering.
    :return: A list of lists, where each inner list represents a movie entry.

    Example usage:
    >>> read_file('films.csv', 2014)[:2]
    [['1', 'Guardians of the Galaxy', 'Action,Adventure,Sci-Fi', \
'A group of intergalactic criminals are forced to work together to stop a fanatical \
warrior from taking control of the universe.', \
'James Gunn', 'Chris Pratt, Vin Diesel, Bradley Cooper, Zoe Saldana', '2014', '121', \
'8.1', '757074', '333.13', '76.0'], ['3', \
'Split', 'Horror,Thriller', 'Three girls are kidnapped by a man with a diagnosed 23 \
distinct personalities. They must try to \
escape before the apparent emergence of a frightful new 24th.', 'M. Night Shyamalan', \
'James McAvoy, Anya Taylor-Joy, Haley Lu Richardson, Jessica Sula', \
'2016', '117', '7.3', '157606', '138.12', '62.0']]
    """

    movie_data = []
    header_skipped = False  # Flag to skip the first row

    with open(pathname, mode='r', encoding='utf-8') as file:
        for line in file:
            if not header_skipped:  # Skip the first line
                header_skipped = True
                continue

            row = line.strip().split(';')
            movie_year = int(row[6])

            if year == 0 or movie_year >= year:
                movie_data.append(row)

    return movie_data


def top_n(data, genre='', n=0):
    """
    Filters movies by genre, calculates an adjusted rating based on actor ratings,
    and returns the top n movies sorted by combined rating.

    :param data: List of movies, where each movie is represented as a list of fields.
    :param genre: Filter for specific genres (comma-separated). Defaults to '' (all genres).
    :param n: Number of top-rated movies to return. Defaults to 0 (return all).
    :return: List of tuples (Title, Average_rating), sorted by rating in descending order.

    Example usage:
    >>> top_n(read_file('films.csv', 2014), genre='Action', n=5)
    [('Dangal', 8.8), ('Bahubali: The Beginning', 8.3), ('Guardians of the Galaxy', 8.1),\
 ('Mad Max: Fury Road', 8.1), ('Star Wars: Episode VII - The Force Awakens', 8.1)]
    """

    def get_highest_rating_for_actor(actor, all_movies):
        # Find the highest rating for any movie that the actor appears in
        return max(float(movie[8]) for movie in all_movies if actor in movie[5])

    # Split genre parameter for handling multiple genres (if specified)
    genre_list = [g.strip() for g in genre.split(',')] if genre else []

    # Filter data by genre
    filtered_movies = [
        movie for movie in data
        if not genre_list or any(g in movie[2] for g in genre_list)
    ]

    # Calculate actor ratings and combined ratings for each movie
    movie_ratings = []
    for movie in filtered_movies:
        title = movie[1]
        movie_rating = float(movie[8])
        actors = movie[5].split(', ')

        # Calculate actor_rating as the average of the highest ratings for each actor
        actor_ratings = [get_highest_rating_for_actor(actor, data) for actor in actors]
        actor_rating = sum(actor_ratings) / len(actor_ratings)

        # Store as (Title, Rating, Actor_Rating)
        movie_ratings.append((title, movie_rating, actor_rating))

    # Define a helper function for sorting by combined rating and title
    def sort_key(movie_info):
        # movie_info is in the format (Title, Rating, Actor_Rating)
        title, movie_rating, actor_rating = movie_info
        combined_rating = (movie_rating + actor_rating) / 2
        return -combined_rating, title  # Negative combined_rating for descending sort

    # Sort movies using the helper function
    sorted_movies = sorted(movie_ratings, key=sort_key)

    # Return the top n movies, or all if n is 0
    return [(title, (movie_rating + actor_rating) / 2) for title, movie_rating, actor_rating in
            sorted_movies[:n or None]]


def write_file(top: list, file_name: str):
    """
    Writes a list of movie titles and ratings to a file, each on a new line.

    Parameters:
        top (list): A list of tuples where each tuple\
 contains a movie title (str) and its rating (float).
        file_name (str): The name of the file to write to.

    Each line in the file will contain the title and rating in the format: "Title, rating".

    Example:
    >>> top = [('Dangal', 8.8), ('Bahubali: The Beginning', 8.3), ('Guardians of the Galaxy', 8.1)]
    >>> write_file(top, 'movies.txt')
    >>> with open('movies.txt', 'r') as f:
    ...     f.readlines()
    ['Dangal, 8.8\\n', 'Bahubali: The Beginning, 8.3\\n', 'Guardians of the Galaxy, 8.1\\n']
    """
    with open(file_name, 'w') as f:
        for title, rating in top:
            f.write(f"{title}, {rating}\n")

if __name__ == "__main__":
    import doctest
    print(doctest.testmod())
