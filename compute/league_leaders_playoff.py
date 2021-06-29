import functools
import operator
from datetime import datetime, timezone

from compute.league_leader_criteria import LeagueLeaderCriteria
from compute.utils import get_leader_categories_with_criteria
from hfdb.models import LeagueLeadersPlayoff, PlayerStatsPlayoff

dt = datetime.now(timezone.utc)
utc_time = dt.replace(tzinfo=timezone.utc)

PLAYOFF_TOTAL_GAMES = 16

default_qualifying_criteria = LeagueLeaderCriteria(PLAYOFF_TOTAL_GAMES)
categories_to_qualifying_criteria = get_leader_categories_with_criteria()

def computeLeaders(Model, season):
  for k in categories_to_qualifying_criteria:
    # Determine where clauses based on qualifying criteria, if applicable
    where_clauses = [(Model.season == season)]
    qualifying_criteria = categories_to_qualifying_criteria.get(k)
    qualifying_criteria = qualifying_criteria if qualifying_criteria else default_qualifying_criteria
    min_games_played = qualifying_criteria.get_min_games_played()
    if min_games_played:
      where_clauses.append((Model.gp >= qualifying_criteria.get_min_games_played()))

    query = Model.select(Model.player_key, getattr(Model, k)) \
                              .where(functools.reduce(operator.and_, where_clauses)) \
                              .order_by(getattr(Model, k).desc()) \
                              .limit(10)

    formatted_date_from_timestamp = datetime.utcfromtimestamp(utc_time.timestamp()).strftime('%Y-%m-%d %H:%M:%S')
    print ('Adding league leaders for {category} on {date}...'.format(category=k.upper(), date=formatted_date_from_timestamp))      

    player_keys_and_stats = []               
    for result in query:
      player_keys_and_stats.append({
        'player_key': result.player_key,
        'stat': float(getattr(result, k))
      })

    LeagueLeadersPlayoff.create(
      category=k,
      date=dt,
      player_keys_and_stats=player_keys_and_stats
    )

computeLeaders(PlayerStatsPlayoff, '2020-2021')