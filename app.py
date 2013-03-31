from flask import Flask, render_template
app = Flask(__name__)
import urllib2
import json

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
    songs = []
    info = []
    data = json.loads(urllib2.urlopen("https://graph.facebook.com/me/music.listens?access_token=AAADWmEJZAo5wBALusrxVLBReZAPYRCsbJifjRrjkKOw8ZBZA4xuaZCB8HuSkxPhbjFYD9xheEM0zA6mRP8ZBJewMfp8V9vTZBsOVOWsH4l5MgZDZD").read())["data"]
    other = json.loads(urllib2.urlopen("https://api.foursquare.com/v2/users/self/checkins?oauth_token=J0A4I2LRHH4CYGRPY545Q2SKIEHKMW3XF5ZUXVR1QURHH4MO").read())["response"]["checkins"]["items"]
    for i in range(5):
        songs.append(data[i])
    for i in range(5):
        info.append(other[i]["venue"])
    #title = json.loads(urllib2.urlopen("https://graph.facebook.com/me/music.listens?access_token=AAADWmEJZAo5wBALusrxVLBReZAPYRCsbJifjRrjkKOw8ZBZA4xuaZCB8HuSkxPhbjFYD9xheEM0zA6mRP8ZBJewMfp8V9vTZBsOVOWsH4l5MgZDZD").read())["data"][0]["data"]["song"]["title"]       #song
    #start_time = json.loads(urllib2.urlopen("https://graph.facebook.com/me/music.listens?access_token=AAADWmEJZAo5wBALusrxVLBReZAPYRCsbJifjRrjkKOw8ZBZA4xuaZCB8HuSkxPhbjFYD9xheEM0zA6mRP8ZBJewMfp8V9vTZBsOVOWsH4l5MgZDZD").read())["data"][0]["start_time"]     #artist
    #end_time = json.loads(urllib2.urlopen("https://graph.facebook.com/me/music.listens?access_token=AAADWmEJZAo5wBALusrxVLBReZAPYRCsbJifjRrjkKOw8ZBZA4xuaZCB8HuSkxPhbjFYD9xheEM0zA6mRP8ZBJewMfp8V9vTZBsOVOWsH4l5MgZDZD").read())["data"][0]["end_time"]     #artist
    #name = json.loads(urllib2.urlopen("https://graph.facebook.com/me/music.listens?access_token=AAADWmEJZAo5wBALusrxVLBReZAPYRCsbJifjRrjkKOw8ZBZA4xuaZCB8HuSkxPhbjFYD9xheEM0zA6mRP8ZBJewMfp8V9vTZBsOVOWsH4l5MgZDZD").read())["data"][0]["from"]["name"]     #artist
    return render_template('mylife.html', data=[songs, info])
@app.route("/porn")
def porn():
	return "Porn!"
@app.route("/location")
def location():
    return "LOCATION LOLLLL"
@app.route("/helperbot")
def helperbot():
    return "helperbot"

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


   