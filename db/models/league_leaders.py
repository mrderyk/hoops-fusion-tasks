from peewee import Model, CharField, DateTimeField
from playhouse.postgres_ext import BinaryJSONField
from .. connection import db


class LeagueLeadersRegular(Model):
  class Meta:
    database = db
    db_table = 'league_leaders_regular'

  category = CharField()
  date = DateTimeField()
  player_keys_and_stats = BinaryJSONField()

  def serialize(self):
    return {
      'id': self.id,
      'category': self.category,
      'date': self.date,
      'player_keys_and_stats': self.player_keys
    }

class LeagueLeadersPlayoff(LeagueLeadersRegular):
  class Meta:
    database = db
    db_table = 'league_leaders_playoff'