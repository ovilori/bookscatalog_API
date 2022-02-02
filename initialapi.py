'''Creating Web APIs with Python and Flask - https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask#understanding-our-database-powered-api
    This file contains the code for an example API - Distant Reading Archive API which is a book catalog.
'''
#imports the flask library and other library
from flask import Flask, request, jsonify

#this creates the flask application object, containing data about the application & also methods that tell the app what to do.
app = Flask(__name__)

#starts the debugger.
app.config['DEBUG'] = True

#creating some test data for the catalog in form of a list of dictionaries.
books = [
    {
        'id': 0,
        'title': 'A Fire Upon the Deep',
        'author': 'Vernor Vinge',
        'first_sentence': 'The coldsleep itself was dreamless.',
        'year_published': '1992'
    },
    {
        'id': 1,
        'title': 'The Ones Who Walk Away From Omelas',
        'author': 'Ursula K. Le Guin',
        'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
        'published': '1973'
    },
    {
        'id': 2,
        'title': 'Dhalgren',
        'author': 'Samuel R. Delany',
        'first_sentence': 'to wound the autumnal city.',
        'published': '1975'
    }
]

#mapping the function 'home' to the path '/' and specifying the type of HTTP request that is allowed.
@app.route('/', methods=['GET'])

#homepage - function containing the result that will be displayed in the browser.
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

#A route to return all of the available entries in the catalog.
@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    return jsonify(books)

#allow users to filter their requests using a unique ID.
@app.route('/api/v1/resources/books', methods=['GET'])
def api_id():
    #check if user provides an ID as part of the URL, and assign it to a variable if provided.
    #displays an error message if no ID is provided.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return 'Error: No id field provided. Please specify an id.'

    #empty list for the results
    results = []

    #loop through the data and match results that fit the specified ID by the user.
    for book in books:
        if book['id'] == id:
            results.append(book)

        #else:
            #message to display if requested id does not exist.
            #return 'No entry for specified id.'
    #convert list of Python dictionaries to the JSON format using the jsonify function.
    return jsonify(results)

#this method runs the application server.
app.run()
