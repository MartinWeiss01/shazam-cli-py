import os
import click
import autoshazam

currentDirectory = os.getcwd()

@click.command()
@click.option('--path', '-p', default=currentDirectory, help='The specific path to the folder in which the files will be browsed. If the value is not set manually, the current folder is automatically taken.')
@click.option('--r', '-r', is_flag=True, help='Browse subfolders and check the files in them.')
@click.option('--n', '-n', is_flag=True, help='Rename the files to the extracted metadata.')
def main(path, r, n):
    """ShazamApp reads all audio files from the specified folder, attempts to identify them, and if successful, sets the extracted audio file information to metadata. Let ShazamApp automatically organize your entire audio library."""
    path = os.path.abspath(path)
    if os.path.isdir(path):
      click.echo(f"Path: {path}")
      click.echo(f"Include subfolders: {r}")
      click.echo(f"Rename successfully identified files: {n}")
    else:
      click.secho(f"[!] Path is not valid, folder '{path}' was not found.", fg='red')


if __name__ == '__main__':
    main()