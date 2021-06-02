import dash
import flask

external_stylesheets = [
    {
        'href': 'http://fonts.googleapis.com/css?family=Open+Sans',
        'rel': 'stylesheet',
        'type': 'text/css',
    }
]

server = flask.Flask(__name__)
app = dash.Dash(__name__, 
                external_stylesheets=external_stylesheets,
                suppress_callback_exceptions=True, 
                server=server)

# to start production server
# gunicorn index:server -b :8000