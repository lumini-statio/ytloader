import yt_dlp
import os
import random
import time


class Downloader:
    def get_playlist_videos(self, playlist_url: str):
        """Extract songs titles and URLs from a yt playlist.
        
        Args:
            playlist_url (str): Playlist URL
            
        Returns:
            songs (list[tuple]): song titles and URLs.
        """
        ydl_opts = {
            'extract_flat': True,  # ⬅️ Solo metadata de la playlist
            'quiet': True,
            'ignoreerrors': True,
            'no_warnings': True,
        }
        
        songs = []
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                playlist_info = ydl.extract_info(playlist_url, download=False)
                
                for entry in playlist_info['entries']:
                    if entry:
                        video_url: str = entry.get('url')
                        video_title: str = entry.get('title').replace(' ', '_')
                        song = (video_title, video_url)
                        if video_url:
                            songs.append(song)
                
            except Exception as e:
                print(f"Error to process the playlist: {e}")
        
        return songs


    def download_audio(self, youtube_url: str, set_filename: str = 'temp_file', extension: str = 'mp3'):
        """download audio from a youtube url and save as a file.

        args:
            youtube_url (str): youtube video url.
            set_filename (str): output filename. default 'temp_file'.
            extension (str): audio file extension. default 'mp3'.

        returns:
            none: downloads and saves the audio file.
        """
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'http_headers': {
                'User-Agent': random.choice([
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
                    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
                ]),
            },
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': extension,
            }],
            'retries': 5,
            'fragment_retries': 5,
            'skip_unavailable_fragments': True,
            'extract_flat': False,
            'wait_for_video': (10, 30),
            'outtmpl': set_filename,
            'quiet': False,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])


    def download_playlist(self, playlist_url: str, dir_name: str = ''):
        songs = self.get_playlist_videos(playlist_url)

        os.makedirs(name=dir_name, exist_ok=True)

        for i, song in enumerate(songs):
            self.download_audio(
                youtube_url=song[1],
                set_filename=f'{dir_name}/{song[0]}',
            )

            if i < len(songs) - 1:
                pause_time = random.uniform(5, 15)
                time.sleep(pause_time)
