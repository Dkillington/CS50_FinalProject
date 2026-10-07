import app
from flask import Flask
 
# Display options and accept user input
print("[1] Scrape a youtube channel")
print("[2] Open website\n")
answer = input()

# Use Webscraper
if(answer == "1"):
    import webScraper
    print("Type channel name here:")
    webScraper.Scrape(input())
    
# Run website
elif(answer == "2"):
    app.runApp()
