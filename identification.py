import os
from shazamapp import ShazamAppTrack
from formattedstring import FormattedString
import errors

ALLOWED_FILE_TYPES = ['.aac', '.aiff', '.dsf', '.flac', '.m4a', '.mp3', '.ogg', '.opus', '.wav', '.wv']

def is_file_type_allowed(file_extension):
  return file_extension in ALLOWED_FILE_TYPES

def identify_file(file_path, is_rename, is_preview, is_strict, discogs_api):
  file_extension = os.path.splitext(file_path)[1]
  if is_file_type_allowed(file_extension):
    try:
      shazamapp = ShazamAppTrack(file_path, is_rename, is_preview, is_strict, discogs_api)
      shazamapp.identify_track()
    except KeyboardInterrupt:
      print(f"\n{FormattedString().WARNING}[ShazamApp] Aborting the program...{FormattedString().END}")
      exit()
    except PermissionError:
      print(f"\r{FormattedString().ERROR}[ShazamApp] Permission denied for file: {file_path} is used by another process{FormattedString().END}")
    except errors.InvalidFileType:
      print(f"\r{FormattedString().ERROR}[ShazamApp] Invalid file {file_path}{FormattedString().END}")
  #else:
  #  print(f"{FormattedString().WARNING}[ShazamApp] Skipping {file_extension} file: {file_path}{FormattedString().END}")

# Browse directory_path and identify all found files (recursively if specified)
def identify_folder_files(directory_path, is_recursive, is_rename, is_preview, is_strict, discogs_api):
    for root, dirs, files in os.walk(directory_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            identify_file(file_path, is_rename, is_preview, is_strict, discogs_api)
        if not is_recursive:
            break
