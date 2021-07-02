from hfdb.models import Player

def backfill_searchable_tokens():
  players = Player.select()

  for p in players:
    if p.searchable_tokens: 
      continue

    searchable_name = '{first_name} {last_name}'.format(
      first_name=p.first_name.lower(),
      last_name=p.last_name.lower()
    )

    p.searchable_tokens = tokenize_name_for_search(searchable_name)
    p.save()
    print ('Backfilled tokens  for "{s}": {t}\n\n'.format(s=searchable_name, t=tokens))
  

def tokenize_name_for_search(searchable_name):
  tokens = []
  start = 0
  end = len(searchable_name)

  substr_end = start + 1

  while start < end:
    if searchable_name[start] == ' ':
      start = start + 1
      continue

    while substr_end <= end:
      token = ''.join([searchable_name[i] for i in range(start, substr_end)])
      substr_end = substr_end + 1
      if token:
          tokens.append(token)

    start = start + 1
    substr_end = start + 1
  return tokens


backfill_searchable_tokens()