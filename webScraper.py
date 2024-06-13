import sqlite3 # Allow for database management in SQL
import concurrent.futures # Allow for threading (Grabbing multiple pages at once)
import requests
from selenium import webdriver # Import driver functionality used to scrape webpages
from selenium.webdriver.chrome.options import Options # Allows for creating custom options in chrome for each driver used
from selenium.webdriver.common.by import By # Allows for quickly grabbing HTML, CSS data using 'By'
from selenium.webdriver.common.action_chains import ActionChains # Allows executing JavaScript scripts through the driver in Python
from selenium.webdriver.common.keys import Keys # Allows executing key strokes through the driver in Python
# Allow waiting functionality on websites that take a while to load
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Custom variables I use across multiple files (For ease of access)
import tools

# For setting timers
import time

# Create custom options to use for every driver
customOptions = Options()
customOptions.add_argument("--headless=new") # Headless keeps it in the background
customOptions.add_argument("--mute-audio") # Mute will mute any audio when opening youtube videos
customOptions.add_argument("--incognito") # Do in incognito mode
customOptions.add_argument('--ignore-certificate-errors')
customOptions.add_argument('--ignore-ssl-errors')
customOptions.add_argument('--window-size=1920,1080')

# Import Sqlite3 and connect it to the database
db = sqlite3.connect(tools.databaseName)
db.row_factory = sqlite3.Row
cursor = db.cursor()


