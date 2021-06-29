import functools
import operator
from datetime import datetime, timezone

from compute.league_leader_criteria import LeagueLeaderCriteria
from compute.utils import get_leader_categories_with_criteria
from hfdb.models import LeagueLeadersRegular, PlayerStatsRegular

dt = datetime.now(timezone.utc)
utc_time = dt.replace(tzinfo=timezone.utc)

SEASON_TOTAL_GAMES = 72
MIN_PRESTIGE_STATS_GAME_PERCENTAGE = 70
SEASON = '2020-2021'

default_qualifying_criteria = LeagueLeaderCriteria(SEASON_TOTAL_GAMES)
simple_qualifying_criteria = LeagueLeaderCriteria(SEASON_TOTAL_GAMES, MIN_PRESTIGE_STATS_GAME_PERCENTAGE)
categories_to_qualifying_criteria = get_leader_categories_with_criteria(
  ptspg=simple_qualifying_criteria,
  astpg=simple_qualifying_criteria,
  rebpg=simple_qualifying_criteria,
  orebpg=simple_qualifying_criteria,
  drebpg=simple_qualifying_criteria,
  stlpg=simple_qualifying_criteria,
  blkpg=simple_qualifying_criteria,
  ftapg=simple_qualifying_criteria,
  ftmpg=simple_qualifying_criteria,
  fg3mpg=simple_qualifying_criteria,
  fgpct=LeagueLeaderCriteria(SEASON_TOTAL_GAMES, MIN_PRESTIGE_STATS_GAME_PERCENTAGE, 'fgmpg', 3.65),
  fg2pct=LeagueLeaderCriteria(SEASON_TOTAL_GAMES, MIN_PRESTIGE_STATS_GAME_PERCENTAGE, 'fg2mpg', 2.65),
  fg3pct=LeagueLeaderCriteria(SEASON_TOTAL_GAMES, MIN_PRESTIGE_STATS_GAME_PERCENTAGE, 'fg3mpg', 1.0),
  ftpct=LeagueLeaderCriteria(SEASON_TOTAL_GAMES, MIN_PRESTIGE_STATS_GAME_PERCENTAGE, 'ftmpg', 1.52)
)

def computeLeaders():
  for k in categories_to_qualifying_criteria:
    # Determine where clauses based on qualifying criteria, if applicable
    where_clauses = [(PlayerStatsRegular.season == SEASON)]
    qualifying_criteria = categories_to_qualifying_criteria.get(k)
    qualifying_criteria = qualifying_criteria if qualifying_criteria else default_qualifying_criteria
    min_games_played = qualifying_criteria.get_min_games_played()
    if min_games_played:
      where_clauses.append((PlayerStatsRegular.gp >= qualifying_criteria.get_min_games_played()))

    query = PlayerStatsRegular.select(PlayerStatsRegular.player_key, getattr(PlayerStatsRegular, k)) \
                              .where(functools.reduce(operator.and_, where_clauses)) \
                              .order_by(getattr(PlayerStatsRegular, k).desc()) \
                              .limit(10)

    formatted_date_from_timestamp = datetime.utcfromtimestamp(utc_time.timestamp()).strftime('%Y-%m-%d %H:%M:%S')
    print ('Adding league leaders for {category} on {date}...'.format(category=k.upper(), date=formatted_date_from_timestamp))      

    player_keys_and_stats = []               
    for result in query:
      player_keys_and_stats.append({
        'player_key': result.player_key,
        'stat': float(getattr(result, k))
      })

    LeagueLeadersRegular.create(
      category=k,
      date=dt,
      player_keys_and_stats=player_keys_and_stats
    )

computeLeaders()