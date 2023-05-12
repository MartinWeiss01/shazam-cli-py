import os
from shazamapp import ShazamAppTrack
from formattedstring import FormattedString
import errors
import magic
import shutil
from static_supported_values import ALLOWED_FILE_TYPES, ALLOWED_MIME_TYPES

DEFAULT_TEMPORARY_FILE_NAME = ".0001_shazam"

def is_file_extension_supported(file_extension):
  return file_extension in ALLOWED_FILE_TYPES

def fallback_mime_support(file_path):
  """
    This function is used as a fallback when magic fails to identify the file type because of encoding issues.
    It copies the file to a temporary file and checks MIME type again.
    If it fails again, it checks the file extension.
  """
  file_extension = os.path.splitext(file_path)[1]
  temp_file_path = f"{DEFAULT_TEMPORARY_FILE_NAME}{file_extension}"
  
  shutil.copyfile(file_path, temp_file_path)
  try:
    result = is_mime_supported(temp_file_path, False)
  except:
    pass
  finally:
    if(result is not True):
      result = is_file_extension_supported(file_extension)
    os.remove(temp_file_path)
  return result

def is_mime_supported(file_path, fallback = True):
  try:
    mime = magic.from_file(file_path, mime=True)
    if (mime.startswith("cannot open")):
      raise Error("Magic cannot open file")
    return mime in ALLOWED_MIME_TYPES
  except:
    if(fallback):
      # Try to identify file without encoding issues or by file extension
      return fallback_mime_support(file_path)
    else:
      # Avoid infinite recursion
      return False

def identify_file(file_path, is_rename, is_preview, is_strict, discogs_api):
  if is_mime_supported(file_path):
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

# Browse directory_path and identify all found files (recursively if specified)
def identify_folder_files(directory_path, is_recursive, is_rename, is_preview, is_strict, discogs_api):
  for root, dirs, files in os.walk(directory_path):
    for filename in files:
      file_path = os.path.join(root, filename)
      identify_file(file_path, is_rename, is_preview, is_strict, discogs_api)
    if not is_recursive:
      break
