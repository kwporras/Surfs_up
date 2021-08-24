# Import the Flask dependency
from flask import Flask

# Create a New Flash App Instance
app = Flask(__name__)

# Define the starting point, aka the root.
@app.route('/')

# Create a function, aka route
def hello_world():
    return 'Hello world'

