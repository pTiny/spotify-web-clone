import os, sys, sqlite3 as sq, hashlib as hs, json as js
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class User():
    def __init__(self, username, email, password) -> None:
        self.username = username
        self.email = email
        self.password = password
        self.user_data = {'artists': [], 'albums': [], 'songs': []}

    def add_to_database(self):
        conn = sq.connect("users.db")

        cur = conn.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS userdata(id INTEGER PRIMARY KEY, username VARCHAR(100) NOT NULL, email VARCHAR(250) NOT NULL, password VARCHAR(500) NOT NULL, user_data JSON)")
        cur.execute(f"INSERT INTO userdata VALUES('{self.username}', '{self.email}', '{hs.sha256(self.password.encode()).hexdigest()}', '{js.dumps(self.user_data)}')")
        
        conn.commit()
        conn.close()

class searchItem():
    def __init__(self, name, type, author, image) -> None:
        self.name = name
        self.type = type
        self.author = author # artist = self.name if type is artist
        self.image = image # link to image
        # self.type = type # artist, album, song etc.
        # the rest of the attributes are retrieved from Spotify API
        # add instance of this object to database when user clicks "like" button