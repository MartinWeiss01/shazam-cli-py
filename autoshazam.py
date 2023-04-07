import os
import sys
from ShazamAPI import Shazam as ShazamAPI
import asyncio
from shazamio import Shazam as ShazamIO
import music_tag

class FormattedString():
  SUCCESS = '\033[92m'
  WARNING = '\033[93m'
  ERROR = '\033[91m'
  INFO = '\033[94m'
  CYAN = '\033[96m'
  PURPLE = '\033[95m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'
  END = '\033[0m'

# ShazamApp - AutoShazam
class ShazamManager:
  def __init__(self, file_path):
    self.file_path = file_path

  ### ShazamIO Recognizer =========================
  async def async_shazamio_recognizer(self):
    shazam_io = ShazamIO()
    return await shazam_io.recognize_song(self.file_path)
  
  def shazamio_recognize(self):
    loop = asyncio.get_event_loop()
    shazamio_result = loop.run_until_complete(self.async_shazamio_recognizer())
    if("track" in shazamio_result):
      return {"success": True, "author": shazamio_result["track"]["subtitle"], "song": shazamio_result["track"]["title"]}
    else:
      return {"success": False}
  ### ShazamIO Recognizer =========================
  
  ### ShazamAPI Recognizer =========================
  def shazamapi_recognize(self):
    file_handler = open(self.file_path, 'rb').read()
    shazam_api = ShazamAPI(file_handler)
    recognize_generator = shazam_api.recognizeSong()
    matched = next(recognize_generator)[1]
    if("track" in matched):
      return {"success": True, "author": matched["track"]["subtitle"], "song": matched["track"]["title"]}
    else:
      return {"success": False}
  ### ShazamAPI Recognizer =========================

  def recognize_song(self):
    result = {}
    #ShazamAPI 
    #result['shazamapi'] = self.shazamapi_recognize()
    #ShazamIO
    result['shazamio'] = self.shazamio_recognize()

    fetched_tags = result['shazamio']
    if fetched_tags['success']:
      file_handler = music_tag.load_file(self.file_path)
      file_handler['artist'] = fetched_tags['author']
      file_handler['title'] = fetched_tags['song']
      file_handler.save()
    return result['shazamio']
# ShazamApp - End

allowed_file_types = ['.aac', '.aiff', '.dsf', '.flac', '.m4a', '.mp3', '.ogg', '.opus', '.wav', '.wv']

def is_file_type_allowed(file_extension):
  return file_extension in allowed_file_types

def rename_file(file_abs_path, file_new_name):
  path_parts = os.path.split(file_abs_path)
  file_extension = os.path.splitext(file_abs_path)[1]
  new_file_name_with_extension = file_new_name + file_extension
  new_file_path = os.path.join(path_parts[0], new_file_name_with_extension)
  os.rename(file_abs_path, new_file_path)
  print(f"{FormattedString().INFO}<< file renamed to: {new_file_name_with_extension}>>{FormattedString().END}")

def identify_file(file_path, rename):
  file_extension = os.path.splitext(file_path)[1]
  if is_file_type_allowed(file_extension):
    print(f"\r{FormattedString().CYAN}[ShazamApp] Identifying {file_path}{FormattedString().END}", end='', flush=True)
    shazam_manager = ShazamManager(file_path)
    result = shazam_manager.recognize_song()
    if result['success']:
      print(f"\n{FormattedString().SUCCESS}[ShazamApp] Found match for {result['author']} - {result['song']} {FormattedString().END}", end='' if rename else '\n', flush=True)

      if rename:
        file_new_name = result['author'] + " - " + result['song']
        rename_file(file_path, file_new_name)
    else:
      print(f"\r{FormattedString().ERROR}[ShazamApp] No match found for {file_path}{FormattedString().END}")
  else:
    print(f"{FormattedString().WARNING}[ShazamApp] Skipping {file_extension} file: {file_path}{FormattedString().END}")

def identify_folder_files(directory_path, is_recursive, is_rename):
    for root, dirs, files in os.walk(directory_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            identify_file(file_path, is_rename)
        if not is_recursive:
            break
