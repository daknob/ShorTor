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

VERSION = "0.2.1"

#Router
@app.route('/')
def index():
	return render_template("index.html", title=TITLE, version=VERSION)

@app.route('/new', methods=["POST"])
def shortenLink():
	ShortID, PrivKey = shortLink(request)
	FullURI = getFullURL(ShortID, request)
	if(request.headers.get("Accept") and request.headers.get("Accept") == "application/json"):
		return Response('{\n\t"success":"true",\n\t"id":"' + ShortID + '",\n\t"link":"' + FullURI + '",\n\t"private_key": "' + PrivKey + '"\n}', mimetype="text/json")
	return redirect("/v/" + ShortID + "/" + PrivKey)

@app.route('/l/<linkid>')
def redirectToLink(linkid):
	if(not isInCSet(linkid, LINK_ID_CHARSET)):
		return "Invalid Link ID", 400
	A = linkid[0:2]
	B = linkid[2:4]
	MainFile = "links/" + A + "/" + B + "/" + linkid
	if(not os.path.isfile(MainFile)):
		return "No such Link ID", 404
	if(not os.path.isfile(MainFile + ".views")):
		fout = open(MainFile + ".views", "w+")
		fout.write("1")
		fout.close()
	else:
		fin = open(MainFile + ".views", "r")
		views = int(fin.read())
		fin.close()
		views += 1
		fout = open(MainFile + ".views", "w+")
		fout.write(str(views))
		fout.close()
	return redirect(open(MainFile, "r").read())

@app.route('/stats/<linkid>/<privkey>')
def showStats(linkid, privkey):
	if(not isInCSet(linkid, LINK_ID_CHARSET)):
		return "Invalid Link ID", 400
	if(not isInCSet(privkey, LINK_ID_CHARSET)):
		return "Invalid Private Key", 400
	A = linkid[0:2]
	B = linkid[2:4]
	MainFile = "links/" + A + "/" + B + "/" + linkid
	if(not os.path.isfile(MainFile)):
		return "No such Link ID", 404
	try:
		ActPriv = open(MainFile + ".privkey", "r").read()
	except:
		return "Link ID has no Private Key", 400
	if ( not ( ActPriv == privkey ) ):
		return "Invalid Private Key for Link ID", 403
	try:
		Views = open(MainFile + ".views", "r").read()
	except:
		Views = 0
	return render_template("stats.html", title=TITLE, views=Views, version=VERSION)

@app.route('/v/<linkid>/<privkey>')
def viewLinkID(linkid, privkey):
	if(not isInCSet(linkid, LINK_ID_CHARSET)):
		return "Invalid Link ID", 400
	if(not isInCSet(privkey, LINK_ID_CHARSET)):
		return "Invalid Private Key", 400
	return render_template("viewlink.html", title=TITLE, link=(request.url_root + 'l/' + linkid), version = VERSION, uid=linkid, privkey = privkey)

@app.route("/MIT")
def license():
	return Response(open("LICENSE", "r").read(), mimetype="text/plain")

#Extra Functions

# isInCSet ::	This function checks if all of a string's characters
#				belong in a specified character set
def isInCSet(target, cset):
	for char in target:
		if ( char not in cset ):
			return False
	return True

# shortLink ::	This function will shorten a link and return the Link
#				ID, the Private Key, as well as the full URL of the
#				new link.
def shortLink(rq):
	if(not(rq.form['link'])):
		return "Invalid URL", 400
	if(invalidURL(rq.form['link'])):
		return "Invalid URL", 400
	ShortID, LinkPath = getLinkID()
	PrivKey, _ = getLinkID()
	open(LinkPath, "w+").write(rq.form['link'])
	open(LinkPath + ".privkey", "w+").write(PrivKey)
	return ShortID, PrivKey

# getFullURL ::	This function will return the full shortened link URL
#				based on the Link ID and the current request object.
def getFullURL(linkid, rq):
	return rq.url_root + "l/" + linkid

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
