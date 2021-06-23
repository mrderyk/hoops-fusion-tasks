class LeagueLeaderCriteria():
  def __init__(self, season_total_games, min_games_played_percentage=None, raw_stat=None, raw_stat_min_per_game=None):
    self.season_total_games = season_total_games
    self.min_games_played_percentage = min_games_played_percentage
    self.raw_stat = raw_stat
    self.raw_stat_min_per_game = raw_stat_min_per_game
  
  def get_min_games_played(self):
    return self.season_total_games * (self.min_games_played_percentage * .01) if self.min_games_played_percentage else None