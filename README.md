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
$ python shazamapp.py
```

## Options

| Argument name        | Description                                                                                                                                      |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| --path, -p TEXT | The specific path to the folder in which the files will be browsed. If the value is not set manually, the current folder is automatically taken. |
| --r, -r              | Browse subfolders and check the files in them.                                                                                                   |
| --n, -n              | Rename the files to the extracted metadata.                                                                                                      |
| --help               | Show Usage & Options and exit.                                                                                                                   |
