from platform import java_ver
import sqlite3, os
from sqlite3 import Error


# functions
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        # print(f"Sqlite Version {sqlite3.version}")
        # print("Opened database successfully!")
        print("Connected to database...")
        return conn
    except Error as e:
        print(e)

    return conn



def create_table(conn: sqlite3.Connection, create_table):
    """ Create a table from the create_table param
    :param conn: Connection Object
    :param create_table: an sql CREATE_TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table) 
    except Error as e:
        print(e)


def add_movie(conn: sqlite3.Connection, movie_obj: tuple):
    """ Insert movie in db"""
    sql = """ INSERT INTO movies (movie_title, link)
            VALUES(?,?)"""
    cur = conn.cursor()#(str(movie_title), str(link)
    cur.execute(sql, movie_obj)
    conn.commit()
    return cur.lastrowid


def update_movie(conn: sqlite3.Connection, movie_update: tuple):
    """Update existing movie details"""
    sql = """ UPDATE movies
              SET movie_title = ?,
                  link = ?
              WHERE id = ?"""
    cur = conn.cursor()
    cur.execute(sql, movie_update)
    conn.commit()
    conn.close()


def delete_movie(conn: sqlite3.Connection, movie_id: int):
    """ Delete a movie by movie_id"""
    sql = """ DELETE FROM movies WHERE id=?"""
    # sql = """ DELETE FROM movies WHERE movie_title=?  AND id=?"""
    cur = conn.cursor()
    cur.execute(sql, (movie_id,))
    conn.commit()
    conn.close() # explicitly close the db connection


def show_all_movies(conn: sqlite3.Connection):
    """ Shows all the movie and their links currently in the db."""
    cur = conn.cursor()
    cur.execute("SELECT * FROM movies")
    rows = cur.fetchall()
    # in production
    return rows

def show_movie_by_title(conn: sqlite3.Connection, movie_title: tuple):
    """ Returns the movie matching 'movie_title' """
    cur = conn.cursor()
    cur.execute("SELECT * FROM movies WHERE movie_title LIKE ?", (f"%{movie_title}%",))
    rows = cur.fetchall()
    # in production
    return rows


def main():
    # Movies table 
    movies = """ CREATE TABLE IF NOT EXISTS movies (
                        id integer PRIMARY KEY,
                        movie_title text NOT NULL,
                        link text NOT NULL
    );"""    

    # entry point
    # database = './movies.db' # path to db
    # # if not os.path.exists(database): # only creates a db if path does not exist
    # conn = create_connection(database)
        
    if conn is not None:
        # create table "movies"
        create_table(conn=conn, create_table=movies)
        print("Table was created succesfully!")
    else:
        print("Error! cannot create the database connection.")

    # movie_1 = ('Movie_15', "t.me/lazy_jay")
    # movie_2 = ("Movie_16 🔎", "t.me/Artemokrloov")

    # add_movie(conn, movie_1)

    # update_movie(conn, ("Movie_11", "t.me/Artemokrloov", 2))

    # delete_movie(conn, 10)

    # print(show_movie_by_title(conn, "Movie_16"))
 
    


if __name__ == "__main__":
    main()

    






# 

# conn = sqlite3.connect(PATH)

# # goes inside a function
# print("Opened database successfully")


# conn.execute(""" CREATE TABLE MOVIES
#             (_id INT PRIMARY KEY     NOT NULL,
#             title           TEXT    NOT NULL,
#             link            TEXT    NOT NULL)
# """)
# print("Table created successfully")
# conn.close()

# # goes inside a function
# conn.execute(""" INSERT INTO MOVIES ()

# """)

