from peewee import SqliteDatabase, Model, CharField, FloatField, sqlite3

db = SqliteDatabase('data/race_data.db')


class BaseModel(Model):
    class Meta:
        database = db


class BestTable(BaseModel):
    driver_name = CharField()
    team_name = CharField()
    lap_time = FloatField()


class InvalidTable(BaseModel):
    driver_name = CharField()
    team_name = CharField()
    lap_time = CharField()


db.connect()
db.create_tables([BestTable, InvalidTable], safe=True)

conn = sqlite3.connect('data/race_data.db')
cursor = conn.cursor()

conn.close()
