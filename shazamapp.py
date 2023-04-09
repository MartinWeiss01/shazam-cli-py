import os
import sys
import asyncio
from shazamio import Shazam as ShazamIO
import music_tag
import requests
from formattedstring import FormattedString

class ShazamAppTrack:
  def __init__(self, file_path, is_rename, is_preview):
    # Manager properties
    self.file_path = file_path
    self.is_rename = is_rename
    self.is_preview = is_preview
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
    shazam_io = ShazamIO()
    return await shazam_io.recognize_song(self.file_path)
  
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
    path_parts = os.path.split(self.file_path)
    file_extension = os.path.splitext(self.file_path)[1]
    new_file_name_with_extension = file_new_name + file_extension
    new_file_path = os.path.join(path_parts[0], new_file_name_with_extension)
    os.rename(self.file_path, new_file_path)
    self.file_path = new_file_path
    print(f" {FormattedString().INFO}<< file renamed to: {new_file_name_with_extension} >>{FormattedString().END}")

  def __update_id3_tags(self):
    file_handler = music_tag.load_file(self.file_path)
    file_handler['artist'] = self.artist
    file_handler['title'] = self.song
    # Check for album artwork, if available, set it to the file
    response = requests.get(self.imageUrl)
    if response.status_code == 200:
      file_handler['artwork'] = response.content
    file_handler.save()

  def identify_track(self):
    print(f"\r{FormattedString().CYAN}[ShazamApp] Identifying {self.file_path}{FormattedString().END}",
      end='', flush=True
    )
    result = self.__get_track_details()

    if result:
      print(f"\n{FormattedString().SUCCESS}[ShazamApp] Found match for {self.artist} - {self.song}{FormattedString().END}",
        end='' if self.is_rename and self.is_preview is not True else '\n', flush=True
      )

      if self.is_preview is False:
        self.__update_id3_tags()
        if self.is_rename:
          self.__rename_file()
    else:
      print(f"\r{FormattedString().ERROR}[ShazamApp] No match found for {self.file_path}{FormattedString().END}")
