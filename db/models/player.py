from peewee import Model, BooleanField, CharField, IntegerField, DateField
from .. connection import db


class Player(Model):
    class Meta:
        database = db
        db_table = 'players'

    first_name = CharField()
    last_name = CharField()
    number = IntegerField()
    position = CharField()
    height = IntegerField()
    weight = IntegerField()
    dob = DateField()
    birth_city = CharField()
    birth_country = CharField()
    team_code = CharField()
    img_url = CharField()
    key = CharField()
    is_rookie = BooleanField()
    roster_status = IntegerField()
    injury = CharField()

    def serialize(self):
      return {
        'id': self.id,
        'first_name': self.first_name,
        'last_name': self.last_name,
        'number': self.number,
        'position': self.position,
        'height': self.height,
        'weight': self.weight,
        'dob': self.dob,
        'birth_city': self.birth_city,
        'birth_country': self.birth_country,
        'team_name': self.team_name,
        'key': self.key,
        'img_url': self.img_url,
        'is_rookie': self.is_rookie
      }