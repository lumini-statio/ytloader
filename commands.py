import cmd
import sys
from abc import ABC, abstractmethod
from download import Downloader
from typing import List, Tuple


class Command(ABC):
    @abstractmethod
    def execute(self, args):
        pass
    
    @abstractmethod
    def get_name(self, args):
        pass

    @abstractmethod
    def get_description(self, args):
        pass


class DownloadPlaylist(Command):
    def __init__(self, downloader: Downloader):
        self.downloader = downloader

    def execute(self, args):
        if len(args) < 1:
            print("Error: You might set the playlist URL")
            print("Use: playlist <url_playlist> [directory_name]")
            return False
        
        url_playlist = args[0]
        directory_name = args[1] if len(args) > 1 else "~/Music"
        directory_name = f"~/Music/{directory_name}"
        
        print(f"Downloading playlist...")
        
        try:
            self.downloader.download_playlist(url_playlist, directory_name)
            print("Download Complete!")
        except Exception as e:
            print(f"Error in playlist download: {e}")
        
        return False
    
    def get_name(self) -> str:
        return "playlist"
    
    def get_description(self) -> str:
        return "Download a YouTube playlist: playlist <url> [directory]"


class ListSongsCommand(Command):
    def __init__(self, downloader: Downloader):
        self.downloader = downloader
    
    def execute(self, args: List[str]) -> bool:
        if len(args) < 1:
            print("Error: You might set the playlist URL")
            print("Use: list <url_playlist>")
            return False
        
        url_playlist = args[0]
        
        try:
            print('Extracting songs...')
            songs = self.downloader.get_playlist_videos(url_playlist)
            
            if not songs:
                print("Not songs founded in the playlist...")
                return False
            
            print(f"\nsongs founded ({len(songs)}):")
            for i, (titulo, url) in enumerate(songs, 1):
                print(f"  {i}. {titulo.replace('_', ' ')}")
            
        except Exception as e:
            print(f"Error to get the list: {e}")
        
        return False
    
    def get_name(self, args):
        return "list"
    
    def get_description(self) -> str:
        return "List a playlist videos: list <url>"


class DownloadSongCommand(Command):
    def __init__(self, downloader: Downloader):
        self.downloader = downloader
    
    def execute(self, args: List[str]) -> bool:
        if len(args) < 1:
            print("Error: You might set song URL")
            print("Use: song <url_song> [filename]")
            return False
        
        url_song = args[0]
        filename = args[1] if len(args) > 1 else "song_downloaded"
        filename = f'~/Downloads/{filename}'

        print(f"Downloading song...")
        
        try:
            self.downloader.download_audio(url_song, filename)
            print("\nSong downloaded on your Downloads directory!")
        except Exception as e:
            print(f"Error in song download: {e}")
        
        return False
    
    def get_name(self) -> str:
        return "song"
    
    def get_description(self) -> str:
        return "Download an individual song: song <url> [name]"


class HelpCommand(Command):
    def __init__(self, register_commands):
        self.commands = register_commands
    
    def execute(self, args: List[str]) -> bool:
        print("\nYouTube Downloader - available commands:")
        print("=" * 50)
        for name, command in self.commands.items():
            print(f"  {name:12} - {command.get_description()}")

        print("\n💡 Examples:")
        print("  playlist https://www.youtube.com/playlist?list=OLAK5uy_lXqIRZtLoDPhkivuHfrMVK_dXI3fyiHJk hamilton")
        print("  list https://www.youtube.com/playlist?list=OLAK5uy_lXqIRZtLoDPhkivuHfrMVK_dXI3fyiHJk")
        print("  song https://www.youtube.com/watch?v=eKFN-aqPJH8&si=EBHnACHEyRGImkZi youll_be_back")
        print("  exit")
        return False
    
    def get_name(self) -> str:
        return "help"
    
    def get_description(self) -> str:
        return "Help here!"


class ExitCommand(Command):
    def execute(self, args: List[str]) -> bool:
        print("Exiting...")
        return True
    
    def get_name(self) -> str:
        return "exit"
    
    def get_description(self) -> str:
        return "Exit application"