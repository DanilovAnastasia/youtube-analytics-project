import os
from googleapiclient.discovery import build
import isodate
from datetime import timedelta

YT_API_KEY = os.getenv('API_KEY')


class PlayList:

    youtube = build('youtube', 'v3', developerKey=YT_API_KEY)

    def __init__(self, playlist_id: str):
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.playlist_id = playlist_id
        self.playlist = self.youtube.playlists().list(part='snippet', id=playlist_id).execute()
        self.title = self.playlist['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={playlist_id}"

    @property
    def total_duration(self):
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                                     part='contentDetails',
                                                                     maxResults=50,
                                                                     ).execute()
        playlist_video_ids = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                                  id=','.join(playlist_video_ids)
                                                                  ).execute()
        duration = 0
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration += isodate.parse_duration(iso_8601_duration).seconds
        return timedelta(seconds=duration)

    def show_best_video(self):
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()
        playlist_video_ids = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(playlist_video_ids)
                                                    ).execute()
        best_url_video = ""
        best_like_video = 0
        for video in video_response['items']:
            if best_like_video or best_like_video < int(video['statistics']['likeCount']):
                best_url_video, best_like_video = video['id'], int(video['statistics']['likeCount'])
        return f"https://youtu.be/{best_url_video}"