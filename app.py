import os
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

@app.route("/mylife")
def mylife():
	return render_template('mylife.html')

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)