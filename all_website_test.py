from flask import Flask, render_template

app = Flask(__name__)

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for the login page
@app.route('/login')
def login():
    return render_template('login.html')

# Route for the signup page
@app.route('/signup')
def signup():
    return render_template('signup.html')

# Route for the piyasa page
@app.route('/piyasa')
def piyasa():
    return render_template('piyasa.html')

# Route for the orta page
@app.route('/orta')
def orta():
    return render_template('orta.html')

# Route for the premium page
@app.route('/premium')
def premium():
    return render_template('premium.html')

# Route for the portfoy page
@app.route('/portfoy')
def portfoy():
    return render_template('portfoy.html')

# Route for the yatirim page
@app.route('/yatirim')
def yatirim():
    return render_template('yatirim.html')

# Route for the yuksek page
@app.route('/yuksek')
def yuksek():
    return render_template('yuksek.html')

# Running the app
if __name__ == '__main__':
    app.run(debug=True)
