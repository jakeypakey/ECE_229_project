import dash
import flask

server = flask.Flask(__name__)
app = dash.Dash(__name__, suppress_callback_exceptions=True, server=server)

# to start production server
# gunicorn index:server -b :8000