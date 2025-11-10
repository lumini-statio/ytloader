# YTLOADER

CLI to download playlists and songs individualy with mp3 extension.

> [!NOTE]
> You can change the script to adapt the python version, dependencies or the program to your machine.

> [!WARNING]
> If you abuse of this tool, yt may block your computer, it's configured to avoid that, but it's not impossible.

## Install
To install dependencies, clone or download the proyect, position your powershell on the root directory and run:

if you have enabled scripts execution on your system:

`.\install.ps1`

if not:

`powershell -ExecutionPolicy Bypass -File "install.ps1"`


## Use
To execute, run:
1. `.\venv\Scripts\activate`
2. `python main.py`

## Commands

- help: Returns all the commands info.
- playlist: Provide the playlist url and the folder name where the songs will be placed.
- list: Provide the playlist url and the program will tell you what songs and how much has that playlist.
- song: Provide the song url and this will be placed on your downloads folder.
- exit: Exit the program.
