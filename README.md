# ShazamApp

ShazamApp reads all audio files from the specified folder, attempts to identify them, and if successful, sets the extracted audio file information to metadata. Let ShazamApp automatically organize your entire audio library.

## Setup

You need to install all the required packages included in requirements.txt

```
$ pip install -r requirements.txt
```

## Run

The application can be run without arguments, in which case the application only loads files from the folder it is currently in and does not rename files if the song is successfully identified

```
$ python shazamapp.py
```

## Options

| Argument name        | Description                                                                                                                                      |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| --path TEXT, -p TEXT | The specific path to the folder in which the files will be browsed. If the value is not set manually, the current folder is automatically taken. |
| --r, -r              | Browse subfolders and check the files in them.                                                                                                   |
| --n, -n              | Rename the files to the extracted metadata.                                                                                                      |
| --help               | Show Usage & Options and exit.                                                                                                                   |
