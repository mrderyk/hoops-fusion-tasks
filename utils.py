import base64
import hashlib
import requests

from config import API_KEY, API_PASSWORD, API_URL_ROOT

def fetch(url_path):
  full_url = '{url_root}/{url_path}'.format(url_root=API_URL_ROOT, url_path=url_path)

  return requests.get(
    url=full_url,
    headers={
      "Authorization": "Basic " + base64.b64encode('{}:{}'.format(API_KEY, API_PASSWORD).encode('utf-8')).decode('ascii')
    }
  )

def compute_key_for_player(first_name, last_name, external_api_id):
  full_name = '{lname} {fname}'.format(
    lname=last_name.lower(),
    fname=first_name.lower()
  )

  to_hash = '{full_name}_{external_api_id}'.format(
      full_name=full_name,
      external_api_id=external_api_id
  )
  m = hashlib.md5()
  m.update(to_hash.encode('utf-8'))

  return m.hexdigest()

def compute_stats_key_for_player(first_name, last_name, external_api_id, season):
  full_name = '{lname} {fname}'.format(
    lname=last_name.lower(),
    fname=first_name.lower()
  )

  to_hash = '{full_name}_{external_api_id}_{season}'.format(
      full_name=full_name,
      external_api_id=external_api_id,
      season=season
  )
  m = hashlib.md5()
  m.update(to_hash.encode('utf-8'))

  return m.hexdigest()

def decode_utf8(str):
  return u''.join(str).encode('utf-8').strip()