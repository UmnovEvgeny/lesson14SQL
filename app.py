import json
import sqlite3

import flask


def get_all_table(sql):
    with sqlite3.connect("netflix.db") as conntention:
        conntention.row_factory = sqlite3.Row
        return conntention.execute(sql).fetchall()


app = flask.Flask(__name__)


@app.route("/movie/<title>")
def search_by_name(title):
    """Поиск по названию"""
    sql = f'''
    SELECT title, country, release_year, listed_in as genre, description
    FROM netflix
    WHERE title = {title}
    ORDER BY date_added DESC
    Limit 1
           '''
    result = None
    for item in get_all_table(sql):
        result = dict(item)
    return flask.jsonify(result)


@app.route("/movie/<int:year1>/to/<int:year2>")
def search_by_year_range(year1, year2):
    """Поиск по диапазону лет выпуска"""
    sql = f'''
    SELECT title, release_year
    FROM netflix
    WHERE release_year BETWEEN {year1} AND {year2}
    ORDER BY release_year
    Limit 100
           '''
    result = []
    for item in get_all_table(sql):
        result.append(dict(item))
    return flask.jsonify(result)


@app.route("/rating/<rating>")
def search_by_rating(rating):
    """Поиск по рейтингу"""
    my_dict = {
        "children": ("G", "G"),
        "family": ("G", "PG", "PG-13"),
        "adult": ("R", "NC-17")
    }
    sql = f'''
    SELECT title, rating, description FROM netflix
    WHERE rating in {my_dict.get(rating, ('ТPG-13', 'NC-17'))}
    Limit 100
           '''
    result = []
    for item in get_all_table(sql):
        result.append(dict(item))
    return flask.jsonify(result)


@app.route("/genre/<genre>")
def search_by_genre(genre):
    """Поиск по жанру"""
    sql = f'''
    SELECT title, description FROM netflix
    WHERE  listed_in LIKE '%{genre}%'
    Limit 100
           '''
    result = []
    for item in get_all_table(sql):
        result.append(dict(item))
    return flask.jsonify(result)


def two_actors(name1, name2):
    sql = f'''
    SELECT "cast" FROM netflix
    WHERE "cast" LIKE '%{name1}%' AND "cast" LIKE '%{name2}%'
           '''
    result = get_all_table(sql)
    main_name = {}
    for item in result:
        names = item.get('cast').split(", ")
        for name in names:
            if name in main_name.keys():
                main_name[name] += 1
            else:
                main_name[name] = 1

    result = []
    for item in main_name:
        if item not in (name1, name2) and main_name[item] > 2:
            result.append(item)
    return result

def step6(types, release_yer, genre):
    sql = f'''
    SELECT * FROM netflix
    WHERE type = '{types}'
    AND release_yer = '{release_yer}'
    AND listed_in LIKE '%{genre}%'
           '''
    return json.dumps(get_all_table(sql), indent=4, ensure_ascii=False)


if __name__ == '__main__':
    app.run()
