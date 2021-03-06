from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///albums.sqlite3"

Base = declarative_base()

class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """

    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)

def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def find(artist):
    """
    Находит все альбомы в базе данных по заданному артисту
    """
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums



@route("/albums", method="POST")
def album():
    session = connect_db()
    album_data = {
        "year" : request.forms.get("year"),
        "artist" : request.forms.get("artist"),
        "genre" : request.forms.get("genre"),
        "album" : request.forms.get("album")
    }

    # проверка, что все поля введены
    if None in (album_data['artist'], album_data['genre'] , album_data['album'], album_data['year']):
        raise HTTPError(409, 'Введены не все данные')
    #проверка введенного года на валидность
    if album_data['year'].isnumeric() == False:
        print('Year should be a number')
        raise HTTPError (409, 'Year should be a number')


        #проверка базы данных на наличие альбома
    album_in_db = session.query(Album).filter(Album.album == album_data['album'], Album.artist == album_data['artist']).first()
    if album_in_db:
        print('Такой альбом уже есть в базе. Его ID - {}'.format(album_in_db.id))
        raise HTTPError (409, 'Такой альбом уже есть в базе')

    #внесение в базу данных
    else:
        new_album = Album(
            year=album_data['year'],
            artist=album_data['artist'],
            genre=album_data['genre'],
            album=album_data['album']
        )
        session.add(new_album)
        session.commit()
        print('Album added', album_data)
        return album_data



@route("/albums/<artist>")
def albums(artist):
    albums_list = find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        head = "Группа {} альбомов выпустила {} альбомов:<br>".format(artist, len(album_names))
        album_list = ''
        for i in ['<li>'+i for i in album_names]:
            album_list+=i
        result = head + '<ul>'+album_list+'</ul>'
    return result




if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)


