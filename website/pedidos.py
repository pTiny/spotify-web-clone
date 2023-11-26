import os, sys, sqlite3 as sq, hashlib as hs, json as js, random as rn, requests as rq, spotipy as sp, base64 as bs64
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from website.details import creds


def database_check(base, table, username, email, password):
    conn = sq.connect(base)
    cur = conn.cursor()

    try:
        try:
            identity = cur.execute(f"SELECT id FROM {table} WHERE username='{username}'").fetchone()[0]
        except:
            identity = cur.execute(f"SELECT id FROM {table} WHERE email='{email}'").fetchone()[0]

        user_password = cur.execute(f"SELECT password FROM {table} WHERE id={identity}").fetchone()[0]

        if user_password == password:
            conn.commit()
            conn.close()
            return True
        else:
            conn.commit()
            conn.close()
            return False

    except: return False


def search(item):
    def spotify_token():
        auth_string = creds['Spotify']['CLIENT_ID'] + ':' + creds['Spotify']['CLIENT_SECRET']
        auth_bytes = auth_string.encode('utf-8')
        auth_base64 = str(bs64.b64encode(auth_bytes), 'utf-8')

        url = 'https://accounts.spotify.com/api/token'

        headers = {'Authorization': 'Basic ' + auth_base64, 
                'Content-Type': 'application/x-www-form-urlencoded'}
        
        data = {'grant_type': 'client_credentials',
                'scope': 'user-follow-read'}
        
        result = rq.post(url, headers=headers, data=data)

        json_result = js.loads(result.content)

        token = json_result['access_token']
        return token
    
    response = js.loads(rq.get(f"https://api.spotify.com/v1/search?q={item}&type=artist,album,track&limit=15", headers={'Authorization': 'Bearer ' + spotify_token()}).content)
    results = {'artists': {}, 'albums': {}, 'tracks': {}}

    for i in response['tracks']['items']:
        artists = []
        for artist in i['artists']:
            artists.append(f"{artist['name']}")

        authors = ''
        for author in artists:
            authors = f"{authors}, {author}"
        
        results['tracks'][i['name']] = {'type': 'tracks', 'name': i['name'], 'authors': artists, 'authors_str': authors[2:], 'img': i['album']['images'][1]['url']}
    
    for i in response['albums']['items']:
        artists = []
        for artist in i['artists']:
            artists.append(f"{artist['name']}")

        authors = ''
        for author in artists:
            authors = f"{authors}, {author}"

        results['albums'][i['name']] = {'type': 'albums', 'name': i['name'], 'authors': artists, 'authors_str': authors[2:], 'img': i['images'][1]['url']}
    
    for i in response['artists']['items']:
        try:
            results['artists'][i['name']] = {'type': 'artists', 'name': f"{i['name']}", 'authors': [f"{i['name']}"], 'authors_str': i['name'], 'img': i['images'][1]['url']}
        except:
            results['artists'][i['name']] = {'type': 'artists', 'name': f"{i['name']}", 'authors': [f"{i['name']}"], 'authors_str': i['name'], 'img': 'https://i.pinimg.com/736x/83/bc/8b/83bc8b88cf6bc4b4e04d153a418cde62.jpg'}

    return results


def fetch_user(user, base, table):
    conn = sq.connect(base)
    cur = conn.cursor()

    try:
        data = js.loads(cur.execute(f"SELECT user_data FROM {table} WHERE username='{user}'").fetchone()[0])
    except:
        data = js.loads(cur.execute(f"SELECT user_data FROM {table} WHERE email='{user}'").fetchone()[0])

    return data # looks like {'artists': {}, 'albums': {}, 'songs': {}}


def like(item, type, user, base, table):
    conn = sq.connect(base)
    cur = conn.cursor()

    try:
        data = js.loads(cur.execute(f"SELECT user_data FROM {table} WHERE username='{user}'").fetchone()[0])
    except:
        data = js.loads(cur.execute(f"SELECT user_data FROM {table} WHERE email='{user}'").fetchone()[0])

    data[type][item['name']] = item # item is a dict of form {'type': 'artists'/'albums'/'tracks', 'name': str name, 'authors': list artists, 'authors_str': string authers, 'img': str link to image}
    cur = cur.execute(f"UPDATE userdata SET user_data='{js.dumps(data)}'")
    
    conn.commit()
    conn.close()