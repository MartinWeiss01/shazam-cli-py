import os
import click
import identification

VERSION = "1.2.0"

currentDirectory = os.getcwd()

@click.command()
@click.option('--path', '-f', default=currentDirectory, help='The specific path to the folder in which the files will be browsed. If the value is not set manually, the current folder is automatically taken.')
@click.option('--recursive', '-r', is_flag=True, help='Include files from all subfolders for the track identification.')
@click.option('--rename', '-n', is_flag=True, help='If this parameter is set, the file name of each successfully identified song is renamed in the format: ARTIST - SONG.')
@click.option('--preview', '-p', is_flag=True, help='If this parameter is set, identification details will be printed on the output, but no changes will be made to the files (rename nor ID3 tags edit).')
@click.option('--version', '-v', is_flag=True, help='Prints the current version of the ShazamApp.')
@click.option('--strict', '-s', is_flag=True, help='If this parameter and token are set, ShazamApp will use Discogs API to get more details. If there will be match, then the track duration will be compared. If they are not the same, then the track will be skipped.')
@click.option('--token', default="", help='Discogs Personal Access Token. You can get it here: https://www.discogs.com/settings/developers')

def main(path, recursive, rename, preview, version, strict, token):
    """ShazamApp reads all audio files from the specified folder, attempts to identify them, and if successful, sets the extracted audio file information to metadata. Let ShazamApp automatically organize your entire audio library."""
    if version:
        click.secho(f"ShazamApp version: {VERSION}", fg='green')
        return
    else:
      path = os.path.abspath(path)
      if os.path.isdir(path) and os.path.exists(path):
        identification.identify_folder_files(path, recursive, rename, preview, strict, token)
      elif os.path.isfile(path) and os.path.exists(path):
        identification.identify_file(path, rename, preview, strict, token)
      else:
        click.secho(f"[ERROR] [ShazamApp] The specified path is not valid – '{path}' was not found.", fg='red')

if __name__ == '__main__':
    main()