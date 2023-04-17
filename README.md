# ShazamApp

ShazamApp reads all audio files from the specified folder, attempts to identify them, and if successful, sets the extracted audio file information to metadata. Let ShazamApp automatically organize your entire audio library.

## Installation

You need to have [ffmpeg](https://ffmpeg.org/) and ffprobe installed and added to PATH (Environment Variables)

> If you are using Windows, you can use [build from BtBN](https://github.com/BtbN/FFmpeg-Builds)

> If you are using Linux, you can use [package manager depending on your distribution](https://ffmpeg.org/download.html#build-linux)

You also need to install all the required packages included in requirements.txt

```
$ pip install -r requirements.txt
```

## Usage

The application can be run without arguments, in which case the application only loads files from the folder it is currently in and does not rename files if the song is successfully identified

```
$ python app.py
```

## Options

| Argument name   | Description                                                                                                                                                                                                          |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| --path, -f TEXT | Path to the specific file or folder in which the files will be browsed. If the value is not set manually, the current folder is automatically taken.                                                                 |
| --recursive, -r | Include files from all subfolders for the track identification.                                                                                                                                                      |
| --rename, -n    | If this parameter is set, the file name of each successfully identified song is renamed in the format: ARTIST - SONG.                                                                                                |
| --preview, -p   | If this parameter is set, identification details will be printed on the output, but no changes will be made to the files (rename nor ID3 tags edit).                                                                 |
| --version, -v   | Prints the current version of the ShazamApp.                                                                                                                                                                         |
| --strict, -s    | If this parameter and token are set, ShazamApp will use Discogs API to get more details. If there will be match, then the track duration will be compared. If they are not the same, then the track will be skipped. |
| --token TEXT    | Only needed when using the --strict parameter. Discogs Personal Access Token. You can get it here: https://www.discogs.com/settings/developers                                                                       |
| --help          | Show Usage & Options and exit.                                                                                                                                                                                       |
