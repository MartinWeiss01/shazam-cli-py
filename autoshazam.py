import os

def identify_file(file_path, rename):
  file_extension = os.path.splitext(file_path)[1]
  print(f"[ShazamApp] Identifying {file_extension} file: {file_path} ")
  if rename:
    print(f"[ShazamApp] Renaming this file...")


def identify_folder_files(directory_path, is_recursive, is_rename):
    for root, dirs, files in os.walk(directory_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            identify_file(file_path,is_rename)
        if not is_recursive:
            break
