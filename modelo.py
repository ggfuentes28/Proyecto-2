import repositorio as repo


def enmarcar(textini, textfin): #decorador para enmarcar la salida de la función get_playlist
    def enmarcar_inner(method):
        def inner(*args):
            print(textini)
            #print(f'Listado Playlist {ref.titulo}:')
            method(*args)
            print(textfin)
        return inner
    return enmarcar_inner

class Playlist(object):

    def __init__(self, titulo:str, username:str, canciones=[]):

        self.titulo = titulo
        self.username = username
        self.canciones = canciones

    def save(self): #guarda titulo y username de una nueva Playlist (canciones queda vacío) en base de datos
        self.id = repo.insert_playlist(self.titulo, self.username)
        return self.id

    def search_song(self, trackName): #busca una canción por título desde la Colección canciones. Devuelve el _id.
        return repo.search_song_by_trackName(trackName)

    def add_song(self, id_cancion): #añade la canción dada por _id a la Playlist que esté abierta
        repo.add_song_to_playlist(self.titulo, id_cancion)

    @enmarcar('*'*20, '*'*20)
    def get_playlists(self):  # trae todas las canciones de una Playlist
        return repo.get_playlist_titles(self.username)

    @enmarcar('*'*20, '*'*20)
    def get_playlist_songs(self, string1, string2): #trae todas las canciones de una Playlist
        return repo.get_playlist_songs(self.titulo)

    def add_many_songs(self, canciones): #Añade un listado de canciones (viene de selección previa por género)
        repo.add_many_songs(self.titulo, canciones)

    def remove_song(self, id_cancion): #elimina una canción de una Playlist
        repo.remove_song(self.titulo, id_cancion)

    def get_suggestions(self, n): #Obtiene una lista de canciones de Playlist
        return repo.get_random_songs(self.titulo, n)

    def __str__(self):
        return '***** No coinciden los datos con nungún usuario ******'

    def __del__(self):
        return 1

class Canciones:

    def __init__(self, artistId='', trackName='', artistName='', primaryGenreName=''):
        self.artistId = artistId
        self.trackName = trackName
        self.artistName = artistName
        self.genero = primaryGenreName

    def add(self, artistName): #añade canciones tras búsqueda de artista en itunes
        repo.add_artist(artistName)

    def get_all(self):  #trae el listado de canciones de la colección canciones
        return repo.get_all_songs()

    def get_all_gen(self): #trae todas las canciones de un género (según seleccion por teclado
        return repo.get_songs_by_gen(self.genero)

    def __str__(self):
        return '***** No coinciden los datos con nungún usuario ******'

    def __del__(self):
        return 1


class PlaylistConsole(Playlist): #clase heredada de Playlist para APP (main).

    def __init__(self, titulo, username, canciones=[]):
        Playlist.__init__(self, titulo, username, canciones)

    def get_playlist_console(self): #trae todas las canciones de una Playlist
        return repo.get_playlist_songs(self.titulo)

    def sugerencias(self): #muestra una sugerencia de 20 canciones
        return repo.get_random_from_canciones(self.canciones, 20)

    def other_playlists(self): #Muestra las otras playlist del usuario
        return repo.get_other_playlist(self.titulo, self.username)


