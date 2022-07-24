from tinydb import TinyDB, Query
import os, re


PATH = './movies.json' # path to db

db = TinyDB(PATH)
Movies = Query() # to query the db



def add_movie(title: str, link: str):
    """Adds movie to the database"""
    title: title
    db.insert({'title': title, 'link': link})

def list_all():
    """List all the movies in the database"""
    return db.all()
    
def get_movie():
    pass

def search_db(title: str):
    """Search the db and retuns the title and link of the movie"""
    match = db.search(Movies.title.search(f'{title}', flags=re.IGNORECASE))
    results = {}
    return match

    # return match

def update_movie_title(old_title: str, *new_title: str):
    searching_stage = db.search(Movies.title in old_title)
    print(searching_stage)
    # return db.update({old_title: new_title}, Movies.title==old_title)

def update_movie_link(old_link: str, *new_link: str):
    pass

def delete_movie(title: str):
    """Deletes the movie that matches the title provided"""
    return db.remove(Movies.title==title)



         
# Driver code
# red = {}
# results = list_all()
# print(results)

# for l in results:
#     # print(l)
#     for x, y in l.items():
#         print(x, y)


# print(search_db("Movie"))
# print(delete_movie("Movie_10"))
# print(search_db(title="Movie_11"))
# print(update_movie_title("Movie_11", "Movie_111"))
# increment by one before adding
# add_movie(title="Movie_10", link="tg_url_to_movie_10")


# >>> # Regex:
# >>> # Full item has to match the regex:
# >>> db.search(User.name.matches('[aZ]*'))
# >>> # Case insensitive search for 'John':
# >>> import re
# >>> db.search(User.name.matches('John', flags=re.IGNORECASE))
# >>> # Any part of the item has to match the regex:
# >>> db.search(User.name.search('b+'))