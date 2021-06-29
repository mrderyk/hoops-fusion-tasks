import peewee

from enum import Enum
from utils import compute_key_for_player, compute_stats_key_for_player, fetch
from hfdb.models import PlayerStatsPlayoff, PlayerStatsRegular

class StatType(Enum):
  REGULAR = "regular"
  PLAYOFF = "playoff"

def collect(stat_type=StatType.REGULAR, seasons=[]):
  for season in seasons:
    r = fetch('{season}-{stat_type}/player_stats_totals.json'.format(season=season, stat_type=stat_type.value))

    if not r:
      continue

    # normalize erroneous playoffs season API values until we hear back from stats provider
    if stat_type == StatType.PLAYOFF:
      if season == '2020-2021':
        season = '2019-2020'
      elif season == '2021-2022':
        season = '2020-2021'
    else:
      season = season

    players_stats_data = r.json()['playerStatsTotals']

    if players_stats_data:
      for player_stats_data in players_stats_data:
        player = player_stats_data['player']
        stats = player_stats_data['stats']
        last_name = player['lastName']
        first_name = player['firstName']
        external_api_id = player['id']

        # TODO: Create a model for this expected data structure, separate from the db model.
        player_key = compute_key_for_player(
          first_name,
          last_name,
          external_api_id
        )

        player_stats_key = compute_stats_key_for_player(
          first_name,
          last_name,
          external_api_id,
          season
        )

        # We collect archived stats once per day.
        # Delete live game cached stats from previous day.
        #_redis.delete(player_key)

        DBModel = PlayerStatsRegular if stat_type == StatType.REGULAR else PlayerStatsPlayoff

        try:
          p = DBModel.get(key=player_stats_key)
        except peewee.DoesNotExist:
          p = DBModel.create(key=player_stats_key)

        p.player_key = player_key
        p.season = season

        # games played
        p.gp = int(stats['gamesPlayed'])

        # field goals
        stats_field_goals = stats['fieldGoals']

        p.fg2a = int(stats_field_goals['fg2PtAtt'])
        p.fg2apg = float(stats_field_goals['fg2PtAttPerGame'])
        p.fg2m = int(stats_field_goals['fg2PtMade'])
        p.fg2mpg = float(stats_field_goals['fg2PtMadePerGame'])
        p.fg2pct = float(stats_field_goals['fg2PtPct'])

        # 3pt field goals
        p.fg3a = int(stats_field_goals['fg3PtAtt'])
        p.fg3apg = float(stats_field_goals['fg3PtAttPerGame'])
        p.fg3m = int(stats_field_goals['fg3PtMade'])
        p.fg3mpg = float(stats_field_goals['fg3PtMadePerGame'])
        p.fg3pct = float(stats_field_goals['fg3PtPct'])

        # all field goals
        p.fga = int(stats_field_goals['fgAtt'])
        p.fgapg = float(stats_field_goals['fgAttPerGame'])
        p.fgm = int(stats_field_goals['fgMade'])
        p.fgmpg = float(stats_field_goals['fgMadePerGame'])
        p.fgpct = float(stats_field_goals['fgPct'])

        # free throws
        stats_free_throws = stats['freeThrows']
        p.fta = int(stats_free_throws['ftAtt'])
        p.ftapg = float(stats_free_throws['ftAttPerGame'])
        p.ftm = int(stats_free_throws['ftMade'])
        p.ftmpg = float(stats_free_throws['ftMadePerGame'])
        p.ftpct = float(stats_free_throws['ftPct'])

        # rebounds
        stats_rebounds = stats['rebounds']
        p.oreb = int(stats_rebounds['offReb'])
        p.orebpg = float(stats_rebounds['offRebPerGame'])
        p.dreb = int(stats_rebounds['defReb'])
        p.drebpg = float(stats_rebounds['defRebPerGame'])
        p.reb = int(stats_rebounds['reb'])
        p.rebpg = float(stats_rebounds['rebPerGame'])

        # offense
        stats_offense = stats['offense']

        # assists
        p.ast = int(stats_offense['ast'])
        p.astpg = float(stats_offense['astPerGame'])

        # points
        p.pts = int(stats_offense['pts'])
        p.ptspg = float(stats_offense['ptsPerGame'])

        # defense
        stats_defense = stats['defense']

        # turnovers
        p.tov = int(stats_defense['tov'])
        p.tovpg = float(stats_defense['tovPerGame'])

        # steals
        p.stl = int(stats_defense['stl'])
        p.stlpg = float(stats_defense['stlPerGame'])

        # blocks
        p.blk = int(stats_defense['blk'])
        p.blkpg = float(stats_defense['blkPerGame'])
        p.blka = int(stats_defense['blkAgainst'])
        p.blkapg = float(stats_defense['blkAgainstPerGame'])

        # misc
        stats_misc = stats['miscellaneous']
        p.gs = int(stats_misc['gamesStarted'])

        # fouls
        p.foul = int(stats_misc['fouls'])
        p.foulpg = float(stats_misc['foulsPerGame'])
        p.fould = int(stats_misc['foulsDrawn'])
        p.fouldpg = float(stats_misc['foulsDrawnPerGame'])
        p.foulp = int(stats_misc['foulPers'])
        p.foulppg = float(stats_misc['foulPersPerGame'])
        p.foulpd = int(stats_misc['foulPersDrawn'])
        p.foulpdpg = float(stats_misc['foulPersDrawnPerGame'])
        p.foult = int(stats_misc['foulTech'])
        p.foultpg = float(stats_misc['foulTechPerGame'])
        p.foultd = int(stats_misc['foulTechDrawn'])
        p.foultdpg = float(stats_misc['foulTechDrawnPerGame'])
        p.foulf1 = int(stats_misc['foulFlag1'])
        p.foulf1pg = float(stats_misc['foulFlag1PerGame'])
        p.foulf1d = int(stats_misc['foulFlag1Drawn'])
        p.foulf1dpg = float(stats_misc['foulFlag1DrawnPerGame'])
        p.foulf2 = int(stats_misc['foulFlag2'])
        p.foulf2pg = float(stats_misc['foulFlag2PerGame'])
        p.foulf2d = int(stats_misc['foulFlag2Drawn'])
        p.foulf2dpg = float(stats_misc['foulFlag2DrawnPerGame'])

        # ejections
        p.ejection = int(stats_misc['ejections'])

        # plus/minus
        p.pm = int(stats_misc['plusMinus'])
        p.pmpg = float(stats_misc['plusMinusPerGame'])

        # minutes
        p.min = int(stats_misc['minSeconds'])/60
        p.minpg = float(stats_misc['minSecondsPerGame'])/60
        p.save()

        print('# Updating {season} stats for player {key} - {last_name}, {first_name}...'.format(
            season=season,
            key=player_key,
            last_name=last_name,
            first_name=first_name
        ))


collect(stat_type=StatType.PLAYOFF)