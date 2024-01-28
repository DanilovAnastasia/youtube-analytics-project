import os
import json
from googleapiclient.discovery import build
from src.video import Video
import isodate
from datetime import timedelta

YT_API_KEY = os.getenv('API_KEY')

class PlayList():

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
        best_like_video = 0
        for video in video_response['items']:
            if best_like_video or best_like_video < int(video['statistics']['likeCount']):
                best_url_video, best_like_video = video['id'], int(video['statistics']['likeCount'])
        return f"https://youtu.be/{best_url_video}"

    # def total_duration(self):
    #     """
    #     Возвращает объект класса `datetime.timedelta` с суммарной длительность плейлиста
    #     """
    #     playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
    #                                                    part='contentDetails',
    #                                                    maxResults=50,
    #                                                    ).execute()
    #
    #     video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
    #     video_response = youtube.videos().list(part='contentDetails,statistics',
    #                                            id=','.join(video_ids)
    #                                            ).execute()
    #
    #     total_video_diration = datetime.timedelta(hours=0, minutes=0, seconds=0)
    #
    #     for video in video_response['items']:
    #         iso_8601_duration = video['contentDetails']['duration']
    #         duration = isodate.parse_duration(iso_8601_duration)
    #
    #         duration_split = str(duration).split(':')
    #         duration = datetime.timedelta(hours=int(duration_split[0]), minutes=int(duration_split[1]),
    #                                       seconds=int(duration_split[2]))
    #         print(duration)
    #         total_video_diration += duration
    #
    #     return total_video_diration

    # def show_best_video(self):
    #     """
    #     Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)
    #     """
    #     playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
    #                                                    part='contentDetails',
    #                                                    maxResults=50,
    #                                                    ).execute()
    #
    #     video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
    #     video_response = youtube.videos().list(part='contentDetails,statistics',
    #                                            id=','.join(video_ids)
    #                                            ).execute()
    #
    #     video_like_count = 0
    #     video_url = ''
    #
    #     for video in video_response['items']:
    #         like_count = int(video['statistics']['likeCount'])
    #
    #         if like_count > video_like_count:
    #             video_like_count = like_count
    #             video_url = f"https://youtu.be/{video['id']}"
    #
    #     return video_url


# class PlayList(Video):
#     def __init__(self, playlist_id):
#         playlists = super().get_service().playlists().list(id=playlist_id,
#                                                            part='id,snippet',
#                                                            ).execute()
#         self.playlist_id = playlist_id
#         self.title = playlists['items'][0]['snippet']['title']
#         self.url = f"https://www.youtube.com/playlist?list={playlists['items'][0]['id']}"
#         playlist_videos = super().get_service().playlistItems().list(playlistId=playlist_id,
#                                                                      part='contentDetails',
#                                                                      maxResults=50,
#                                                                      ).execute()
#         playlist_video_ids = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
#         self.video_response = super().get_service().videos().list(part='contentDetails,statistics',
#                                                                   id=','.join(playlist_video_ids)
#                                                                   ).execute()
#
#     @property
#     def total_duration(self):
#         duration = 0
#         for video in self.video_response['items']:
#             iso_8601_duration = video['contentDetails']['duration']
#             duration += isodate.parse_duration(iso_8601_duration).seconds
#         return timedelta(seconds=duration)
#
#     def show_best_video(self):
#         best_like_video = 0
#         for video in self.video_response['items']:
#             if best_like_video or best_like_video < int(video['statistics']['likeCount']):
#                 best_url_video, best_like_video = video['id'], int(video['statistics']['likeCount'])
#         return f"https://youtu.be/{best_url_video}"