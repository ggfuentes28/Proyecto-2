from flask import Flask, render_template, request, redirect, url_for

import repositorio as repo

from modelo import Canciones, PlaylistConsole

app = Flask(__name__)

CAMPOS_PLAYLIST = ('_id', 'titulo', 'username', 'canciones')
CAMPOS_USUARIOS = ('_id', 'name', 'surname', 'username', 'email')
CAMPOS_CANCIONES = ('artistId', 'trackName', 'artistName', 'primaryGenreName', 'collectionName', 'trackViewUrl')


@app.route("/inicio")
def inicio():
    return render_template('Inicio.html', titulo='PlayList')


@app.route("/add_user", methods=('GET', 'POST'))
def add_user(): #añade un usuarioa colección usuarios requiriendo nombre username e e-mail
    if request.method.upper() == "GET":
        return render_template('add_user.html', CAMPOS_USUARIOS=CAMPOS_USUARIOS)
    else:  # es post
        datos = request.form.getlist('campos')
        repo.add_user(datos)
        return redirect('/inicio')


@app.route("/add_song", methods=('GET', 'POST'))
def add_artistname(): #busca artista (grupo) y lo añade a coleción canciones
    if request.method.upper() == "GET":
        return render_template('add_artistname.html')
    else:  # es post
        try:
            grupo = request.form['artist']
            canciones = Canciones()
            canciones.add(grupo)
            del canciones
            return redirect('/inicio')
        except:
            message = repo.error_message('    ***** Error de descarga de datos ******')
            return render_template('error_screen.html', error=message)


@app.route("/show_all_songs")
def show_all_songs(): #muestra todas las canciones de la colección canciones
    canciones = Canciones()
    temas = canciones.get_all()
    del canciones
    return render_template('view_all_songs.html', temas=temas, CAMPOS_CANCIONES=CAMPOS_CANCIONES)


@app.route("/add_song_to_playlist/<id>", methods=('GET', 'POST'))
def add_selected_song_to_playlist(id): #desde el html que muestra todas las canciones, trae el id_cancion y lo añade a una play list
    if request.method.upper() == "GET":
        return render_template('add_song_to_playlist.html')
    else:  # es post
        username = request.form['username']
        e_mail = request.form['correo']
        title = request.form['title']
        verification = repo.user_check(username, e_mail)
        if verification is True:
            new_songs = PlaylistConsole(title, '')
            new_songs.add_song(id)
            del new_songs
            return redirect('/show_all_songs')

        else:
            new_songs = PlaylistConsole('', '')
            message = new_songs.__str__()
            del new_songs
            return render_template('error_screen.html', error=message)


@app.route("/see_your_playlist", methods=('GET', 'POST'))
def see_your_playlist():
    if request.method.upper() == "GET":
        return render_template('play_list_check.html')
    else:  # es post
        title = request.form['title']
        username = request.form['username']
        e_mail = request.form['correo']
        verification = repo.user_check(username, e_mail)
        if verification is True:
            myplaylist = PlaylistConsole(title, username)
            results = myplaylist.get_playlist_console()
            del myplaylist
            return render_template('see_playlist_songs.html', results=results, title=title, username=username,
                                   CAMPOS_CANCIONES=CAMPOS_CANCIONES)
        else:
            myplaylist = PlaylistConsole('', '')
            message = myplaylist.__str__()
            del myplaylist
            return render_template('error_screen.html', error=message)


@app.route("/remove_song/<id>/<title>/<username>", methods=('GET', 'POST'))
def remove_song(id, title, username):
    myplaylist = PlaylistConsole(title, username)
    myplaylist.remove_song(id)
    results = myplaylist.get_playlist_songs()
    del myplaylist
    return render_template('see_playlist_songs.html', title=title, results=results, username=username,
                           CAMPOS_CANCIONES=CAMPOS_CANCIONES)


@app.route("/carga_masiva/<title>/<username>", methods=('GET', 'POST'))
def add_many_songs(title, username):
    if request.method.upper() == "GET":
        return render_template('play_list_check_add_many.html')
    else:  # es post
        genero = request.form['genero']
        canciones = Canciones('', '', '', genero)
        listado_canciones = canciones.get_all_gen()
        myplaylist = PlaylistConsole(title, username)
        myplaylist.add_many_songs(listado_canciones)
        results = myplaylist.get_playlist_songs()
        del myplaylist
        del canciones
        return render_template('see_playlist_songs.html', results=results, CAMPOS_CANCIONES=CAMPOS_CANCIONES)

@app.route("/your_other_playlist/<title>/<username>")
def your_other_playlist(title, username):
    myother_playlists = PlaylistConsole(title, username)
    results = myother_playlists.other_playlists()
    del myother_playlists
    return render_template('see_other_playlists.html', results=results)


@app.route("/seleccion_random", methods=('GET', 'POST'))
def select_random():
    if request.method.upper() == "GET":
        return render_template('play_list_check.html')
    else:  # es post
        title = request.form['title']
        username = request.form['username']
        e_mail = request.form['correo']
        verification = repo.user_check(username, e_mail)
        if verification is True:
            myplaylist = PlaylistConsole(title, username)
            results = myplaylist.get_suggestions(20)
            del myplaylist
            return render_template('see_playlist_random_selection.html', results=results, title=title)
        else: # verificacion es False
            myplaylist = PlaylistConsole('', '')
            message = myplaylist.__str__()
            del myplaylist
            return render_template('error_screen.html', error=message)


@app.route("/get_user_id_console", methods=('GET', 'POST'))
def insert_playlist_consola():
    if request.method.upper() == "GET":
        return render_template('user_check.html')
    else:  # es post
        title = request.form['title']
        username = request.form['username']
        e_mail = request.form['correo']
        verification = repo.user_check(username, e_mail)
        if verification is True:  # request.form['username'], request.form['correo']
            canciones = Canciones()
            new_playlist = PlaylistConsole(title, username, canciones.get_all())
            if new_playlist.save() == True:
                selected20 = new_playlist.sugerencias()
                del new_playlist
                del canciones
                return render_template('suggested_songs.html', title=title, username=username, selected=selected20,
                                       CAMPOS_CANCIONES=CAMPOS_CANCIONES)
            else:
                del new_playlist
                del canciones
                return render_template('error_screen.html', error=f' ya existe la colección {title}')
        else:
            new_playlist = PlaylistConsole('', '')
            message = new_playlist.__str__()
            del new_playlist
            return render_template('error_screen.html', error=message)


@app.route("/add_suggested_song/<id>/<title>/<username>")
def add_suggested_song(id: str, title: str, username: str):
    playlist = PlaylistConsole(title, username)
    playlist.add_song(id)
    return redirect('/inicio')
