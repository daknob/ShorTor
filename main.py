#!bin/python
#Imports
from flask import *
from random import randint
import os

#Globals
app = Flask(__name__)
TITLE = "ShorTor"
LINK_ID_LENGTH = 8
LINK_ID_CHARSET = "abcdefghijklmnopqrstuvwxyz1234567890"

VERSION = "0.2"

#Router
@app.route('/')
def index():
	return render_template("index.html", title=TITLE, version=VERSION)

@app.route('/new', methods=["POST"])
def shortenLink():
	if(not(request.form['link'])):
		return "Invalid URL", 400
	if(invalidURL(request.form['link'])):
		return "Invalid URL", 400
	ShortID, LinkPath = getLinkID()
	open(LinkPath, "w+").write(request.form['link'])
	if(request.headers.get("Accept") and request.headers.get("Accept") == "application/json"):
		return Response('{\n\t"success":"true",\n\t"id":"' + ShortID + '",\n\t"link":"' + request.url_root + 'l/' + ShortID + '"\n}', mimetype="text/json")
	return redirect("/v/" + ShortID)

@app.route('/l/<linkid>')
def redirectToLink(linkid):
	for char in linkid:
		if(char not in LINK_ID_CHARSET):
			return "Invalid Link ID", 400
	A = linkid[0:2]
	B = linkid[2:4]
	MainFile = "links/" + A + "/" + B + "/" + linkid
	if(not os.path.isfile(MainFile)):
		return "No such Link ID", 404
	return redirect(open(MainFile, "r").read())

@app.route('/v/<linkid>')
def viewLinkID(linkid):
	for char in linkid:
		if(char not in LINK_ID_CHARSET):
			return "Invalid Link ID", 400
	return render_template("viewlink.html", title=TITLE, link=(request.url_root + 'l/' + linkid), version = VERSION)

@app.route("/MIT")
def license():
	return Response(open("LICENSE", "r").read(), mimetype="text/plain")

#Extra Functions

# invalidURL :: This function will perform some *basic* checks on the
#				provided URL. It will return True if a URL is invalid
#				but if it returns False there is no guarantee this URL
#				is valid. It is a very basic and simple function.
def invalidURL(url):
	if(url[0:4] != "http"):
		return True
	if(url[0:7] != "http://" and url[0:8] != "https://"):
		return True
	if(not("." in url)):
		return True
	if(" " in url):
		return True
	if("\n" in url or "\t" in url):
		return True
	if(len(url) > 4096):
		return True
	return False

# randomID ::	This function will return a randomly generated ID
def randomID():
	rid = ""
	for i in range(0, LINK_ID_LENGTH):
		rid += LINK_ID_CHARSET[randint(0,len(LINK_ID_CHARSET)-1)]
	return rid

# getLinkID ::	This function returns a unique link ID as well as
#				the filesystem path where this link will be saved
def getLinkID():
	ShortID = randomID()
	A = ShortID[0:2]
	B = ShortID[2:4]
	try:
		os.makedirs("links/"+A+"/"+B)
	except:
		pass
	LinkPath = "links/" + A + "/" + B + "/" + ShortID
	if(os.path.isfile(LinkPath)):
		return getLinkID()
	return ShortID, LinkPath

#Execution
if __name__ == '__main__':
	app.run(debug=True, threaded=True)
