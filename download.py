import yt_dlp
import os
import random
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUSIC_DIR = os.path.join(BASE_DIR, 'Music')
VIDEOS_DIR = os.path.join(BASE_DIR, 'Videos')


class Downloader:
    def get_playlist_videos(self, playlist_url: str):
        """Extract songs titles and URLs from a yt playlist.
        
        Args:
            playlist_url (str): Playlist URL
            
        Returns:
            songs (list[tuple]): song titles and URLs.
        """
        ydl_opts = {
            # solo metadatos
            'extract_flat': True,
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
        if not os.path.dirname(set_filename):
            set_filename = os.path.join(MUSIC_DIR, set_filename)

        os.makedirs(os.path.dirname(set_filename), exist_ok=True)
        
        ydl_opts = {
            'format': 'bestaudio/best' if extension in ['mp3', 'm4a', 'wav'] else 'best[ext=mp4]/best',
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'ios', 'web']
                }
            },
            'retries': 5,
            'fragment_retries': 5,
            'skip_unavailable_fragments': True,
            'extract_flat': False,
            'wait_for_video': (10, 30),
            'outtmpl': f'{set_filename}.{extension}',
            'quiet': False,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])


    def download_playlist_audio(self, playlist_url: str, dir_name: str = ''):
        songs = self.get_playlist_videos(playlist_url)

        target_dir = dir_name if dir_name else MUSIC_DIR
        os.makedirs(name=target_dir, exist_ok=True)

        for i, song in enumerate(songs):
            self.download_audio(
                youtube_url=song[1],
                set_filename=os.path.join(target_dir, song[0]),
            )

            if i < len(songs) - 1:
                pause_time = random.uniform(5, 15)
                time.sleep(pause_time)


    def download_video(self, youtube_url: str, set_filename: str = 'temp_file', extension: str = 'mp4'):
        """download video from a youtube url and save as a file.

        args:
            youtube_url (str): youtube video url.
            set_filename (str): output filename. default 'temp_file'.
            extension (str): video file extension. default 'mp4'.

        returns:
            none: downloads and saves the video file.
        """
        if not os.path.dirname(set_filename):
            set_filename = os.path.join(VIDEOS_DIR, set_filename)

        os.makedirs(os.path.dirname(set_filename), exist_ok=True)
        
        ydl_opts = {
            'format': 'bestvideo*+bestaudio/best',
            'merge_output_format': extension,
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'ios', 'web']
                }
            },
            'retries': 5,
            'fragment_retries': 5,
            'skip_unavailable_fragments': True,
            'extract_flat': False,
            'wait_for_video': (10, 30),
            'outtmpl': f'{set_filename}.{extension}',
            'quiet': False,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])


    def download_playlist_video(self, playlist_url: str, dir_name: str = ''):
        songs = self.get_playlist_videos(playlist_url)

        target_dir = dir_name if dir_name else VIDEOS_DIR
        os.makedirs(name=target_dir, exist_ok=True)

        for i, song in enumerate(songs):
            self.download_video(
                youtube_url=song[1],
                set_filename=os.path.join(target_dir, song[0]),
            )

            if i < len(songs) - 1:
                pause_time = random.uniform(5, 15)
                time.sleep(pause_time)
