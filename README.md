# YouTube Channel Stats

[**Download YouTubeChannelStats.exe**](https://github.com/Dkillington/CS50_FinalProject/releases/latest/download/YouTubeChannelStats.exe)

Save the EXE and double-click it on Windows 10 or 11, 64-bit. It opens the original Flask dashboard in your browser. Python, Flask, SQLite, and offline interface assets are included. No setup, terminal, Python installation, or YouTube account is needed. Close the launcher window to stop the server.

**Includes sample data:** the first launch creates 24 fictional video records in three clearly labeled sample channels. A banner identifies sample data on every page. These are demonstration values, not real YouTube statistics. The original project demonstration remains available below.

Your database lives in `%LOCALAPPDATA%\YouTubeChannelStats\youtube.db`. To view your existing collected data, close the launcher, back up that file, and replace it with your own `youtube.db` using the original `videos` schema. Existing databases are never overwritten or mixed with sample rows. Advanced users can pass `--data-dir "C:\my-data"` to choose another data folder.

## Running or building from source

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-build.txt
.\.venv\Scripts\python.exe launcher.py
.\scripts\Build-Release.ps1 -Python .\.venv\Scripts\python.exe
```

The build produces `dist/YouTubeChannelStats.exe`. Run `launcher.py --self-test --data-dir "C:\temporary-test-data"` to check all dashboard pages, bundled styles, channel queries, and invalid selections. The EXE accepts the same options. The local server binds only to `127.0.0.1` on an available port.

## Optional scraper

The executable is the statistics viewer. The original scraper remains in source for collecting your own data. Install `requirements-scraper.txt`, then run `run.py` and select option 1. It requires Chrome and may need maintenance as YouTube changes. Normal dashboard launch does not import Selenium or start scraping.

## Original CS50 project

YouTube Channel Statistics Website and WebScrape Tool
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



