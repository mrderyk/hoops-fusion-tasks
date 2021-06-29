import hashlib
import peewee

from hfdb.models.player import Player
from utils import fetch, compute_key_for_player

ROSTER_STATUS_TO_CODE = {
  'ROSTER': 0,
  'UFA': 1,
  'ASSIGNED_TO_MINORS': 2,
  'UNDRAFTED': 3,
  'ASSIGNED_TO_OTHER': 4,
  'ASSIGNED_TO_INJURY_LIST': 5,
  'UNASSIGNED': 6
}

def collect():
    r = fetch('players.json')

    if r.status_code != 200:
        return

    players_data = r.json()['players']
    for player_data in players_data:
        player = player_data['player']
        last_name = player['lastName']
        first_name = player['firstName']
        number = player['jerseyNumber']
        number = int(number) if number else None
        position = player['primaryPosition']
        dob = player.get('birthDate')
        birth_city = player.get('birthCity')
        birth_country = player.get('birthCountry')
        img_url = player.get('officialImageSrc')
        roster_status = ROSTER_STATUS_TO_CODE[player['currentRosterStatus']]

        injury = player.get('currentInjury')
        is_rookie = player.get('rookie')
        external_api_id = player['id']

        height_ft_in = player['height']
        if height_ft_in:
          height_parts = height_ft_in.replace('"','').split('\'')
          height = int(height_parts[0])*12 + int(height_parts[1])
        else: 
          height = None

        weight_str = player['weight']
        weight = int(weight_str) if weight_str else None

        team_details = player['currentTeam']
        if team_details:
          team_code = team_details['abbreviation']
        else: 
          team_code = None

        player_key = compute_key_for_player(first_name, last_name, external_api_id)

        try:
          p = Player.get(key=player_key)
        except peewee.DoesNotExist:
          p = Player.create(
            first_name=first_name,
            last_name=last_name,
            key=player_key,
            id=external_api_id,
            position=position,
            is_rookie=is_rookie
          )

        p.position = position
        p.number = number
        p.height = height
        p.weight = weight
        p.dob = dob
        p.birth_city = birth_city
        p.birth_country = birth_country
        p.img_url = img_url if img_url else None
        p.team_code = team_code
        p.injury = injury
        p.roster_status = roster_status
        p.save()
        

        print('# Updating player {key} - {last_name}, {first_name}...'.format(
            key=player_key,
            last_name=last_name,
            first_name=first_name
        ))


collect()