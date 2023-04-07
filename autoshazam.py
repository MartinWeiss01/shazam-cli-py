import os

# ShazamApp - AutoShazam
import sys
from ShazamAPI import Shazam as ShazamAPI
import asyncio
from shazamio import Shazam as ShazamIO

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
    result['shazamapi'] = self.shazamapi_recognize()
    #ShazamIO
    result['shazamio'] = self.shazamio_recognize()
    return result
# ShazamApp - End

class ColoredInput:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

allowed_file_types = ['.aac', '.aiff', '.dsf', '.flac', '.m4a', '.mp3', '.ogg', '.opus', '.wav', '.wv']

def is_file_type_allowed(file_extension):
  return file_extension in allowed_file_types

def identify_file(file_path, rename):
  file_extension = os.path.splitext(file_path)[1]
  if is_file_type_allowed(file_extension):
    print(f"{ColoredInput().OKGREEN}[ShazamApp] Identifying {file_extension} file: {file_path}{ColoredInput().ENDC}")
    shazam_manager = ShazamManager(file_path)
    result = shazam_manager.recognize_song()
    print(f"{ColoredInput().OKCYAN}[ShazamApp] ShazamApp result: {result}{ColoredInput().ENDC}")
    #if rename:
    #  print(f"{ColoredInput().OKBLUE}[ShazamApp] Renaming this file...{ColoredInput().ENDC}")
  else:
    print(f"{ColoredInput().WARNING}[ShazamApp] Skipping {file_extension} file: {file_path}{ColoredInput().ENDC}")

def identify_folder_files(directory_path, is_recursive, is_rename):
    for root, dirs, files in os.walk(directory_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            identify_file(file_path, is_rename)
        if not is_recursive:
            break
