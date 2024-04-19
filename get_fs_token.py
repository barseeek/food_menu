import pprint

from environs import Env
import requests
import re
from googletrans import Translator


env = Env()
env.read_env()

client_id = env.str('FS_CLIENT_ID')
client_secret = env.str('FS_CLIENT_SECRET')

url = 'https://oauth.fatsecret.com/connect/token'

headers = {
    'content-type': 'application/x-www-form-urlencoded'
}

data = {
    'grant_type': 'client_credentials',
    'scope': 'basic'
}

auth = (client_id, client_secret)
response = requests.post(url, headers=headers, data=data, auth=auth)

print(response.json())