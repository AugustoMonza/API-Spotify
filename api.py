import requests
import pandas as pd
import json
from decouple import config

#Acceso al Token de la API
def conn():
    url = 'https://accounts.spotify.com/api/token'
    client_id = config('CLIENT_ID')
    client_secret = config('CLIENT_SECRET')
    
    r = requests.post(url, {
                            'grant_type': 'client_credentials',
                            'client_id': client_id,
                            'client_secret': client_secret,
                        } )
    
    r = r.json()
    access_token = r['access_token']
    return access_token

#Extraigo información de la Playlist seleccionada
def playlist(access_token):
    
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    playlist = '37i9dQZF1DX1XBQ1VPYzXt?si=a4e508d4cac14c11'
    base_URL = f'https://api.spotify.com/v1/playlists/{playlist}/tracks'

    resp = requests.get(base_URL , headers= headers)

    resp = resp.json()

    items_access = resp['tracks']['items']
    songs = []
    id = []
    name = []
    #Busqueda de la información dentro del .json
    for track in items_access:
        songs.append(track['track']['name'])
        root_items = track['track']['album']['artists'][0]
        id.append(root_items['id'])
        name.append(root_items['name'])
    
    return id, name, songs 

#En base al artista obtengo el Género
def gener(access_token, id):
    headers = {
    'Authorization': f'Bearer {access_token}'
    }
    genres = []
    for i in id:
        base_URL = f'https://api.spotify.com/v1/artists/{i}'
        resp = requests.get(base_URL , headers= headers)
        resp = resp.json()
        genres.append(resp['genres'])
    
    return genres

#En base a información obtenida genero la tabla del top de canciones
def to_csv(name, songs, genres):
    table = {
        'Artista': name,
        'Canción': songs,
        'Género': genres
    }
    df = pd.DataFrame(table)
    df = df.astype({'Género': 'str'})
    df['Género'] = df['Género'].str.replace('[', '').str.replace(']', '').str.replace("'", '') #Normalizo columna 'Género'
    df.to_csv('Top canciones de Colombia.csv')


def extract():
    access_token = conn()
    id, name, songs = playlist(access_token)
    genres = gener(access_token, id)
    to_csv(name, songs, genres)


if __name__ == '__main__':
    extract()