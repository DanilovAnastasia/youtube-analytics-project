import os
import json
from googleapiclient.discovery import build

YT_API_KEY = os.getenv('API_KEY')


class Video:
    """Класс для ютуб-видео"""

    youtube = build('youtube', 'v3', developerKey=YT_API_KEY)


    def __init__(self, video_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        try:
            self.video_id = video_id
            self.video = self.youtube.videos().list(id=self.video_id, part='snippet,statistics').execute()
            # self.video_id = self.video['items'][0]['id']
            self.title = self.video['items'][0]['snippet']['title']
            self.video_url = self.video['items'][0]['snippet']['thumbnails']['default']['url']
            self.video_number_views = self.video['items'][0]['statistics']['viewCount']
            self.like_count = self.video['items'][0]['statistics']['likeCount']
        except IndexError:
            self.title = None
            self.video_url = None
            self.video_number_views = None
            self.like_count = None

    def __str__(self):
        return f'{self.title}'

    @classmethod
    def get_service(cls):
        youtube = build('youtube', 'v3', developerKey=YT_API_KEY)
        return youtube

    # def to_json(self, dict_to_print) -> None:
    #     """Сохраняет в файл значения атрибутов экземпляра `Video`"""
    #
    #     with open(dict_to_print, "w", encoding='utf-8') as write_file:
    #         json.dump({"id": self.video_id,
    #                    "title": self.title,
    #                    "url": self.video_url,
    #                    "likeCount": self.like_count,
    #                    "viewCount": self.video_number_views}, write_file, indent=2, ensure_ascii=False,
    #                   separators=(',', ': '))
    #         print(dict_to_print)


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id


