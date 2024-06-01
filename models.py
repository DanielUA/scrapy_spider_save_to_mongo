from mongoengine import Document, StringField, ListField, connect

# Подключение к базе данных
PASSWORD = 'example'
USER_NAME = 'userweb16'
connect(db='hw', host=f'mongodb+srv://{USER_NAME}:{PASSWORD}@cluster0.q1gz4ma.mongodb.net/')

# Модель для автора
class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(required=True)
    born_location = StringField(required=True)
    description = StringField(required=True)

# Модель для цитаты
class Quote(Document):
    quote = StringField(required=True, unique_with='author')  # уникальность цитаты с автором
    author = StringField(required=True)  # Используем строку вместо ReferenceField для упрощения
    tags = ListField(StringField())
