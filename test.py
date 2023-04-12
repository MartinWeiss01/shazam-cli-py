import discogs_client

#esults = d.search('Stockholm By Night', type='release')
# vyhledání shody podle názvů umělce, skladby a alba

d = discogs_client.Client('MyApp', user_token='ZxOYlSZlyJrjGopmaEoHzbwbdayDeqgcnLZaKbkY')

def print_song_info(song):
    results = d.search(song, type='release')
    release = results[0]
    print(release.data.keys())


    track = None

    for t in release.tracklist:
        if t.title == song:
            track = t
            break




    print("Artist: " + release.artists[0].name)
    print("Title(Album): " + release.title)
    print("Label: " + release.labels[0].name)
    print("Release year: " + str(release.year))
    print("Genre: " + str(release.genres))
    print(f"Length: {track.duration}")
    print("Apple Music ID:" + str(release.id))



print_song_info('Zick Zack')








