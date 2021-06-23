import json
from peewee import Model, CharField, IntegerField, DecimalField

from db.connection import db

class PlayerStatsRegular(Model):
  class Meta:
    database = db
    db_table = 'players_stats_regular'

  season = CharField(max_length=9)
  player_key = CharField()
  key = CharField(primary_key=True)

  # games played
  gp = IntegerField(default=0)

  # games_missed
  gm = IntegerField(default=0)

  # games started
  gs = IntegerField(default=0)

  # field goals
  fg2a = IntegerField(default=0)
  fg2apg = DecimalField(default=0.0)
  fg2m = IntegerField(default=0)
  fg2mpg = DecimalField(default=0.0)
  fg2pct = DecimalField(default=0.0)

  # 3pt field goals
  fg3a = IntegerField(default=0)
  fg3apg = DecimalField(default=0.0)
  fg3m = IntegerField(default=0)
  fg3mpg = DecimalField(default=0.0)
  fg3pct = DecimalField(default=0.0)

  # all field goals
  fga = IntegerField(default=0)
  fgapg = DecimalField(default=0.0)
  fgm = IntegerField(default=0)
  fgmpg = DecimalField(default=0.0)
  fgpct = DecimalField(default=0.0)

  # free throws
  fta = IntegerField(default=0)
  ftapg = DecimalField(default=0.0)
  ftm = IntegerField(default=0)
  ftmpg = DecimalField(default=0.0)
  ftpct = DecimalField(default=0.0)

  # rebounds
  oreb = IntegerField(default=0)
  orebpg = DecimalField(default=0.0)
  dreb = IntegerField(default=0)
  drebpg = DecimalField(default=0.0)
  reb = IntegerField(default=0)
  rebpg = DecimalField(default=0.0)

  # assists
  ast = IntegerField(default=0)
  astpg = DecimalField(default=0.0)

  # points
  pts = IntegerField(default=0)
  ptspg = DecimalField(default=0.0)

  # turnovers
  tov = IntegerField(default=0)
  tovpg = DecimalField(default=0.0)

  # steals
  stl = IntegerField(default=0)
  stlpg = DecimalField(default=0.0)

  # blocks
  blk = IntegerField(default=0)
  blkpg = DecimalField(default=0.0)
  blka = IntegerField(default=0)
  blkapg = DecimalField(default=0.0)

  # fouls
  foul = IntegerField(default=0)
  foulpg = DecimalField(default=0.0)
  fould = IntegerField(default=0)
  fouldpg = DecimalField(default=0.0)
  foulp = IntegerField(default=0)
  foulppg = DecimalField(default=0.0)
  foulpd = IntegerField(default=0)
  foulpdpg = DecimalField(default=0.0)
  foult = IntegerField(default=0)
  foultpg = DecimalField(default=0.0)
  foultd = IntegerField(default=0)
  foultdpg = DecimalField(default=0.0)
  foulf1 = IntegerField(default=0)
  foulf1pg = DecimalField(default=0.0)
  foulf1d = IntegerField(default=0)
  foulf1dpg = DecimalField(default=0.0)
  foulf2 = IntegerField(default=0)
  foulf2pg = DecimalField(default=0.0)
  foulf2d = IntegerField(default=0)
  foulf2dpg = DecimalField(default=0.0)

  # ejections
  ejection = IntegerField(default=0)

  # plus/minus
  pm = IntegerField(default=0)
  pmpg = DecimalField(default=0.0)

  # minutes
  min = IntegerField(default=0)
  minpg = DecimalField(default=0.0)

  @property
  def parameter_formatted(self):
      return '{first_name}-{last_name}'.format(
          first_name=self.first_name,
          last_name=self.last_name
      )

  def serialize(self):
    return {
      'player_key': self.player_key,
      'stats': {
        'gp': self.gp,
        'gm': self.gm,
        'gs': self.gs,
        'fg2a': self.fg2a,
        'fg2apg': float(self.fg2apg),
        'fg2m': self.fg2m,
        'fg2mpg': float(self.fg2mpg),
        'fg2pct': float(self.fg2pct),
        'fg3a': self.fg3a,
        'fg3apg': float(self.fg3apg),
        'fg3m': self.fg3m,
        'fg3mpg': float(self.fg3mpg),
        'fg3pct': float(self.fg3pct),
        'fga': self.fga,
        'fgapg': float(self.fgapg),
        'fgm': self.fgm,
        'fgmpg': float(self.fgmpg),
        'fgpct': float(self.fgpct),
        'fta': self.fta,
        'ftapg': float(self.ftapg),
        'ftm': self.ftm,
        'ftmpg': float(self.ftmpg),
        'ftpct': float(self.ftpct),
        'oreb': self.oreb,
        'orebpg': float(self.orebpg),
        'dreb': self.dreb,
        'drebpg': float(self.drebpg),
        'reb': self.reb,
        'rebpg': float(self.rebpg),
        'ast': self.ast,
        'astpg': float(self.astpg),
        'pts': self.pts,
        'ptspg': float(self.ptspg),
        'tov': self.tov,
        'tovpg': float(self.tovpg),
        'stl': self.stl,
        'stlpg': float(self.stlpg),
        'blk': self.blk,
        'blkpg': float(self.blkpg),
        'blka': self.blka,
        'blkapg': float(self.blkapg),
        'foul': self.foul,
        'foulpg': float(self.foulpg),
        'fould': self.fould,
        'fouldpg': float(self.fouldpg),
        'foulp': self.foulp,
        'foulppg': float(self.foulppg),
        'foulpd': self.foulpd,
        'foulpdpg': float(self.foulpdpg),
        'foult': self.foult,
        'foultpg': float(self.foultpg),
        'foultd': self.foultd,
        'foultdpg': float(self.foultdpg),
        'foulf1': self.foulf1,
        'foulf1pg': float(self.foulf1pg),
        'foulf1d': self.foulf1d,
        'foulf1dpg': float(self.foulf1dpg),
        'foulf2': self.foulf2,
        'foulf2pg': float(self.foulf2pg),
        'foulf2d': self.foulf2d,
        'foulf2dpg': float(self.foulf2dpg),
        'ejection': self.ejection,
        'pm': self.pm,
        'pmpg': float(self.pmpg),
        'min': self.min,
        'minpg': float(self.minpg)
      }
    }

class PlayerStatsPlayoff(PlayerStatsRegular):
  class Meta:
    database = db
    db_table = 'players_stats_playoffs'