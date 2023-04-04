import os

def identify_file(file_path, rename):
  file_extension = os.path.splitext(file_path)[1]
  print(f"[ShazamApp] Identifying {file_extension} file: {file_path} ")
  if rename:
    print(f"[ShazamApp] Renaming this file...")