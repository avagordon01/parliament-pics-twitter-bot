import twitter
import config
api = twitter.Api(
    consumer_key=config.consumer_key,
    consumer_secret=config.consumer_secret,
    access_token_key=config.access_token_key,
    access_token_secret=config.access_token_secret
)
api.VerifyCredentials()

from glob import glob
from time import sleep
from os import remove

files = sorted(glob('out/*'))
for file in files:
    remove(file)
while True:
    files = sorted(glob('out/*'))
    try:
        print('posting ' + files[-1])
        api.PostMedia('', files[-1])
        for file in files:
            remove(file)
    except IndexError:
        pass
    sleep(120)
