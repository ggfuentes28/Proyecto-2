from modelo import Playlist, Canciones

print(
    'Selecciona opción:\n'
    '(1) Buscar nuevo artista y cargar canciones a Colección Canciones\n'
    '(2) Crear nueva Playlist\n'
    '(3) Cargar Playlist\n'
    '(4) Opciones de Menu Playlist\n'
    '(5) Ver títulos de tus Playlist\n'
    '(6) Fin del programa')

opcion = input('\nIndica la opción (nr) y pulsa enter: ')

while opcion:

    if opcion == '1':  # Buscar nuevo artista y cargar canciones a Colección Canciones
        grupo = input('indica grupo (artista) a buscar')
        canciones = Canciones()
        canciones.add(grupo)
        del canciones

    elif opcion == '2':  # Crear nueva Playlist
        title = input('nombre de la nueva Playlist: ')
        usuario = input('tu nombre de usuario: ')
        playlist = Playlist(title, usuario)
        bool = playlist.save()
        if bool == False:
            print(f'\nError, ya existe la colección {title}')

    elif opcion == '3':  # cargar Playlist
        title = input('nombre de la Playlist: ')
        playlist = Playlist(title, '')

    elif opcion == '4':  # saltar a opciones de Playlist
        break

    elif opcion == '5':  # trae los titulos de las playlist con usuario: username
        usuario = input('tu nombre de usuario: ')
        playlist = Playlist('', usuario)
        playlist.get_playlists('*****************************', '*****************************')

    elif opcion == '6':  # cerrar el programa
        print('**** Fin del Programa ****')
        exit()

    opcion = input('\n\nPulsa 4 para ir a MENU PLAYLIST, otras opciones, elige: ')

print('\n ******   MENU PLAYLIST Indica qué quieres hacer con tu Playlist: *********\n\n'
      '(6) Fin del programa' 
      '(7) Agregar canciones a Playlist por género\n'
      '(8) Recuperar canciones de Playlist\n'
      '(9) Agregar canción a Playlist\n'
      '(10) Obtener 20 sugerencias\n')


opcion = input('\n Indica la opción (nr) y pulsa enter: ')

while opcion != '6':

    if opcion == '7':  # Agregar canciones a Playlist por género
        genero = input('\nIndica genero de canciones: ')
        canciones = Canciones('', '', '', genero)
        listado_canciones = canciones.get_all_gen()
        playlist.add_many_songs(listado_canciones)
        del canciones

    elif opcion == '8':  # Recuperar canciones de Playlist
        playlist.get_playlist_songs('*************************', '*****************************')

    elif opcion == '9':  # Agregar canción a Playlist
        trackName = input('\n\nIndica titulo de la cancion: ')
        song_id = playlist.search_song(trackName)
        playlist.add_song(song_id)

    elif opcion == '10':  # Obtener 20 sugerencias
        print(f'Listado de 20 canciones sugeridas: \n {playlist.get_suggestions(20)}')

    elif opcion == '6':
        del playlist
        exit()

    opcion = input('\nIndica nueva opción (nr) y pulsa enter: ')
