databaseName = "youtube.db"

createTable = "CREATE TABLE videos (id INTEGER PRIMARY KEY AUTOINCREMENT, author TEXT, title TEXT, views INTEGER, comments INTEGER, dateDay INTEGER, dateMonth INTEGER, dateYear INTEGER, url TEXT)"
clearTable1 = "DELETE FROM videos"
clearTable2 = "DELETE FROM sqlite_sequence WHERE name='videos'"  # Sqlite has a table for the table above, deleting this resets the autoincrement
returnAllData = "SELECT * FROM videos"

#"INSERT INTO videos (author, title, views, comments, dateDay, dateMonth, dateYear, url) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
