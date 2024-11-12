"""
Code Generation
"""


def read_file(pathname: str, year: int=0) -> \
    list[list[str, str, str, str, str, str, str, str, str, str, str]]:
    """
    Reads csv file and makes it into lists of lists with movies and info about \
    them which are older then year

    :param pathname: name of file with movies
    :param year: year, that filters movie list\
 takeing only films, which were taken later than 'year'
    :return: lists of lists with movies and info about \
    them which are older then year

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
    with open(pathname, "r", encoding="utf-8") as file:
        file.readline()
        result = [line.strip().split(";") for line in file if int(line.split(";")[6]) >= year]
        return result


def top_n(data: list, genre: str='', n: int=0) -> list[tuple]:
    """

    :param data:
    :param genre:
    :param n:
    :return:

    >>> top_n(read_file('films.csv', 2014), genre='Action', n=5)
    [('Dangal', 8.8),\
 ('Bahubali: The Beginning', 8.3),\
 ('Guardians of the Galaxy', 8.1),\
 ('Mad Max: Fury Road', 8.1),\
 ('Star Wars: Episode VII - The Force Awakens', 8.1)]

    """


    def is_in_genres(film_genres: list, genre: str|list[str]):
        if genre == "":
            return True
        if isinstance(genre, str):
            return genre in film_genres

        for g in genre:
            if g in film_genres:
                return True
        return False

    genre = genre.split(",")
    if len(genre) <= 1:
        genre = "".join(genre)

    answer = []

    # not optimized code

    # for film in data:
    #     film_genre = film[2].split(",")
    #     actors = film[5].split(", ")
    #     if is_in_genres(film_genre, genre):
    #         actor_ratings = []
    #         for actor in actors:
    #             actor_ratings.append(max([float(film2[8]) for film2 in data \
    #                 if actor in film2[5].split(", ")]))
    #         average_actor_rating = sum(actor_ratings) / len(actor_ratings)
    #         answer.append((film[1], float(film[8]), average_actor_rating))

    actors_rating = {}
    for film in data:
        actors = film[5].split(", ")
        rating = float(film[8])
        for actor in actors:
            if actor not in actors_rating:
                actors_rating[actor] = rating
            else:
                actors_rating[actor] = max(actors_rating[actor], rating)

    for film in data:
        film_genre = film[2].split(",")
        actors = film[5].split(", ")
        if is_in_genres(film_genre, genre):
            avg_rating = 0
            for actor in actors:
                avg_rating += actors_rating[actor]
            average_actor_rating = avg_rating/ len(actors)
            answer.append((film[1], float(film[8]), average_actor_rating))

    def sorting_lambda(temp: tuple[str, int, float]) -> tuple[float, str]:
        return (-(temp[1]+temp[2])/2, temp[0])

    answer = sorted(answer, key=sorting_lambda)
    answer = [(film[0], (film[1]+film[2])/2) for film in answer]
    return answer[:n] if n > 0 else answer


def write_file(top: list, file_name: str) -> None:
    """
    Create file and write there a top of films from a rating list.
    :param top (list): rating list of films from previous function
    :param file_name (str): the name of output file
    :return: None
    >>> file = read_file('films.csv', 2014)
    >>> rating = top_n(file, genre='Action', n=5)
    >>> write_file(rating, 'films.txt')
    >>> with open('films.txt', 'r') as file:
    ...     file.readlines()
    ['Dangal, 8.8\\n', 'Bahubali: The Beginning, 8.3\\n', 'Guardians of the Galaxy, 8.1\\n', \
'Mad Max: Fury Road, 8.1\\n', 'Star Wars: Episode VII - The Force Awakens, 8.1\\n']

    """
    with open(file_name, 'w', encoding = 'utf-8') as file:
        for title, rating in top:
            file.write(f'{title}, {rating}\n')


if __name__ == "__main__":
    import doctest
    print(doctest.testmod())
