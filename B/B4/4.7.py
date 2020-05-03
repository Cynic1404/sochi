
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///b4_7.sqlite3"

Base = declarative_base()

class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """
    # указываем имя таблицы
    __tablename__ = "album"
    # Задаем колонки в формате
    # название_колонки = sa.Column(ТИП_КОЛОНКИ)
    # идентификатор строки
    id = sa.Column(sa.INTEGER, primary_key=True)
    # Год запис	и альбома
    year = sa.Column(sa.INTEGER)
    # артист или группа, записавшие альбом
    artist = sa.Column(sa.TEXT)
    # жанр альбома
    genre = sa.Column(sa.TEXT)
    # название альбома
    album = sa.Column(sa.TEXT)

# создаем соединение к базе данных
engine = sa.create_engine(DB_PATH)
# создаем фабрику сессию
Sessions = sessionmaker(engine)
# cоздаем сессию
session = Sessions()

# передаем модель Album в метод session.query и вызываем метод all
albums = session.query(Album).all()

for album in albums:
    if album.year==2017:
        print(f"Группа {album.artist} записала альбом {album.album} в жанре {album.genre} в {album.year} году")