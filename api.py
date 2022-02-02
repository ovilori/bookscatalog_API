'''Creating Web APIs with Python and Flask. 
    This file contains the code for an example API - Distant Reading Archive API which is a book catalog.
    Shout out to Patrick Smyth for the tutorial on https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask#understanding-our-database-powered-api
'''
#imports the flask library and other library
from flask import Flask, request, jsonify
import os.path, sqlite3

#this creates the flask application object, containing data about the application & also methods that tell the app what to do.
app = Flask(__name__)

#starts the debugger.
app.config['DEBUG'] = True

#function to return the items from the database as dictionaries rather than as lists.
def dict_factory(cursor, row):
    d = {}
    for index, column in enumerate(cursor.description):
        d[column[0]] = row[index]
    return d

#mapping the function 'home' to the path '/' & specifying the the type of HTTP request that is allowed.
@app.route('/', methods=['GET'])

#homepage function
def home():
    return '''<h1>Distant Reading Archive
                <p>A prototype API for distant reading of science fiction novels.</p>'''

#mapping the function 'api_all' to the path '/api/v1/resources/books/all' to return all the data in the database.
@app.route('/api/v1/resources/books/all', methods=['GET'])

#function to connect to the database and pull return all the data.
def api_all():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, 'books.db')
    db_conn = sqlite3.connect(db_path)
    db_conn.row_factory = dict_factory
    cur = db_conn.cursor()
    all_books = cur.execute('SELECT * FROM books;').fetchall()
    return jsonify(all_books)

#error page to be displayed if the user encounters an error or inputs a route that is undefined.
@app.errorhandler(404)
def page_not_found(e):
    return '''<h1>404</h1>
                <p>The resource could not be found.</p>''', 404

#mapping the function 'api_filter' to the path '/api/v1/resources/books' to allow the user filter data by id, published date, & author.
@app.route('/api/v1/resources/books', methods=['GET'])

#function to connect to the database and return requested data.
def api_filter():

    #grabbing all the query parameters, i.e anything that follows '?' in the URL.
    query_params = request.args

    #retrieving the supported parameters and binding them to variables.
    id = query_params.get('id')
    date_published = query_params.get('published')
    author = query_params.get('author')

    #building the sql query to be used in finding the requested information from the database.
    sql_query = 'SELECT * FROM books WHERE' #defining the query
    to_filter = [] #list to containing the requested parameters (filters)

    #checking if any of id, published date, & author is provided as query parameters, & adding them to the query and filter list.
    if id:
        sql_query += ' id=? AND'
        to_filter.append(id)
    if date_published:
        sql_query += ' published=? AND'
        to_filter.append(date_published)
    if author:
        sql_query += ' author=? AND'
        to_filter.append(author)
    
    #returns the user to the '404 Not Found' page if none of the query parameters is provided.
    if not(id or date_published or author):
        return page_not_found(404)

    #remove the trailing ' AND' and end the sql query with the required ';' symbol.
    sql_query = sql_query[:-4] + ';'
    
    #connect to the database and execute the sql query.
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, 'books.db')
    db_conn = sqlite3.connect(db_path)
    db_conn.row_factory = dict_factory
    cur = db_conn.cursor()
    results = cur.execute(sql_query, to_filter).fetchall()

    #return the result of the sql query in JSON format to the user.
    return jsonify(results)

#run the application server.
app.run()
