import pymongo as pm

import requests

import json

from bson.objectid import ObjectId

import re

import random

CAMPOS_CANCIONES = ('artistId', 'trackName', 'artistName', 'primaryGenreName', 'collectionName', 'trackViewUrl')


def __song_capture(artistName: str):
    response = requests.get('https://itunes.apple.com/search?term=' + artistName)
    json_data = json.loads(response.text)['results']
    lista = []
    for dato in json_data:
        song = {}
        if dato['artistName'] == artistName:
            for campo in CAMPOS_CANCIONES:
                song[campo] = dato[campo]
        lista.append(song)
    print(lista)



def __write_json(new_list):
    with open('canciones_temp.json', 'w', encoding='utf-8') as file:
        datos = (cancion for cancion in new_list if cancion != {})
        json.dump(datos, file, indent=4, ensure_ascii=False)



def __validate_email(email):
    patron = re.compile("^([a-z0-9_.-]+)@([\da-z.-]+).([a-z.]{2,6})$")
    if patron.search(email):  # Comprobemos sí este es un correo electronico valido
        print("Correo valido!")
    else:
        print("Correo Invalido!")


def __connect_db():
    client = pm.MongoClient("mongodb://localhost:27017")
    db = client.MusicPlayList
    return client, db


def __count_collection(col: str):
    client, db = __connect_db()
    collection = db[col]
    value = collection.find().count()
    __close_db(client)
    return value


def __close_db(client):
    client.close()


def error_message(string_error: str):
    error = f'Se ha producido un error: {string_error}'
    return error


def add_user(data: tuple):
    name, surname, username, email = data
    new_user_id = __count_collection('usuario') + 1
    user = {'_id': new_user_id, 'name': name, 'surname': surname, 'username': username, 'email': email}
    client, db = __connect_db()
    users = db.usuario
    users.insert_one(user)
    __close_db(client)


def add_artist(artistName: str):
    lista = __song_capture(artistName)
    __write_json(lista)
    client, db = __connect_db()
    temas = db.canciones
    with open('canciones_temp.json', 'r', encoding='utf-8') as file:
        data_file = json.load(file)
        for insert in data_file:
            temas.insert_one(insert)
    __close_db(client)


def search_infoartist(search_item, grupo):
    query = {}
    client, db = __connect_db()
    temas = db.canciones
    query[search_item] = grupo
    resultados = temas.find(query)
    __close_db(client)
    return resultados


def get_all_songs():
    client, db = __connect_db()
    temas = db.canciones
    lista = list(temas.find())
    __close_db(client)
    return lista


def user_check(user_name: str, e_mail: str) -> bool:
    query = {}
    client, db = __connect_db()
    users = db.usuario
    query['username'] = user_name
    query['email'] = e_mail
    if users.find_one(query):
        __close_db(client)
        return True
    else:
        __close_db(client)
        return False


def insert_playlist(titulo: str, username: str) -> bool:  # insert_playlist     #llamar variable play_list
    client, db = __connect_db()
    play_list = db.playlist
    cursor = play_list.find_one({'titulo': titulo})
    if cursor is None:
        new_playlist = {'titulo': titulo, 'username': username,
                        'canciones': []}
        play_list.insert_one(new_playlist)
        __close_db(client)
        return True
    else:
        return False


def search_song_by_trackName(name_song):
    client, db = __connect_db()
    canciones = db.canciones
    cancion = canciones.find_one({'trackName': name_song})
    __close_db(client)
    return cancion['_id']


def add_song_to_playlist(title, id_cancion):  # aportar el id del playlist en lugar del nombre de usuario
    client, db = __connect_db()  # hacer una __funct para recorrer la conexión
    canciones = db.canciones
    objInstance = ObjectId(id_cancion)
    cancion = canciones.find_one({"_id": objInstance})

    play_list = db.playlist
    playlist_result = play_list.find_one({'titulo': title})
    play_list.update_one({"_id": playlist_result['_id']}, {'$addToSet': {'canciones': cancion}})
    __close_db(client)


def get_playlist_songs(titulo: str) -> list:
    client, db = __connect_db()
    play_list = db.playlist
    mi_playlist = play_list.find_one({'titulo': titulo})  # probar si funciona True
    canciones_seleccionadas = [cancion for cancion in mi_playlist['canciones']]
    __close_db(client)
    return canciones_seleccionadas


def get_songs_by_gen(genero: str)->list:
    client, db = __connect_db()
    canciones = db.canciones
    temas = list(canciones.find({'primaryGenreName': genero}))  # probar si funciona True
    __close_db(client)
    return temas


def add_many_songs(title: str, canciones: list):
    client, db = __connect_db()
    play_list = db.playlist
    for cancion in canciones:
        play_list.update_one({"titulo": title}, {'$addToSet': {'canciones': cancion}})
    __close_db(client)


def remove_song(title, id_cancion):
    client, db = __connect_db()
    play_list = db.playlist
    objInstance = ObjectId(id_cancion)
    play_list.update({'titulo': title}, {'$pull': {'canciones': {'_id': objInstance}}})
    __close_db(client)


def get_random_from_canciones(canciones: list, n: int):
    return random.choices(canciones, k=n)


def get_random_songs(title, n):
    client, db = __connect_db()
    play_list = db.playlist
    todas_canciones = play_list.find_one({'titulo': title})
    titulos_canciones = [(cancion['trackName'], cancion['artistName']) for cancion in todas_canciones['canciones']]
    frecuencia = play_list.aggregate(
        [{'$unwind': {'path': '$canciones'}}, {'$group': {'_id': '$canciones.artistId', 'count': {'$sum': 1}}}])

    frec = {f['_id']: f['count'] for f in frecuencia}
    lista_repeticiones = [frec[cancion['artistId']] for cancion in todas_canciones['canciones']]
    __close_db(client)
    return random.choices(titulos_canciones, weights=lista_repeticiones, k=n)


def get_other_playlist(title, username) -> tuple:
    client, db = __connect_db()
    play_list = db.playlist
    my_playlists = play_list.find({'titulo': {'$ne': title}, 'username': username})
    __close_db(client)
    return tuple(my_playlists)

def get_playlist_titles(username):
    client, db = __connect_db()
    play_list = db.playlist
    my_playlists = play_list.aggregate([{'$match':{'username': username}}, {'$project': {'_id': 0, 'titulo': 1}}])
    my_playlists = [pl['titulo'] for pl in my_playlists]
    __close_db(client)
    return my_playlists