def Scrape(given_YouTubeChannelName):

    # Create driver using Chrome
    driver = webdriver.Chrome(options = customOptions)

    # Check if SQL table exists and create one if it doesnt
    def CreateSQLTable():
        try:
            cursor.execute(tools.returnAllData)
        except Exception:
            cursor.execute(tools.createTable)

    def MakeChannelNameValid(channelName):
        # Ensure given channel name is a string and is properly formatted
        return "@" + str(channelName)


    def ReturnValidYoutubeURL(urlEnding):
        # Return a complete YouTube URL with the given URL attached to the end
            # This is good for entering a channel name and minimizes URL mispelling
            # Example: Entering "@cs50/videos" returns "https://www.youtube.com/@cs50/videos", a working URL

        return 'https://www.youtube.com/' + str(urlEnding)

    def Return_VideoLinks(urlEnding):
        def PopulateScreen():
        # Loop forever...
            while(True):
            # Try to grab the area on YouTube that causes the page to load more videos (Goal is to have every channel video on the screen)
                try:
                    ActionChains(driver).move_to_element(WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "ytd-continuation-item-renderer")))).perform()
                except Exception:
                    # If unable to get this area, assume page can no longer be loaded (Page completely full) and break
                    break
        

        # Go to YouTube channel's 'Video' page
        driver.get(ReturnValidYoutubeURL(urlEnding))

        # Make sure screen is full of videos
        PopulateScreen()

        # Grab every video element
        allVideos = driver.find_elements(By.TAG_NAME, "ytd-rich-item-renderer")

        # Store the URL links of every video element
        links = []
        for eachVideo in allVideos:
            links.append(eachVideo.find_element(By.ID, "thumbnail").find_element(By.ID, "thumbnail").get_attribute('href'))

        # Provide a console message of how many links grabbed
        count = len(links)
        if count > 0:
            print(str(count) + " YouTube Video URLs grabbed!")
        else:
            print("Unable to grab any video URLs!")

        # Return all video links
        return links


    def CleanseList(inputDictionaryList):
        # Empty list of removed URLs
        removedLinks = []
        # Empty list of satisfactory dictionaries
        newDictionaryList = []

        # Begin test
        if inputDictionaryList != None:
            for currentDictionary in inputDictionaryList:
                keepDict = True
                for value in currentDictionary.values():
                        if value == None:
                            keepDict = False

                # If current dictionary passes the test keep it, or else add the url to the removed links
                if keepDict:
                    newDictionaryList.append(currentDictionary)
                else:
                    removedLinks.append(currentDictionary["url"])

        return newDictionaryList, removedLinks

    def GrabData(videoLinks):
        def Async_Return_VideoData(youTubeChannelName, givenYoutubeLinks, max_amount_of_threads = 10):
            def Return_VideoData(currentVideoURL):
                def OpenExpandableWindow():
                    # XPath to the clickable button
                    botton_XPath = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[4]/div[1]/div/ytd-text-inline-expander/tp-yt-paper-button[1]"
                    try:
                        # Wait for clickable button to show up, and click it if able
                        wait = WebDriverWait(newDriver, 5).until(EC.presence_of_element_located((By.XPATH, botton_XPath))).click()
                        return True
                    except Exception as timeout:
                        print("TIMEOUT ERROR: Waited too long for expandable window to appear in [" + str(currentVideoURL) + "]")
                        return False

                def ReturnTextFromPage(textDescript, given_XPath, timeout = 3):
                    returnedText = None # Set the text to return default to None
                    try:
                        # Try to wait for the XPATH to show up, and grab the text at that location
                        returnedText = WebDriverWait(newDriver, timeout).until(EC.presence_of_element_located((By.XPATH, given_XPath))).text
                    except Exception:
                        if textDescript != "comment disabled":
                            try:
                                for times in range(15):
                                    try:
                                        ActionChains(newDriver).send_keys(Keys.PAGE_DOWN).perform()
                                        returnedText = WebDriverWait(newDriver, 1).until(EC.presence_of_element_located((By.XPATH, given_XPath))).text
                                    except Exception as e:
                                        print("Searching... (" + str(times) + "/15)")
                                if returnedText == None:
                                    print("TIMEOUT ERROR: Couldn't find '" + textDescript + "' in [" + str(currentVideoURL) + "]")
                            except Exception as er:
                                print("TIMEOUT ERROR: Couldn't find '" + textDescript + "' in [" + str(currentVideoURL) + "]")
                    return returnedText

                # Create a brand new driver everytime this function is called, using custom options above ^
                newDriver = webdriver.Chrome(options = customOptions)

                # Create all variables and set to None
                title = None
                views = None
                commentCount = None
                dateDay = None
                dateMonth = None
                dateYear = None

                # Assign URL to driver
                newDriver.get(currentVideoURL)
                # Only continue if the expandable window below a video can be opened (Where data is)
                if(OpenExpandableWindow()):
                    # These are the precise XPaths to each element of a YouTube video, assuming Driver is on the video's own page
                    title_XPath = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[1]/h1/yt-formatted-string"
                    views_XPath = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[4]/div[1]/div/ytd-watch-info-text/div/yt-formatted-string/span[1]"
                    commentTurnedOff_XPath = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-comments/ytd-item-section-renderer/div[3]/ytd-message-renderer/yt-formatted-string[1]/span"
                    commentCount_XPath = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-comments/ytd-item-section-renderer/div[1]/ytd-comments-header-renderer/div[1]/h2/yt-formatted-string/span[1]"

                    commentCount_XPath = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-comments/ytd-item-section-renderer/div[1]/ytd-comments-header-renderer/div[1]/div[1]/h2/yt-formatted-string/span[1]"

                    date_XPath = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[4]/div[1]/div/ytd-watch-info-text/div/yt-formatted-string/span[3]"

                    # Grab each specific text element
                    title = ReturnTextFromPage("video title", title_XPath) # Return video title
                    print(title)
                    views = ReturnTextFromPage("view count", views_XPath) # Return video views
                    views = views.split()[0].replace(",", "") if views != None else None # If views were found, grab only the number
                    print(views)
                    commentsDisabled = ReturnTextFromPage("comment disabled", commentTurnedOff_XPath, 2) # Check to see if a 'Comments Disabled' bar exists on the video
                    # If a 'Comment Disabled' section can't be found, assume comments exist and count them
                    if commentsDisabled == None:
                        commentCount = ReturnTextFromPage("number of comments", commentCount_XPath)
                        if commentCount != None:
                            commentCount = commentCount.replace(",", "")
                    # Else, note that comments werent allowed
                    else:
                        commentCount = "-1"
                    print(commentCount)
                    date = ReturnTextFromPage("date", date_XPath) # Return the date of the video
                    # Split up date accordingly if the date above returns a value, or else assign each value to 'None'
                    if date != None:
                        dateSplit = date.split()

                        # Sometimes instead of "Aug 21, 2000" format, we get "Premiered Aug 21, 2000". So, if the length of the first string is not 3 (Not a month), we shift all indexes right 1
                        adder = 0
                        if len(dateSplit[0]) != 3:
                            adder = 1

                        dateMonth = dateSplit[0  + adder].strip(",")
                        dateDay = dateSplit[1 + adder].strip(",")
                        dateYear = dateSplit[2 + adder]
                    print(date)
                # Create a dictionary for all video data
                videoData = {"author": youTubeChannelName, "title": title, "views": views, "comments": commentCount, "dateDay": dateDay, "dateMonth": dateMonth, "dateYear": dateYear, "url": currentVideoURL}
                # End current driver
                newDriver.quit()
                # Return the dictionary data
                return videoData

            # -------------- Async Process ------------------
            # Create empty list to be used at the end
            finalList = []

            # Create empty list of 'futures' object
            futures = []


            with concurrent.futures.ThreadPoolExecutor(max_workers = max_amount_of_threads) as executor:
                for eachLink in givenYoutubeLinks:
                    futures.append(executor.submit(Return_VideoData, currentVideoURL=eachLink))

            # Adds every result to the final list
            for future in concurrent.futures.as_completed(futures):
                try:
                    finalList.append(future.result())
                except Exception as er:
                    print("Couldn't append Future result to list.")

            # Returns that list
            return finalList

        grabbingChannelData = True
        while(grabbingChannelData):
            max_loops = 10
            # Continue only if there are video links...
            if len(videoLinks) > 0:
                # Send the list to 'ReturnEachLinksData', allowing the function to scrape information off each video using it's URL link
                    # ('ReturnEachLinksData' uses threading, allowing multiple scrapes to happen at once!)
                # 'CleanseList' removes any dictionaries that shouldnt be collected (Null values etc...), and returns a number of deleted (Cleansed) dictionaries
                # Finally, store the dictionaries of each video's data into a list
                videoData, removedLinks = CleanseList(Async_Return_VideoData(given_YouTubeChannelName, videoLinks, 12))

                # Add good video data to main list
                for vidDicts in videoData:
                    allVideoDataList.append(vidDicts)

                # Get the total of removed links
                removedLinksCount = len(removedLinks)

                # If there are removed links, go and fetch them using their URLs.
                if(removedLinksCount == 0):
                    grabbingChannelData = False
                else:
                    if max_loops > 0:
                        print("\n" + str(len(videoData)) + " dictionaries grabbed! " + str(removedLinksCount) + " dictionaries cleansed from list, processing remainders...")
                        videoLinks = removedLinks
                        max_loops -= 1
                    else:
                        print("\n" + str(len(videoData)) + " dictionaries grabbed! " + str(removedLinksCount) + " dictionaries cleansed from list")
                        print("Maximum tries exceeded, exiting...")
                        grabbingChannelData = False

            else:
                print("There were no video links to use!")
                grabbingChannelData = False

    def PopulateDatabase(listOfDictionaries):
        # What the SQL table looks like:
        # -- CREATE TABLE videos (id INTEGER PRIMARY KEY AUTOINCREMENT, author TEXT, title TEXT, views INTEGER, comments INTEGER, dateDay INTEGER, dateMonth INTEGER, dateYear INTEGER, url TEXT)

        # Create month name-number equivalent
        months = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6, "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12}

        # Start count of populated entries at 0
        populatedNum = 0

        # Try to add each dictionary into the database
        for eachDict in listOfDictionaries:
            try:
                cursor.execute("INSERT INTO videos (author, title, views, comments, dateDay, dateMonth, dateYear, url) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (eachDict["author"], eachDict["title"], int(eachDict["views"]), int(eachDict["comments"]), int(eachDict["dateDay"]), int(months[eachDict["dateMonth"].lower()]), int(eachDict["dateYear"]), eachDict["url"]))
                db.commit()
                populatedNum += 1
            except Exception as errrr:
                print(str(errrr) + "\nFile could not be entered into the database...")

        print(str(populatedNum) + "/" + str(len(listOfDictionaries)) + " dictionaries entered into database!")

    CreateSQLTable()

    # All collected video URL links will be stored here
    videoLinks = []

    # All dictionaries of data will be stored here
    allVideoDataList = []

    startSecs = time.time()

    # Creates a valid name to put in URL bar: AKA cs50 = @cs50
    channelName = MakeChannelNameValid(given_YouTubeChannelName)

    # Check that channelName returns a 200 code (Channel is valid)
    if requests.get(ReturnValidYoutubeURL(channelName)).status_code != 200:
        print("This YouTube Channel Doesn't Exist!")
    else:
        # Print to console that the youtube channel was found
        print("'" + channelName + "' found!")

        # Grab all video URLs for a YouTube Channel and store in a list
        videoLinks = Return_VideoLinks(channelName + "/videos")

    # End driver
    driver.quit()

    # Record time
    endSecs = time.time()
    print("\n[URLs Grabbed: " + str(round((endSecs - startSecs), 2)) + " seconds]")

    startSecs = time.time()

    # Main function that scrapes information from YouTube using their youtube urls
    GrabData(videoLinks)

    # Populate the database with information through SQL
    PopulateDatabase(allVideoDataList)

    endSecs = time.time()
    print("\n[Video Data Grabbed/Processed: " + str(round((endSecs - startSecs), 2)) + " seconds]")