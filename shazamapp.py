import os
import sys
import asyncio
from shazamio import Shazam as ShazamIO
import music_tag
import requests
from formattedstring import FormattedString
import discogs
from app import VERSION
from datetime import datetime
import errors

INVALID_FILENAME_CHARS = "/\\:*?\"<>|"
MAX_TRACK_LENGTH_SECONGS_DIFFERENCE = 5

class ShazamAppTrack:
  def __init__(self, file_path, is_rename, is_preview, is_strict, discogs_api):
    # Manager properties
    self.file_path = file_path
    self.is_rename = is_rename
    self.is_preview = is_preview
    self.is_strict = is_strict
    self.discogs_api = discogs_api
    # Default tag values
    self.artist = ""
    self.song = ""
    self.isrc = None
    self.genres = []
    self.album = None
    self.label = None
    self.released = None
    self.lyrics = []
    self.apple_music_id = None
    self.imageUrl = None

  # ================== ShazamIO Recognizer ================== #
  async def __async_shazamio_recognizer(self):
    try:
      shazam_io = ShazamIO()
      return await shazam_io.recognize_song(self.file_path)
    except KeyboardInterrupt:
      raise KeyboardInterrupt()
    except:
      raise errors.InvalidFileType()
  
  def __get_track_details(self):
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(self.__async_shazamio_recognizer())
    if("track" in result):
      track = result["track"]

      # Default tag values (some data are wrapped so we have to be careful)
      self.artist = track['subtitle'] if 'subtitle' in track else ""
      self.song = track['title'] if 'title' in track else ""
      self.isrc = track['isrc'] if 'isrc' in track else None
      self.genres = [genre for genre in track['genres'].values()] if 'genres' in track else []

      # Get album artwork URL if available
      if("images" in track):
        if("coverarthq" in track["images"]):
          self.imageUrl = track["images"]["coverarthq"]
        else:
          if("coverart" in track["images"]):
            self.imageUrl = track["images"]["coverart"]

      # Get album, label, release date and lyrics
      if "sections" in track:
        song_section = next((item for item in track['sections'] if item['type'] == 'SONG'), None)
        lyrics_section = next((item for item in track['sections'] if item['type'] == 'LYRICS'), None)

        if song_section is not None and "metadata" in song_section:
          self.album = next((item['text'] for item in song_section['metadata'] if item['title'] == 'Album'), None)
          self.label = next((item['text'] for item in song_section['metadata'] if item['title'] == 'Label'), None)
          self.released = next((item['text'] for item in song_section['metadata'] if item['title'] == 'Released'), None)
        
        if lyrics_section is not None and "text" in lyrics_section:
          self.lyrics = lyrics_section['text']

      # Get Apple Music ID if available
      if "hub" in track and track['hub']['type'] == 'APPLEMUSIC' and 'actions' in track['hub']:
        self.apple_music_id = next((item['id'] for item in track['hub']['actions'] if item['type'] == 'applemusicplay'), None)

      return True
    else:
      return False
  # ================== ShazamIO Recognizer ================== #

  def __rename_file(self):
    file_new_name = self.artist + " - " + self.song

    for char in INVALID_FILENAME_CHARS:
      file_new_name = file_new_name.replace(char, "_")

    file_abs_dir = os.path.split(self.file_path)[0]
    file_extension = os.path.splitext(self.file_path)[1]
    file_new_full_name = file_new_name + file_extension
    file_new_path = os.path.join(file_abs_dir, file_new_full_name)
    #Check if new file path is already in use by different file, if yes, add ("unused") number at the end
    if self.file_path != file_new_path:
      if os.path.exists(file_new_path):
        i = 1
        while os.path.exists(file_new_path):
          file_new_full_name = f"{file_new_name} ({i}){file_extension}"
          file_new_path = os.path.join(file_abs_dir, file_new_full_name)
          i += 1
      os.rename(self.file_path, file_new_path)
      self.file_path = file_new_path

  def __update_id3_tags(self):
    try:
      file_handler = music_tag.load_file(self.file_path)
    except:
      print(f"{FormattedString().WARNING}[warning] {os.path.basename(self.file_path)} doesn't support ID3 tags{FormattedString().END}")
      return

    # Log changes to comment tag
    file_handler.append_tag('comment', f"# ShazamApp {VERSION} Changes, {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    if self.is_rename:
      file_handler.append_tag('comment', f"\n[Rename] {os.path.basename(self.file_path)} -> {self.artist} - {self.song}")
    file_handler['artist'] = self.artist
    file_handler.append_tag('comment', f"\n[Artist] {file_handler['artist']} -> {self.artist}")
    file_handler['title'] = self.song
    file_handler.append_tag('comment', f"\n[Track name] {file_handler['title']} -> {self.song}")

    if self.album is not None:
      file_handler['album'] = self.album
      file_handler.append_tag('comment', f"\n[Album] {file_handler['album']} -> {self.album}")
    if self.released is not None:
      file_handler['year'] = self.released
      file_handler.append_tag('comment', f"\n[Year] {file_handler['year']} -> {self.released}")
    if self.isrc is not None:
      file_handler['isrc'] = self.isrc
      file_handler.append_tag('comment', f"\n[ISRC] {file_handler['isrc']} -> {self.isrc}")

    # In case there are some lyrics, reset the existing ones and add the new ones
    if self.lyrics != []:
      file_handler['lyrics'] = ""
      file_handler.append_tag('comment', "\n[Lyrics] Added")

    for lyrics in self.lyrics:
      file_handler.append_tag('lyrics', "\n" + lyrics)

    file_genres = file_handler['genre'].values
    file_handler.append_tag('comment', f"\n[Genres] Added")

    for genre in self.genres:
      if genre not in file_genres:
        file_handler.append_tag('comment', genre + " ")
        file_handler.append_tag('genre', genre)

    # Check for album artwork, if available, set it to the file
    if self.imageUrl is not None:
      response = requests.get(self.imageUrl)
      if response.status_code == 200:
        try:
          file_handler['artwork'] = response.content
          file_handler.append_tag('comment', f"\n[Album Artwork] Added")
        except:
          self.imageUrl = None

    file_handler.save()

  def is_strict_match(self):
    if(self.is_strict):
      if(self.discogs_api == ""):
        print(f"\n{FormattedString().WARNING}[ShazamApp] Strict mode is enabled and no Discogs API key was provided. Ignoring strict mode...{FormattedString().END}")
        return True
      else:
        discogs_result = discogs.get_track_details(self.song, self.artist, self.released, self.discogs_api)
        if discogs_result is not None and discogs_result['success']:
          #Check if file has option to store ID3 tags, if not, ignore strict mode
          try:
            file_handler = music_tag.load_file(self.file_path)
          except:
            return True
          file_duration = str(file_handler["#length"])
          found_duration = discogs_result['duration']

          if found_duration != "" and file_duration != "":
            #Convert found duration from MIN:SEC to seconds
            found_duration = float(found_duration.split(":")[0]) * 60 + int(found_duration.split(":")[1])
            if abs(found_duration - float(file_duration)) > MAX_TRACK_LENGTH_SECONGS_DIFFERENCE:
              print(f"{FormattedString().WARNING}[ShazamApp] Strict mode is enabled and the track duration is not matching. Skipping track...{FormattedString().END}")
              return False
            else:
              return True
          else:
            return True
        else:
          return True
    else:
      return True

  def print_track_details(self):
    print(f"\r{FormattedString().BOLD}{FormattedString().SUCCESS}[ShazamApp] Found {self.artist} – {self.song}{FormattedString().END} ({self.file_path})")

    print(f"{FormattedString().INFO}[", end = "", flush = True)
    tag_comma = ""

    if self.album is not None:
      print(f"{tag_comma} album: {self.album}", end = "", flush = True)
      tag_comma = ","
    if self.released is not None:
      print(f"{tag_comma} year: {self.released}", end = "", flush = True)
      tag_comma = ","
    if self.isrc is not None:
      print(f"{tag_comma} ISRC: {self.isrc}", end = "", flush = True)
      tag_comma = ","

    if self.genres is not []:
      print(f"{tag_comma} genres: {self.genres}", end = "", flush = True)
      tag_comma = ","
    
    if self.lyrics != []:
      print(f"{tag_comma} with lyrics", end = "", flush = True)
      tag_comma = ","

    print (f" ] {FormattedString().END}")

  def identify_track(self):
    print(f"\r{FormattedString().PURPLE}[ShazamApp] Identifying {self.file_path}{FormattedString().END}",
      end='', flush=True
    )
    result = self.__get_track_details()

    if result:
      if self.is_preview is False:
        if self.is_strict_match():
          self.__update_id3_tags()
          if self.is_rename:
            self.__rename_file()
      self.print_track_details()
    else:
      print(f"\r{FormattedString().ERROR}[ShazamApp] No match found for {self.file_path}{FormattedString().END}")
