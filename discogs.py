import discogs_client

def get_track_details(track_name, artist, year, user_token):
    if user_token is None:
        return {"success": False}
    else:
        d = discogs_client.Client('ShazamApp', user_token=user_token)
        results = d.search(track_name, artist=artist, year=year, format='album', type='master')
        if(len(results) == 0):
            return {"success": False}
        else:
            release = results[0]

            track = None
            duration = None
            artists = []
            album = None
            labels = []
            genres = []
            year = None
            position = None

            for t in release.tracklist:
                if t.title.lower() == track_name.lower():
                    track = t
                    break

            if hasattr(track, "artists"):
                artists = [a.name for a in track.artists]

            if hasattr(track, "position"):
                position = track.position
            
            if hasattr(release, "title"):
                album = release.title

                if track is not None:
                    if hasattr(track, "duration"):
                        duration = track.duration

                    if hasattr(track, "title"):
                        track = track.title
                else:
                    track = album
            
            if hasattr(release, "labels"):
                labels = [l.name for l in release.labels]

            if hasattr(release, "year"):
                year = release.year
            
            if hasattr(release, "genres"):
                genres = release.genres
            
            return {"success": True, "duration": duration, "artists": artists, "album": album, "track": track, "labels": labels, "genres": genres, "year": year, "position": position}
