from commands import DownloadPlaylistAudio, ListSongsCommand, \
    DownloadSongCommand, DownloadPlaylistVideo, DownloadVideoCommand, \
    HelpCommand, ExitCommand
from download import Downloader


class CLI:
    def __init__(self):
        self.downloader = Downloader()
        self.commands = {}
        self._register_commands()
    
    def _register_commands(self):
        self.commands["playlist"] = DownloadPlaylistAudio(self.downloader)
        self.commands["list"] = ListSongsCommand(self.downloader)
        self.commands["song"] = DownloadSongCommand(self.downloader)
        self.commands["playlist_video"] = DownloadPlaylistVideo(self.downloader)
        self.commands["video"] = DownloadVideoCommand(self.downloader)
        self.commands["help"] = HelpCommand(self.commands)
        self.commands["exit"] = ExitCommand()
    
    def execute(self):
        print("YouTube Downloader - Console App")
        print("======================================")
        print("<?> Type 'help' to see available commands")
        
        while True:
            try:
                enter = input("\n>> ").strip()
                if not enter:
                    continue
                
                parts = enter.split()
                command_name = parts[0].lower()
                if command_name in ["video_playlist", "playlist-video"]:
                    command_name = "playlist_video"
                args = parts[1:] if len(parts) > 1 else []
                
                if command_name in self.commands:
                    might_exit = self.commands[command_name].execute(args)
                    if might_exit:
                        break
                else:
                    print(f"Command not recognized: {command_name}")
                    print("<?> Type 'help' to see available commands")
            
            except KeyboardInterrupt:
                print("\n\n Interrupted app by user")
                break
            except Exception as e:
                print(f"Error: {e}")