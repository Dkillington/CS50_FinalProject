import os
import tools
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from time import strftime
import webScraper

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Jinja function to display a month name after taking in a number (Ex. 12 becomes December)
@app.context_processor
def utility_processor():
    def numToMonth(number):
        dayToMonth = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
        return dayToMonth[number]
    return dict(numToMonth=numToMonth)

# Jinja function to add commas to a number accordingly (Ex. 1000 becomes 1,000)
@app.context_processor
def utility_processor():
    def commaNumber(number):
        return ("{:,}".format(number))
    return dict(commaNumber=commaNumber)


# Connect sqlite database
db = sqlite3.connect(tools.databaseName, check_same_thread=False)
db.row_factory = sqlite3.Row
cursor = db.cursor()

# Enter into Terminal to run Flask:
    # python -m flask run

# --- To Add YouTube Channel: Enter Web Crawl Command HERE! ---
        # (Ex. webScraper.Scrape("ChannelName"))


# Function that takes in sqlite commands and returns a list of dictionaries
def To_List(execution):
    try:
        collection = execution.fetchall()
        returnableDictList = []

        for eachDict in collection:
            returnableDictList.append(dict(eachDict))

        return returnableDictList
    except Exception as err:
        print(err)
        return None

# Returns data for a YouTube Channel
def ReturnChannelInfo(channelName):
    allTables = []

    allTables.append({"tableTitle": "5 Newest Videos", "dictList": To_List(cursor.execute("SELECT title, views, comments, dateMonth, dateDay, dateYear, url FROM videos WHERE author = ? ORDER BY dateYear DESC, dateMonth DESC, dateDay DESC LIMIT 5", (channelName, )))})
    allTables.append({"tableTitle": "5 Oldest Videos", "dictList": To_List(cursor.execute("SELECT title, views, comments, dateMonth, dateDay, dateYear, url FROM videos WHERE author = ? ORDER BY dateYear ASC, dateMonth ASC, dateDay ASC LIMIT 5", (channelName, )))})

    allTables.append({"tableTitle": "5 Most Commented Videos", "dictList": To_List(cursor.execute("SELECT title, views, comments, dateMonth, dateDay, dateYear, url FROM videos WHERE author = ? ORDER BY comments DESC LIMIT 5", (channelName, )))})
    allTables.append({"tableTitle": "5 Least Commented Videos", "dictList": To_List(cursor.execute("SELECT title, views, comments, dateMonth, dateDay, dateYear, url FROM videos WHERE author = ? ORDER BY comments ASC LIMIT 5", (channelName, )))})

    allTables.append({"tableTitle": "5 Most Viewed Videos", "dictList": To_List(cursor.execute("SELECT title, views, comments, dateMonth, dateDay, dateYear, url FROM videos WHERE author = ? ORDER BY views DESC LIMIT 5", (channelName, )))})
    allTables.append({"tableTitle": "5 Least Viewed Videos", "dictList": To_List(cursor.execute("SELECT title, views, comments, dateMonth, dateDay, dateYear, url FROM videos WHERE author = ? ORDER BY views ASC LIMIT 5", (channelName, )))})

    allTables.append({"tableTitle": "Longest Video Title", "dictList": To_List(cursor.execute("SELECT title, views, comments, dateMonth, dateDay, dateYear, url FROM videos WHERE author = ? ORDER BY LENGTH(title) DESC LIMIT 1", (channelName, )))})
    allTables.append({"tableTitle": "Shortest Video Title", "dictList": To_List(cursor.execute("SELECT title, views, comments, dateMonth, dateDay, dateYear, url FROM videos WHERE author = ? ORDER BY LENGTH(title) ASC LIMIT 1", (channelName, )))})

    videoCount = To_List(cursor.execute("SELECT COUNT(*) as SUM FROM videos WHERE author = ?", (channelName, )))[0]["SUM"]
    totalComments = To_List(cursor.execute("SELECT SUM(comments) as SUM FROM videos WHERE author = ?", (channelName, )))[0]["SUM"]
    totalViews = To_List(cursor.execute("SELECT SUM(views) as SUM FROM videos WHERE author = ?", (channelName, )))[0]["SUM"]

    averageComments = To_List(cursor.execute("SELECT ROUND(AVG(comments), 2) as AVE FROM videos WHERE author = ?", (channelName, )))[0]["AVE"]
    averageViews = To_List(cursor.execute("SELECT ROUND(AVG(views), 2) as AVE FROM videos WHERE author = ?", (channelName, )))[0]["AVE"]


    if totalComments < 0:
        totalComments = 0
    if averageComments < 0:
        averageComments = 0

    return channelName, allTables, videoCount, totalComments, totalViews, averageComments, averageViews

