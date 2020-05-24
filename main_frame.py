from flask import Flask

app = Flask(__name__)
app.config("DEBUG")==True


@app.route('/', methods=['GET'])
def base(): # Base route - "have it return something"
    return '''<p>Welcome to Facebook</p>'''

app.run(port=3000) #address for local server
