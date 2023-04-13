import discogs_client

d = discogs_client.Client('MyApp', user_token='ZxOYlSZlyJrjGopmaEoHzbwbdayDeqgcnLZaKbkY')

def print_song_info(song, artist):


        results = d.search(song, artist=artist, type='release')


        if(len(results)== 0):
            return {"success": False}
        else:

            release = results[0]

            track = None

            for t in release.tracklist:
                if t.title == song:
                    track = t
                    break

            if release.artists:
                print("Artist(s):", ", ".join([a.name for a in release.artists]))
            else:
                print("Artist(s): N/A ")

            if release.title:
                print("Title: " + release.title)
            else:
                print("Title: N/A ")

            if release.labels:
                print("Label:", release.labels[0].name)
            else:
                print("Label: N/A")

            if release.year:
                print("Release year: " + str(release.year))
            else:
                print("Release year: N/A")

            if release.genres:
                print("Genres:", ", ".join(release.genres))
            else:
                print("Genres: N/A")

            if track is not None and track.duration:
                print("Length:", track.duration)
            else:
                print("Length: N/A")

            return {"success": True}


print_song_info('Wait And Bleed', 'Slipknot')









