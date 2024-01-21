import os
import json
from googleapiclient.discovery import build

YT_API_KEY = os.getenv('API_KEY')


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        youtube = self.get_service()
        ch = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.__channel_id = channel_id
        self.title = ch['items'][0]['snippet']['title']
        self.description = ch['items'][0]['snippet']['description']
        self.url = f'https://www.youtube.com/channel/{self.__channel_id}'
        self.subscribers = ch['items'][0]['statistics']['subscriberCount']
        self.video_count = ch['items'][0]['statistics']['videoCount']
        self.view = ch['items'][0]['statistics']['viewCount']


    def __str__(self):
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        """складывает количество подписчиков с двух каналов"""
        return int(self.subscribers) + int(other.subscribers)

    def __sub__(self, other):
        """вычитает количество подписчиков другого канала из основного"""
        return int(self.subscribers) - int(other.subscribers)

    def __lt__(self, other):
        """сравнение меньше"""
        return int(self.subscribers) < int(other.subscribers)

    def __le__(self, other):
        """сравнение меньше или равно"""
        return int(self.subscribers) <= int(other.subscribers)

    def __gt__(self, other):
        """сравнение больше"""
        return int(self.subscribers) > int(other.subscribers)

    def __ge__(self, other):
        """сравнение больше или равно"""
        return int(self.subscribers) >= int(other.subscribers)

    def __eq__(self, other):
        """сравнение на идентичность"""
        return int(self.subscribers) == int(other.subscribers)


    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        youtube = build('youtube', 'v3', developerKey=YT_API_KEY)
        return youtube

    def to_json(self, path):
        json_dict = {"id": self.__channel_id,
                     "Title": self.title,
                     "Description": self.description,
                     "url": self.url,
                     "Subscribers": self.subscribers,
                     "Video": self.video_count,
                     "View": self.view}
        with open(path, 'w') as outfile:
            json.dump(json_dict, outfile, ensure_ascii=False)

    def print_info(self):
        """Выводит в консоль информацию о канале."""
        youtube = build('youtube', 'v3', developerKey=YT_API_KEY)
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))