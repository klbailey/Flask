from flask import Flask

# Create a Flask object (WSGI application)
app = Flask(__name__)

# Assign URL route
@app.route("/")

# Create a view function
def hello_world():
    return '''
        <p>Kathy</p>
        <p>Bailey Hines</p>
        <p>Seafood</p>
        <p>Any ocean with good surf</p>
        '''

# Run the application in main
if __name__  == '__main__':
   app.run(debug = True, port = 5000)
