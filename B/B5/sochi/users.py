import datetime

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///sochi_athletes.sqlite3"

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id = sa.Column(sa.INTEGER, primary_key=True)
    first_name = sa.Column(sa.TEXT)
    last_name = sa.Column(sa.TEXT)
    gender = sa.Column(sa.TEXT)
    email = sa.Column(sa.TEXT)
    birthdate = sa.Column(sa.TEXT)
    height = sa.Column(sa.REAL)



def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def request_data():
    print("Привет! Я запишу твои данные!")
    first_name = input("Введи своё имя: ")
    last_name = input("А теперь фамилию: ")
    email = input("Мне еще понадобится адрес твоей электронной почты: ")
    gender = input("Пол: ")

    '''
    код проверяет, что дата рождения записана в верном формате,
    иначе - запрашивается повторвый ввод
    '''
    birthdate = input("Дата рождения (формат YYYY-MM-DD): ")
    try:
        datetime.datetime.strptime(birthdate, '%Y-%m-%d')
    except ValueError:
        check_date = False
        while check_date == False:
            birthdate= input('Неверный формат. Введите дату рождения (формат YYYY-MM-DD): ')
            try:
                datetime.datetime.strptime(birthdate, '%Y-%m-%d')
                check_date = True
            except ValueError:
                check_date = False

    """
    можно ввести рост только 120-300 см
    """

    height = ""
    while not height.isnumeric() or (int(height) < 120 or int(height) > 300):
        print('Веедите рост в см (120-300) Используйте цифры.')
        height = input("Рост: ")
    height = height[0]+'.'+height[1:]


    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        gender = gender,
        birthdate = birthdate,
        height = height
    )
    return user



def main():
    session = connect_db()
    user = request_data()
    session.add(user)
    session.commit()
    print("Спасибо, данные сохранены!")



if __name__ == "__main__":
    main()