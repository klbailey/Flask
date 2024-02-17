from flask import Flask

app = Flask(__name__)

@app.route("/") 
# Home page
def homePage():
    dynamic_html = "<html><head><title>Home Page</title></head><body><h1>Welcome to the Home Page!</h1></body></html>"
    return dynamic_html

# About page
@app.route("/about")
def aboutPage():
    dynamic_html = """
    <html>
        <head><title>About Page</title></head>
        <body>
            <p>We are a non-profit organization working as an animal rescue center.</p>
            <p>We aim to help you connect with purrfect furbaby for you!</p>
            <p>The animals you find at our website are rescue animals which have been rehabilitated.</p>
            <p>Our mission is to promote the ideology of "Adopt, don't Shop"!<p>
            </body></html>"""
    return dynamic_html

if __name__ == "__main__":
    app.run(debug = True, port = 5000)