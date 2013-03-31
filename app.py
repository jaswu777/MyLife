from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello Universe!"

@app.route("/hackru")
def hackru():
    return "Hello HackRU!"

@app.route("/sample")
def sample():
	return render_template('sample.html', my_variable='Variable substitution worked')

if __name__ == "__main__":
    app.run()