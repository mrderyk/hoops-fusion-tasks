CATEGORIES_TO_QUALIFYING_CRITERIA = {
  'min': None,
  'pts': None,
  'ast': None,
  'reb': None,
  'oreb': None,
  'dreb': None,
  'stl': None,
  'blk': None,
  'ftm': None,
  'tov': None,
  'foulp': None, 
  'fgm': None,
  'fg2m': None,
  'fg3m': None,
  'ptspg': None,
  'astpg': None,
  'rebpg': None,
  'orebpg': None,
  'drebpg': None,
  'stlpg': None,
  'blkpg': None,
  'ftapg': None,
  'ftmpg': None,
  'fg3mpg': None,
  'tovpg': None,
  'foulppg': None,
  'fgpct': None,
  'fg2pct': None,
  'fg3pct': None,
  'ftpct': None
}

def get_leader_categories_with_criteria(**kwargs):
  categories = { **CATEGORIES_TO_QUALIFYING_CRITERIA }
  for k in kwargs:
    if k in CATEGORIES_TO_QUALIFYING_CRITERIA:
      categories[k] = kwargs[k]

  return categories