# Returns data for a YouTube Channel
def ReturnTotalDatabaseInfo():
    allTables = []

    mostVideoChannels = []

    allTables.append({"tableTitle": "5 Newest Videos", "dictList": To_List(cursor.execute("SELECT author, title, views, comments, dateMonth, dateDay, dateYear, url FROM videos ORDER BY dateYear DESC, dateMonth DESC, dateDay DESC LIMIT 5"))})
    allTables.append({"tableTitle": "5 Oldest Videos", "dictList": To_List(cursor.execute("SELECT author, title, views, comments, dateMonth, dateDay, dateYear, url FROM videos ORDER BY dateYear ASC, dateMonth ASC, dateDay ASC LIMIT 5"))})

    allTables.append({"tableTitle": "5 Most Commented Videos", "dictList": To_List(cursor.execute("SELECT author, title, views, comments, dateMonth, dateDay, dateYear, url FROM videos ORDER BY comments DESC LIMIT 5"))})
    allTables.append({"tableTitle": "5 Least Commented Videos", "dictList": To_List(cursor.execute("SELECT author, title, views, comments, dateMonth, dateDay, dateYear, url FROM videos ORDER BY comments ASC LIMIT 5"))})

    allTables.append({"tableTitle": "5 Most Viewed Videos", "dictList": To_List(cursor.execute("SELECT author, title, views, comments, dateMonth, dateDay, dateYear, url FROM videos ORDER BY views DESC LIMIT 5"))})
    allTables.append({"tableTitle": "5 Least Viewed Videos", "dictList": To_List(cursor.execute("SELECT author, title, views, comments, dateMonth, dateDay, dateYear, url FROM videos ORDER BY views ASC LIMIT 5"))})

    allTables.append({"tableTitle": "Longest Video Title", "dictList": To_List(cursor.execute("SELECT author, title, views, comments, dateMonth, dateDay, dateYear, url FROM videos ORDER BY LENGTH(title) DESC LIMIT 1"))})
    allTables.append({"tableTitle": "Shortest Video Title", "dictList": To_List(cursor.execute("SELECT author, title, views, comments, dateMonth, dateDay, dateYear, url FROM videos ORDER BY LENGTH(title) ASC LIMIT 1"))})

    mostVideoChannels = To_List(cursor.execute("SELECT author, COUNT(*) as SUM FROM videos GROUP BY author ORDER BY COUNT(*) DESC LIMIT 5"))

    videoCount = To_List(cursor.execute("SELECT COUNT(*) as SUM FROM videos"))[0]["SUM"]
    totalComments = To_List(cursor.execute("SELECT SUM(comments) as SUM FROM videos"))[0]["SUM"]
    totalViews = To_List(cursor.execute("SELECT SUM(views) as SUM FROM videos"))[0]["SUM"]

    if totalComments != None:
        if totalComments < 0:
            totalComments = 0
    else:
        totalComments = 0

    return allTables, videoCount, totalComments, totalViews, mostVideoChannels

# Jinja/Flask stuff
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# The main page
@app.route("/")
def index():
    return redirect("/channelInfo")

# Functionality to show statistics of a YouTube channel
@app.route("/databaseInfo", methods=["GET", "POST"])
def askForAllChannels():
    if request.method == "GET":
        # Get all information for channel!
        (allTables, videoCount, totalComments, totalViews, mostVideoChannels) = ReturnTotalDatabaseInfo()
        return render_template("databaseInfoDisplay.html", allTables = allTables, videoCount = videoCount, totalComments = totalComments, totalViews = totalViews, mostVideoChannels = mostVideoChannels)
    else:
        return redirect("/")

# Functionality to show statistics of a YouTube channel
@app.route("/channelInfo", methods=["GET", "POST"])
def askForChannel():
    if request.method == "GET":
        youtubeChannelNames = []
        returnedListDict = To_List(cursor.execute("SELECT DISTINCT author FROM videos"))

        for eachDict in returnedListDict:
            youtubeChannelNames.append(eachDict["author"])

        return render_template("channelInfo.html", inputChannelNames = youtubeChannelNames)

    else:
        if not request.form.get("channelAuthor"):
            print("ERROR!")
            return redirect("/")
        else:
            # Get all information for channel!
            (channelName, allTables, videoCount, totalComments, totalViews, averageComments, averageViews) = ReturnChannelInfo(request.form.get("channelAuthor"))

            return render_template("channelInfoDisplay.html", channelName = str.capitalize(channelName), allTables = allTables, videoCount = videoCount, totalComments = totalComments, totalViews = totalViews, averageComments = averageComments, averageViews = averageViews)


# Functionality to show statistics of a YouTube channel
@app.route("/about", methods=["GET", "POST"])
def about():
    return render_template("channelInfoDisplay.html")