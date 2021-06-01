# Traffic Analysis Site
## Prereqs
1.Make sure you have the necessary dependencies:\
`pip install pandas plotly-express dash`
`pip install python-dotenv`

or use `bash setpy.sh`

2.Put the .env file in the sites/ directory. This file contains the keys for 'GMAPS_KEY' and 'MAPBOX_KEY'

## To run
Open a terminal window and run the index.py file: \
`python index.py`

The webserver will launch and the terminal will say which port it is running on, e.g. http://127.0.0.1:8050/ \
Open your browser and goo to that link

## To add a new screen
1. Create your file in the `screens/` directory.
2. Add `from app import app` as an import.
3. Create a `layout` variable (same thing as `app.layout=`, but just remove the `app.`). Also add `content-screen` to the className in your top-level Div so that we get the right height box.
4. Add your layout to the `index.py` file.
