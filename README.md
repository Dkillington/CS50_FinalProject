cmd# YouTube Channel Statistics Website and WebScrape Tool
#### Video Demo:  https://youtu.be/VyfFdgA0z2Q?si=FyU1h7_sBEkRvgYK
#### Description:

I created a website that displays statistics on any YouTube channel within the 'youtube.db' database.
Channels are entered into the database using a WebScrape tool I created in 'webScraper.py'. Each step is described in detail below:


1. The YouTube WebScraper (webScraper.py) [Languages Used: Python, Sqlite3]
- The YouTube WebScraper I built is designed to go to a given YouTube channel and return data from that channel quickly and store it into a database.

To ensure the process is legal, I only grabbed information that was public and displayed on the front-end of YouTube. This was also done as a 'guest', so no collected information would have required an account to access. I am also using this data for informative and demonstrational purposes, NOT financial gain.
To make this process faster, I used a program called 'Selenium', which allows a user to run a browser autonomously in the background.
While Selenium is used mainly for website testing, I used it for this project to open a browser, visit YouTube, and return data from HTML text fields such as a video's URL, comments, views, etc, all in the Python language.

There are 5 essential steps in this process:
    1st. A YouTube channel name is entered and validated to be real and visitable
    2nd. Selenium visits the YouTube channel's 'videos' page and collects all video URL links
        - It scrolls the screen until the screen is completely filled with videos, ensuring all channel video links are gathered
    3rd. For every youtube video URL, a Selenium 'webdriver' (a browser window) is created and sent to that URL to fetch data (This is limited to around 10 webdrivers at a time to limit CPU usage)
        - This is done as an Async process which greatly speeds up the time of collecting data, but at the expense of using more memory
        - The python code I wrote in this program specifically tells Selenium how to navigate the website, and how to collect what data
    4th. While the process is faster than searching yourself, it isn't perfect, and sometimes data is not found/returned correctly because time-outs, server issues, etc.
        - A 'Cleanse' function is used here to remove any failed entries from the dictionary
        - For those removed entries, the URLs are grabbed and resent to the Data Collection function, ensuring that EVENTUALLY we will have a complete list of all video data.
    5th. The completed list is entered into the 'youtube.db' database using sqlite

2.  Statistics Website (App.py, 'templates' folder) [ Languages Used: HTML, CSS, Python, Sqlite3, Flask, Jinja2]
- The website allows for selecting a youtube channel from a dropdown list and seeing statistics about the page, such as "Oldest videos, longest titles, average likes per video" etc.

    1st. A YouTube Channel name is selected from a dropdown list
    2nd. Sqlite runs various prewritten commands that grab specific information from from the channel in the form of dictionaries. These dictionaries are put into lists.
    3rd. Those lists are sent to an HTML page using Jinja, and the viewer is able to read the statistics

    (There is also a 'View Database' page, which does this process but for all channels at once)

- Selenium Web Driver: https://selenium-python.readthedocs.io/installation.html#introduction



How To Use:
1. Download all files from github as a ZIP
2. Extract all files into a single folder
3. Open this folder into a code editor (Visual Studio Code)
4. Open a terminal window and do the following:
    1. Pip install necessary files (Write the following lines in the terminal)
        - pip install selenium
        - pip install Flask-Session
        - pip install -U Flask
    2. Create a virtual environment (CTRL + SHIFT + P)

5. Run run.py
   - View terminal window
        1. Press 1 to scrape YouTube channel data
            - Type channel name and wait for it to finish
        2. Press 2 to launch website
            - Click the "Running on http://__________" link that appears in the terminal to view the site
            - Press Ctrl+C to end
